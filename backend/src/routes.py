from dotenv import load_dotenv
load_dotenv()

from fastapi import APIRouter, HTTPException, Body, Path, Query, Depends
from src.schemas import ResigneeDisplay, ResigneeCreate, Account, EditDate, Status
from src.services import parse_resignee_text, generate_csv_report, generate_xls_report, is_late
from datetime import datetime, timedelta
from src.database import get_engine
from io import StringIO, BytesIO
from fastapi.responses import Response
import hashlib
from typing import Any
from sqlmodel import Session, select, desc
from src.models import Resignee

router = APIRouter(
    prefix="/resignees",
    tags=["resignee"]
)

def get_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session

def hash_employee_no(employee_no: str) -> str:
    return hashlib.sha256(employee_no.encode()).hexdigest()

# Endpoint accepting raw text (details) of resignees; will parse and add data to database
@router.post("", response_model=list[ResigneeDisplay])
async def add_resignees(
    resignees: str = Body(..., media_type="text/plain"),
    session: Session = Depends(get_session)
):
    """
    Handle raw resignee details and return parsed data per employee.
    Encrypt all fields except dates/timestamps before storing.
    Raise error if employee_no is not unique.
    """
    try:
        entries: list[ResigneeCreate] = parse_resignee_text(resignees)
        cleaned_entries: list[ResigneeDisplay] = []

        for entry in entries:
            employee_no= entry.employee_no
            
            # Check for duplicate
            existing = session.exec(
                select(Resignee)
                .where(Resignee.employee_no == employee_no)
            ).first()
            
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail=f"Duplicate employee_no detected: {entry.employee_no}"
                )

            # Create new resignee record
            resignee = Resignee(
                employee_no=entry.employee_no,
                last_name=entry.last_name,
                first_name=entry.first_name,
                middle_name=entry.middle_name,
                cost_center=entry.cost_center,
                position_title=entry.position_title,
                rank=entry.rank,
                department=entry.department,
                date_hired=datetime.strptime(entry.date_hired, "%m/%d/%Y").date(),
                last_day=datetime.strptime(entry.last_day, "%m/%d/%Y").date(),
                date_hr_emailed=datetime.now(),
                processed_date_time=None,
                um_date_deac=None,
                tp_date_deac=None,
                email_date_deac=None,
                windows_date_deac=None,
                remarks=None
            )

            session.add(resignee)
            
            # For response
            cleaned_entries.append(ResigneeDisplay(
                **entry.model_dump(exclude={'last_name', 'first_name', 'middle_name'}),
                name=f"{entry.last_name}, {entry.first_name} {entry.middle_name}",
                date_hr_emailed=datetime.now().strftime("%m-%d-%Y"),
                um=None,
                third_party=None,
                email=None,
                windows=None,
                remarks=None,
                um_late=False,
                third_party_late=False,
                email_late=False,
                windows_late=False,
                processed_date_time=None
            ))

        session.commit()
        return cleaned_entries

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    

