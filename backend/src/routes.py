from dotenv import load_dotenv
load_dotenv()

# list endpoints here
from fastapi import APIRouter, HTTPException, Body, Path, Query
from schemas import ResigneeDisplay, ResigneeCreate
from services import parse_resignee_text, generate_csv_report, generate_xls_report, is_no_existing_account
from datetime import datetime
from supabase_client import supabase
from io import StringIO, BytesIO
from fastapi.responses import Response
from crypto_utils import encrypt_field, decrypt_field
import hashlib

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

            encrypted_data = {
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
                "date_hr_emailed": datetime.now().strftime("%Y-%m-%d"),
                "um_date_deac": None,
                "tp_date_deac": None, 
                "email_date_deac": None, 
                "windows_date_deac": None,
                "remarks": None
            }
            supabase.table("ResignedEmployees").insert(encrypted_data).execute()

            # For formatting the name field in the response only
            cleaned_entries.append(ResigneeDisplay(
                **entry.model_dump(exclude={'last_name', 'first_name', 'middle_name'}),
                name=entry.last_name + ", " + entry.first_name + " " + entry.middle_name,
                date_hr_emailed=datetime.now().strftime("%m-%d-%Y"),
                um_date_deac=None,
                tp_date_deac=None,
                email_date_deac=None,
                windows_date_deac=None,
                remarks=None
            ))

        return cleaned_entries

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Endpoint serving list of unprocessed resignees to client (frontend) 
@router.get("")
async def get_all_unprocessed_resignees():
    try:
        response = supabase.table("ResignedEmployees") \
            .select("*") \
            .or_("um_date_deac.is_.null, tp_date_deac.is_.null, email_date_deac.is_.null, windows_date_deac.is_.null") \
            .execute()
        
        to_display = response.data
        cleaned_entries: list[ResigneeDisplay] = []

        for entry in to_display:
            try:
                # Print types and values for debugging
                print("Decrypting entry:", entry)
                employee_no = decrypt_field(entry['employee_no']) if entry.get('employee_no') else ""
                last_name = decrypt_field(entry['last_name']) if entry.get('last_name') else ""
                first_name = decrypt_field(entry['first_name']) if entry.get('first_name') else ""
                middle_name = decrypt_field(entry['middle_name']) if entry.get('middle_name') else ""
                cost_center = decrypt_field(entry['cost_center']) if entry.get('cost_center') else ""
                position_title = decrypt_field(entry['position_title']) if entry.get('position_title') else ""
                rank = decrypt_field(entry['rank']) if entry.get('rank') else ""
                department = decrypt_field(entry['department']) if entry.get('department') else ""
                remarks = decrypt_field(entry['remarks']) if entry.get('remarks') else ""

                cleaned_entries.append(ResigneeDisplay(
                    employee_no=employee_no,
                    date_hired=entry.get('date_hired', ""),
                    cost_center=cost_center,
                    name=f"{last_name}, {first_name} {middle_name}",
                    position_title=position_title,
                    rank=rank,
                    department=department,
                    last_day=entry.get('last_day', ""),
                    date_hr_emailed=entry.get('date_hr_emailed', ""),
                    um_date_deac=entry.get('um_date_deac', ""),
                    tp_date_deac=entry.get('tp_date_deac', ""),
                    email_date_deac=entry.get('email_date_deac', ""),
                    windows_date_deac=entry.get('windows_date_deac', ""),
                    remarks=remarks
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
            .update({"last_day": last_day}) \
            .eq("employee_no_hash", employee_no_hash) \
            .execute()
        
        if response.data and len(response.data) > 0:
            return {"message": f"Changed employee {employee_no} last day to {last_day}."}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{employee_no}/um")
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
            return {"message": f"Set employee {employee_no} Batch Deactivation from UM date to {um_date_deac}."}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{employee_no}/third-party")
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
            return {"message": f"Set employee {employee_no} 3rd party systems deactivation date to {tp_date_deac}."}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{employee_no}/email")
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
            return {"message": f"Set employee {employee_no} e-mail deactivation date to {email_date_deac}."}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{employee_no}/windows")
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
            return {"message": f"Set employee {employee_no} windows return date to {windows_date_deac}."}
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
async def edit_windows_deactivation_date(
    employee_no: str = Path(...),
    remarks: str = Body(..., media_type="text/plain")
):
    try:
        employee_no_hash = hash_employee_no(employee_no)
        response = supabase.table("ResignedEmployees") \
            .update({"remarks": remarks}) \
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
        # end_datetime = datetime.fromisoformat(end_date)

        # # Set the time to 23:59:59 of the same day
        # end_datetime = end_datetime.replace(hour=23, minute=59, second=59)

        # # Convert back to ISO format string if needed
        # end_date_with_time = end_datetime.isoformat()
        
        response = supabase.table("ResignedEmployees") \
            .select("*") \
            .execute()
        
        if response.data and len(response.data) > 0:
            # Decrypt fields for the report if needed
            decrypted_data = []
            for entry in response.data:
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
                    "Date HR Emailed": entry['date_hr_emailed'],
                    "Batch Deactivation from UM": "No Existing Account" if is_no_existing_account(entry['um_date_deac']) else entry['um_date_deac'],
                    "3rd party systems/apps": "No Existing Account" if is_no_existing_account(entry['tp_date_deac']) else entry['tp_date_deac'],
                    "E-mails": "No Existing Account" if is_no_existing_account(entry['email_date_deac']) else entry['email_date_deac'],
                    "Windows": "No Existing Account" if is_no_existing_account(entry['windows_date_deac']) else entry['windows_date_deac'],
                    "Remarks": decrypt_field(entry['remarks'])
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
        raise HTTPException(status_code=400, detail=str(e))
    
# Endpoint to mark resignation entry as processed (will now not be returned to client )
# @router.put("/{employee_no}/process")
# async def mark_resignee_processed(employee_no: str = Path(...)):
#     try:
#         now = datetime.now().isoformat()
#         employee_no_hash = hash_employee_no(employee_no)
#         response = supabase.table("ResignedEmployees") \
#             .update({"processed_date_time": now}) \
#             .eq("employee_no_hash", employee_no_hash) \
#             .execute()
#         if response.data and len(response.data) > 0:
#             return {"message": f"Employee {employee_no} marked as processed.", "processed_date_time": now}
#         else:
#             raise HTTPException(status_code=404, detail="Employee not found")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


# @router.put("/{employee_no}/unprocess")
# async def unmark_resignee_processed(
#     employee_no: str = Path(..., description="Employee number to unmark as processed")
# ):
#     """
#     Unmark a resignee as processed by setting the processed_date_time to None.
#     """
#     try:
#         employee_no_hash = hash_employee_no(employee_no)
#         response = supabase.table("ResignedEmployees") \
#             .update({"processed_date_time": None}) \
#             .eq("employee_no_hash", employee_no_hash) \
#             .execute()
#         if response.data and len(response.data) > 0:
#             return {"message": f"Employee {employee_no} unmarked as processed."}
#         else:
#             raise HTTPException(status_code=404, detail="Employee not found")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))