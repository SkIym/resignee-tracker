from dotenv import load_dotenv
load_dotenv()

# list endpoints here
from fastapi import APIRouter, HTTPException, Body, Path, Query
from schemas import ResigneeDisplay, ResigneeCreate, Account, EditDate, Status
from services import parse_resignee_text, generate_csv_report, generate_xls_report, is_late
from datetime import datetime, timedelta
from supabase_client import supabase
from io import StringIO, BytesIO
from fastapi.responses import Response
from crypto_utils import encrypt_field, decrypt_field
import hashlib
from typing import Any

router = APIRouter(
    prefix="/resignees",
    tags=["resignee"]
)

def hash_employee_no(employee_no: str) -> str:
    return hashlib.sha256(employee_no.encode()).hexdigest()

# Endpoint accepting raw text (details) of resignees; will parse and add data to database
@router.post("", response_model=list[ResigneeDisplay])
async def add_resignees(resignees: str = Body(..., media_type="text/plain")):
    """
    Handle raw resignee details and return parsed data per employee.
    Encrypt all fields except dates/timestamps before storing.
    Raise error if employee_no is not unique.
    """
    
    try:
        entries: list[ResigneeCreate] = parse_resignee_text(resignees)
        cleaned_entries: list[ResigneeDisplay] = []
        data: list[dict[str, Any]] = []

        for entry in entries:
            employee_no_hash = hash_employee_no(entry.employee_no)
            # Check for duplicate
            existing = supabase.table("ResignedEmployees") \
                .select("employee_no_hash") \
                .eq("employee_no_hash", employee_no_hash) \
                .execute()
            if existing.data and len(existing.data) > 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"Duplicate employee_no detected: {entry.employee_no}"
                )

            encrypted_data: dict[str, Any] = {
                "employee_no": encrypt_field(entry.employee_no),
                "employee_no_hash": employee_no_hash,
                "last_name": encrypt_field(entry.last_name),
                "first_name": encrypt_field(entry.first_name),
                "middle_name": encrypt_field(entry.middle_name),
                "cost_center": encrypt_field(entry.cost_center),
                "position_title": encrypt_field(entry.position_title),
                "rank": encrypt_field(entry.rank),
                "department": encrypt_field(entry.department),
                "date_hired": datetime.strptime(entry.date_hired, "%m/%d/%Y").strftime("%Y-%m-%d"),
                "last_day": datetime.strptime(entry.last_day, "%m/%d/%Y").strftime("%Y-%m-%d"),
                "date_hr_emailed": datetime.now().isoformat(),
                "um_date_deac": None,
                "tp_date_deac": None, 
                "email_date_deac": None, 
                "windows_date_deac": None,
                "remarks": None,
                "processed_date_time": None
            }

            data.append(encrypted_data)

            # For formatting the name field in the response only
            cleaned_entries.append(ResigneeDisplay(
                **entry.model_dump(exclude={'last_name', 'first_name', 'middle_name'}),
                name=entry.last_name + ", " + entry.first_name + " " + entry.middle_name,
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

        supabase.table("ResignedEmployees").insert(data).execute()
        return cleaned_entries

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Endpoint serving list of unprocessed resignees to client (frontend) 
@router.get("")
async def get_all_unprocessed_resignees():
    try:
        response = supabase.table("ResignedEmployees") \
            .select("*") \
            .is_("processed_date_time", "null") \
            .order("date_hr_emailed", desc=True) \
            .execute()
        
        to_display = response.data
        past_day_date = (datetime.now() - timedelta(days=1)).isoformat()

        response = supabase.table("ResignedEmployees") \
            .select("*") \
            .not_.is_("processed_date_time", "null") \
            .gte("processed_date_time", past_day_date) \
            .execute()

        to_display.extend(response.data) 

        cleaned_entries: list[ResigneeDisplay] = []

        for entry in to_display:
            try:
                # Print types and values for debugging
                employee_no = decrypt_field(entry['employee_no']) if entry.get('employee_no') else ""
                last_name = decrypt_field(entry['last_name']) if entry.get('last_name') else ""
                first_name = decrypt_field(entry['first_name']) if entry.get('first_name') else ""
                middle_name = decrypt_field(entry['middle_name']) if entry.get('middle_name') else ""
                cost_center = decrypt_field(entry['cost_center']) if entry.get('cost_center') else ""
                position_title = decrypt_field(entry['position_title']) if entry.get('position_title') else ""
                rank = decrypt_field(entry['rank']) if entry.get('rank') else ""
                department = decrypt_field(entry['department']) if entry.get('department') else ""
                remarks = decrypt_field(entry['remarks']) if entry.get('remarks') else ""

                um = entry.get('um_date_deac', "")
                third_party = entry.get('tp_date_deac', "")
                email = entry.get('email_date_deac', "")
                windows = entry.get('windows_date_deac', "")
                last_day = entry.get('last_day', "")
                date_hr_emailed = entry.get('date_hr_emailed', "")

                cleaned_entries.append(ResigneeDisplay(
                    employee_no=employee_no,
                    date_hired=entry.get('date_hired', ""),
                    cost_center=cost_center,
                    name=f"{last_name}, {first_name} {middle_name}",
                    position_title=position_title,
                    rank=rank,
                    department=department,
                    last_day=last_day,
                    date_hr_emailed=date_hr_emailed,
                    um=um,
                    third_party=third_party,
                    email=email,
                    windows=windows,
                    remarks=remarks,
                    um_late=is_late(last_day, um, date_hr_emailed, Account.UM),
                    third_party_late=is_late(last_day, third_party, date_hr_emailed, Account.TP),
                    email_late=is_late(last_day, email, date_hr_emailed, Account.EM),
                    windows_late=is_late(last_day, windows, date_hr_emailed, Account.WN),
                    processed_date_time=entry.get('processed_date_time', "")
                ))
            except Exception as inner_e:
                print("Error decrypting entry:", entry)
                print("Exception:", repr(inner_e))
                continue  # Skip this entry if it fails

        return cleaned_entries
    
    except Exception as e:
        print("Outer exception:", e)
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{employee_no}/last_day")    
async def edit_employee_last_day(
    employee_no: str = Path(...),
    last_day: str = Body(..., media_type="text/plain")
):
    """
    Edit an employee's recorded last day.
    Format: YYYY-MM-DD
    """
    try:
        employee_no_hash = hash_employee_no(employee_no)
        response = supabase.table("ResignedEmployees") \
            .update({"last_day": last_day})  \
            .eq("employee_no_hash", employee_no_hash) \
            .execute()
        
        if response.data and len(response.data) > 0:
            return {"message": f"Changed employee {employee_no} last day to {last_day}."}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{employee_no}/um", response_model=EditDate)
async def edit_um_deactivation_date(
    employee_no: str = Path(...),
    um_date_deac: str = Body(..., media_type="text/plain")
):
    try:
        employee_no_hash = hash_employee_no(employee_no)
        response = supabase.table("ResignedEmployees") \
            .update({"um_date_deac": um_date_deac}) \
            .eq("employee_no_hash", employee_no_hash) \
            .execute()
        
        if response.data and len(response.data) > 0:
            emp = response.data[0]

            return EditDate(
                message = f"Set employee {employee_no} Batch Deactivation from UM date to {um_date_deac}.",
                date = um_date_deac,
                late = is_late(emp['last_day'], um_date_deac, emp['date_hr_emailed'], Account.UM)
            )
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{employee_no}/third-party", response_model=EditDate)
async def edit_tp_deactivation_date(
    employee_no: str = Path(...),
    tp_date_deac: str = Body(..., media_type="text/plain")
):
    try:
        employee_no_hash = hash_employee_no(employee_no)
        response = supabase.table("ResignedEmployees") \
            .update({"tp_date_deac": tp_date_deac}) \
            .eq("employee_no_hash", employee_no_hash) \
            .execute()
        
        if response.data and len(response.data) > 0:
            emp = response.data[0]

            return EditDate(
                message = f"Set employee {employee_no} 3rd party systems deactivation date to {tp_date_deac}.",
                date = tp_date_deac,
                late = is_late(emp['last_day'], tp_date_deac, emp['date_hr_emailed'], Account.TP)
            )

        else:
            raise HTTPException(status_code=404, detail="Employee not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{employee_no}/email", response_model=EditDate)
async def edit_email_deactivation_date(
    employee_no: str = Path(...),
    email_date_deac: str = Body(..., media_type="text/plain")
):
    try:
        employee_no_hash = hash_employee_no(employee_no)
        response = supabase.table("ResignedEmployees") \
            .update({"email_date_deac": email_date_deac}) \
            .eq("employee_no_hash", employee_no_hash) \
            .execute()
        
        if response.data and len(response.data) > 0:
            emp = response.data[0]

            return EditDate(
                message = f"Set employee {employee_no} e-mail deactivation date to {email_date_deac}.",
                date = email_date_deac,
                late = is_late(emp['last_day'], email_date_deac, emp['date_hr_emailed'], Account.EM)
            )

        else:
            raise HTTPException(status_code=404, detail="Employee not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{employee_no}/windows", response_model=EditDate)
async def edit_windows_deactivation_date(
    employee_no: str = Path(...),
    windows_date_deac: str = Body(..., media_type="text/plain")
):
    try:
        employee_no_hash = hash_employee_no(employee_no)
        response = supabase.table("ResignedEmployees") \
            .update({"windows_date_deac": windows_date_deac}) \
            .eq("employee_no_hash", employee_no_hash) \
            .execute()
        
        if response.data and len(response.data) > 0:
            emp = response.data[0]

            return EditDate(
                message = f"Set employee {employee_no} windows return date to {windows_date_deac}.",
                date = windows_date_deac,
                late = is_late(emp['last_day'], windows_date_deac, emp['date_hr_emailed'], Account.WN)
            )
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{employee_no}/date_hr_emailed")
async def edit_hr_emailed_date(
    employee_no: str = Path(...),
    date_hr_emailed: str = Body(..., media_type="text/plain")
):
    try:
        employee_no_hash = hash_employee_no(employee_no)
        response = supabase.table("ResignedEmployees") \
            .update({"date_hr_emailed": date_hr_emailed}) \
            .eq("employee_no_hash", employee_no_hash) \
            .execute()
        
        if response.data and len(response.data) > 0:
            return {"message": f"Changed date when HR emailed on employee {employee_no} resignation."}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{employee_no}/remarks")
async def edit_remarks(
    employee_no: str = Path(...),
    remarks: str | None = Body(..., media_type="text/plain")
):
    try:
        employee_no_hash = hash_employee_no(employee_no)
        response = supabase.table("ResignedEmployees") \
            .update({"remarks": encrypt_field(remarks) if remarks else None}) \
            .eq("employee_no_hash", employee_no_hash) \
            .execute()
        
        if response.data and len(response.data) > 0:
            return {"message": f"Set employee {employee_no} remarks."}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/report")
async def get_report(start_date: str, end_date: str, format: str = Query(default="csv", regex="^(csv|xlsx)$")):
    """
    Generate an CSV or XLSX report of processed resignees within a selected timeframe.
    """
    try:
        end_date = datetime.fromisoformat(end_date).date().strftime("%Y-%m-%d")
        start_date = datetime.fromisoformat(start_date).date().strftime("%Y-%m-%d")

        response = supabase.table("ResignedEmployees") \
            .select("*") \
            .lte("last_day", end_date) \
            .gte("last_day", start_date) \
            .execute()
        
        if response.data and len(response.data) > 0:
            # Decrypt fields for the report if needed
            decrypted_data = []
            for entry in response.data:
                print(entry.keys())
                
                decrypted_data.append({
                    "Employee no.": decrypt_field(entry['employee_no']),
                    "Last Name": decrypt_field(entry['last_name']),
                    "First Name": decrypt_field(entry['first_name']),
                    "Middle Name": decrypt_field(entry['middle_name']),
                    "Cost center": decrypt_field(entry['cost_center']),
                    "Position Title": decrypt_field(entry['position_title']),
                    "Rank": decrypt_field(entry['rank']),
                    "Department": decrypt_field(entry['department']),
                    "Date hired": entry['date_hired'],
                    "Last day with AUB": entry['last_day'],
                    "Date HR Emailed": datetime.fromisoformat(entry['date_hr_emailed']).strftime("%Y-%m-%d"),
                    "Batch Deactivation from UM": entry['um_date_deac'],
                    "3rd party systems/apps": entry['tp_date_deac'],
                    "E-mails": entry['email_date_deac'],
                    "Windows": entry['windows_date_deac'],
                    "Remarks": (decrypt_field(entry['remarks']) if entry['remarks'] else ""),
                    "Status": Status.PROCESSED if entry["processed_date_time"] else Status.UNPROCESSED,
                    "Processed on": (
                        datetime.fromisoformat(entry['processed_date_time'].replace("Z", "+00:00")).strftime("%B %d, %Y %I:%M %p")
                        if entry.get('processed_date_time') else ""
                    )
                })

            if format == "csv":
                csv_file = StringIO()
                generate_csv_report(csv_file, decrypted_data)
                return Response(
                content=csv_file.getvalue(),
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=export.csv"},
                )

            elif format == "xlsx":
                excel_file = BytesIO()
                generate_xls_report(excel_file, decrypted_data)
                excel_file.seek(0)
                return Response(
                    content=excel_file.read(),
                    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    headers={"Content-Disposition": "attachment; filename=export.xlsx"},
                )
        else:
            raise HTTPException(status_code=404, detail="There were no resignees processed within the given period")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint to mark resignation entry as processed (will now not be returned to client )
@router.put("/{employee_no}/process")
async def mark_resignee_processed(employee_no: str = Path(...)):
    try:
        now = datetime.now().isoformat()
        employee_no_hash = hash_employee_no(employee_no)
        response = supabase.table("ResignedEmployees") \
            .update({"processed_date_time": now}) \
            .eq("employee_no_hash", employee_no_hash) \
            .execute()
        if response.data and len(response.data) > 0:
            return {"message": f"Employee {employee_no} marked as processed.", "processed_date_time": now}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{employee_no}/unprocess")
async def unmark_resignee_processed(
    employee_no: str = Path(..., description="Employee number to unmark as processed")
):
    """
    Unmark a resignee as processed by setting the processed_date_time to None.
    """
    try:
        employee_no_hash = hash_employee_no(employee_no)
        response = supabase.table("ResignedEmployees") \
            .update({"processed_date_time": None}) \
            .eq("employee_no_hash", employee_no_hash) \
            .execute()
        if response.data and len(response.data) > 0:
            return {"message": f"Employee {employee_no} unmarked as processed."}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))