# Endpoint serving list of unprocessed resignees to client (frontend) 
@router.get("")
async def get_all_unprocessed_resignees(session: Session = Depends(get_session)):
    try:
        # Get unprocessed resignees
        statement = select(Resignee).where(
            Resignee.processed_date_time == None
        ).order_by(desc(Resignee.date_hr_emailed))
        unprocessed = session.exec(statement).all()

        # Get recently processed (last 24 hours)
        past_day_date = datetime.now() - timedelta(days=1)
        statement = (
            select(Resignee)
            .where(Resignee.processed_date_time != None)
            .where(Resignee.processed_date_time >= past_day_date)
        )
        recently_processed = session.exec(statement).all()

        all_resignees: list[Resignee] = list(unprocessed) + list(recently_processed)
        cleaned_entries: list[ResigneeDisplay] = []

        for entry in all_resignees:
            try:

                cleaned_entries.append(ResigneeDisplay(
                    employee_no=entry.employee_no,
                    date_hired=entry.date_hired.strftime("%Y-%m-%d") if entry.date_hired else "",
                    cost_center=entry.cost_center,
                    name=f"{entry.last_name}, {entry.first_name} {entry.middle_name}",
                    position_title=entry.position_title,
                    rank=entry.rank,
                    department=entry.department,
                    last_day=entry.last_day.strftime("%Y-%m-%d") if entry.last_day else "",
                    date_hr_emailed=entry.date_hr_emailed.strftime("%Y-%m-%d") if entry.date_hr_emailed else "",
                    um=entry.um_date_deac.strftime("%Y-%m-%d") if entry.um_date_deac else "",
                    third_party=entry.tp_date_deac.strftime("%Y-%m-%d") if entry.tp_date_deac else "",
                    email=entry.email_date_deac.strftime("%Y-%m-%d") if entry.email_date_deac else "",
                    windows=entry.windows_date_deac.strftime("%Y-%m-%d") if entry.windows_date_deac else "",
                    remarks=entry.remarks,
                    um_late=is_late(entry.last_day, entry.um_date_deac, entry.date_hr_emailed, Account.UM),
                    third_party_late=is_late(entry.last_day, entry.tp_date_deac, entry.date_hr_emailed, Account.TP),
                    email_late=is_late(entry.last_day, entry.email_date_deac, entry.date_hr_emailed, Account.EM),
                    windows_late=is_late(entry.last_day, entry.windows_date_deac, entry.date_hr_emailed, Account.WN),
                    processed_date_time=entry.processed_date_time.strftime("%Y-%m-%d %H:%M:%S") if entry.processed_date_time else ""
                ))
            except Exception as inner_e:
                print(f"Error processing entry {entry.employee_no}: {str(inner_e)}")
                continue

        return cleaned_entries
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{employee_no}/last_day")    
async def edit_employee_last_day(
    employee_no: str = Path(...),
    last_day: str = Body(..., media_type="text/plain"),
    session: Session = Depends(get_session)
):
    """
    Edit an employee's recorded last day.
    Format: YYYY-MM-DD
    """
    try:
        parsed_last_day = datetime.strptime(last_day, "%Y-%m-%d").date()
        statement = select(Resignee).where(Resignee.employee_no == employee_no)
        result = session.exec(statement).first()
        if not result:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        result.last_day = parsed_last_day
        session.add(result)
        session.commit()
        return {"message": f"Changed employee {employee_no} last day to {parsed_last_day}."}

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{employee_no}/um", response_model=EditDate)
async def edit_um_deactivation_date(
    employee_no: str = Path(...),
    um_date_deac: str = Body(..., media_type="text/plain"),
    session: Session = Depends(get_session)
):
    try:
        parsed_um_date = datetime.strptime(um_date_deac, "%Y-%m-%d").date()
        statement = select(Resignee).where(Resignee.employee_no == employee_no)
        resignee = session.exec(statement).first()

        if not resignee:
            raise HTTPException(status_code=404, detail="Employee not found")

        # Update UM deactivation date
        resignee.um_date_deac = parsed_um_date
        session.commit()

        # Determine lateness
        late = is_late(
            resigned=resignee.last_day,
            deac=parsed_um_date if parsed_um_date else None,
            hr=resignee.date_hr_emailed,
            acc=Account.UM
        )

        return EditDate(
            message=f"Set employee {employee_no} Batch Deactivation from UM date to {um_date_deac}.",
            date=um_date_deac,
            late=late
        )

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{employee_no}/third-party", response_model=EditDate)
async def edit_tp_deactivation_date(
    employee_no: str = Path(...),
    tp_date_deac: str = Body(..., media_type="text/plain"),
    session: Session = Depends(get_session)
):
    try:
        parsed_tp_date = datetime.strptime(tp_date_deac, "%Y-%m-%d").date()
        statement = select(Resignee).where(Resignee.employee_no == employee_no)
        resignee = session.exec(statement).first()

        if not resignee:
            raise HTTPException(status_code=404, detail="Employee not found")

        # Update TP deactivation date
        resignee.tp_date_deac = parsed_tp_date
        session.commit()

        # Determine lateness
        late = is_late(
            resigned=resignee.last_day,
            deac=parsed_tp_date if parsed_tp_date else None,
            hr=resignee.date_hr_emailed,
            acc=Account.TP
        )

        return EditDate(
            message=f"Set employee {employee_no} Third Party Account deactivation date to {tp_date_deac}.",
            date=tp_date_deac,
            late=late
        )

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{employee_no}/email", response_model=EditDate)
async def edit_email_deactivation_date(
    employee_no: str = Path(...),
    email_date_deac: str = Body(..., media_type="text/plain"),
    session: Session = Depends(get_session)
):
    try:
        parsed_email_date = datetime.strptime(email_date_deac, "%Y-%m-%d").date()
        statement = select(Resignee).where(Resignee.employee_no == employee_no)
        resignee = session.exec(statement).first()

        if not resignee:
            raise HTTPException(status_code=404, detail="Employee not found")

        # Update Email deactivation date
        resignee.email_date_deac = parsed_email_date
        session.commit()

        # Determine lateness
        late = is_late(
            resigned=resignee.last_day,
            deac=parsed_email_date if parsed_email_date else None,
            hr=resignee.date_hr_emailed,
            acc=Account.EM
        )

        return EditDate(
            message=f"Set employee {employee_no} Email Deactivation date to {email_date_deac}.",
            date=email_date_deac,
            late=late
        )

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{employee_no}/windows", response_model=EditDate)
async def edit_windows_deactivation_date(
    employee_no: str = Path(...),
    windows_date_deac: str = Body(..., media_type="text/plain"),
    session: Session = Depends(get_session)
):
    try:
        parsed_win_date = datetime.strptime(windows_date_deac, "%Y-%m-%d").date()
        statement = select(Resignee).where(Resignee.employee_no == employee_no)
        resignee = session.exec(statement).first()

        if not resignee:
            raise HTTPException(status_code=404, detail="Employee not found")

        # Update WN deactivation date
        resignee.windows_date_deac = parsed_win_date
        session.commit()

        # Determine lateness
        late = is_late(
            resigned=resignee.last_day,
            deac=parsed_win_date if parsed_win_date else None,
            hr=resignee.date_hr_emailed,
            acc=Account.WN
        )

        return EditDate(
            message=f"Set employee {employee_no} Windows deactivation date to {windows_date_deac}.",
            date=windows_date_deac,
            late=late
        )

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{employee_no}/date_hr_emailed")
async def edit_hr_emailed_date(
    employee_no: str = Path(...),
    date_hr_emailed: str = Body(..., media_type="text/plain"),
    session: Session = Depends(get_session)
):
    try:
        date_hr = datetime.now()
        statement = select(Resignee).where(Resignee.employee_no == employee_no)
        result = session.exec(statement).first()

        if not result:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        result.date_hr_emailed = date_hr
        session.commit()
        return {"message": f"HR email date updated."}

    except ValueError:
        raise HTTPException(status_code=400)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{employee_no}/remarks")
async def edit_remarks(
    employee_no: str = Path(...),
    remarks: str | None = Body(..., media_type="text/plain"),
    session: Session = Depends(get_session)
):
    try:

        statement = select(Resignee).where(Resignee.employee_no == employee_no)
        result = session.exec(statement).first()

        if not result:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        result.remarks = remarks
        session.commit()
        return {"message": f"Set employee {employee_no} remarks."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/report")
async def get_report(
    start_date: str, 
    end_date: str, 
    format: str = Query(default="csv", regex="^(csv|xlsx)$"),
    session: Session = Depends(get_session)
):
    """
    Generate an CSV or XLSX report of processed resignees within a selected timeframe.
    """
    try:
        end = datetime.fromisoformat(end_date).date()
        start = datetime.fromisoformat(start_date).date()

        statement = (
            select(Resignee)
            .where(Resignee.last_day >= start)
            .where(Resignee.last_day <= end)
        )

        resignees = session.exec(statement).all()

        if not resignees:
            raise HTTPException(status_code=404, detail="There were no resignees processed within the given period")
        

        report_data: list[Any] = []
        for r in resignees:
            report_data.append({
                "Employee no.": r.employee_no,
                "Last Name": r.last_name,
                "First Name": r.first_name,
                "Middle Name": r.middle_name,
                "Cost center": r.cost_center,
                "Position Title": r.position_title,
                "Rank": r.rank,
                "Department": r.department,
                "Date hired": r.date_hired.strftime("%Y-%m-%d"),
                "Last day with AUB": r.last_day,
                "Date HR Emailed": r.date_hr_emailed,
                "Batch Deactivation from UM": r.um_date_deac if r.um_date_deac else "",
                "3rd party systems/apps": r.tp_date_deac if r.tp_date_deac else "",
                "E-mails": r.email_date_deac if r.email_date_deac else "",
                "Windows": r.windows_date_deac if r.windows_date_deac else "",
                "Remarks": r.remarks or "",
                "Status": Status.PROCESSED if r.processed_date_time else Status.UNPROCESSED,
                "Processed on": r.processed_date_time.strftime("%B %d, %Y %I:%M %p") if r.processed_date_time else "",
            })


        if format == "csv":
            csv_file = StringIO()
            generate_csv_report(csv_file, report_data)
            return Response(
                content=csv_file.getvalue(),
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=export.csv"},
            )

        elif format == "xlsx":
            excel_file = BytesIO()
            generate_xls_report(excel_file, report_data)
            excel_file.seek(0)
            return Response(
                content=excel_file.read(),
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": "attachment; filename=export.xlsx"},
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint to mark resignation entry as processed (will now not be returned to client )
@router.put("/{employee_no}/process")
async def mark_resignee_processed(
    employee_no: str = Path(...),
    session: Session = Depends(get_session)
):
    try:
        now = datetime.now()
        statement = select(Resignee).where(Resignee.employee_no == employee_no)
        resignee = session.exec(statement).first()

        if not resignee:
            raise HTTPException(status_code=404, detail="Employee not found")

        resignee.processed_date_time = now
        session.commit()

        return {
            "message": f"Employee {employee_no} marked as processed.",
            "processed_date_time": now.isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{employee_no}/unprocess")
async def unmark_resignee_processed(
    employee_no: str = Path(..., description="Employee number to unmark as processed"),
    session: Session = Depends(get_session)
):
    """
    Unmark a resignee as processed by setting processed_date_time to None.
    """
    try:

        statement = select(Resignee).where(Resignee.employee_no == employee_no)
        resignee = session.exec(statement).first()

        if not resignee:
            raise HTTPException(status_code=404, detail="Employee not found")

        resignee.processed_date_time = None
        session.commit()

        return {"message": f"Employee {employee_no} unmarked as processed."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
