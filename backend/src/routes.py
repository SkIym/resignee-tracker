from dotenv import load_dotenv
load_dotenv()

# list endpoints here
from fastapi import APIRouter, HTTPException, Body, Path, Form
from schemas import ResigneeDisplay, ResigneeCreate
from services import parse_resignee_text, generate_report
from datetime import datetime
from supabase_client import supabase
from io import BytesIO
from fastapi.responses import Response
from datetime import timedelta
from crypto_utils import encrypt_field, decrypt_field
import jwt
import os
import hashlib

router = APIRouter()

def hash_employee_no(employee_no: str) -> str:
    return hashlib.sha256(employee_no.encode()).hexdigest()

# Endpoint accepting raw text (details) of resignees; will parse and add data to database
@router.post("/resignees", response_model=list[ResigneeDisplay])
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
                "processed_date_time": None
            }
            supabase.table("ResignedEmployees").insert(encrypted_data).execute()

            # For formatting the name field in the response only
            cleaned_entries.append(ResigneeDisplay(
                **entry.model_dump(exclude={'last_name', 'first_name', 'middle_name'}),
                name=entry.last_name + ", " + entry.first_name + " " + entry.middle_name
            ))

        return cleaned_entries

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Endpoint serving list of unprocessed resignees to client (frontend) 
@router.get('/resignees')
async def get_all_unprocessed_resignees():
    try:
        response = supabase.table("ResignedEmployees") \
            .select("*") \
            .is_("processed_date_time", "null") \
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
                print("Decrypting entry:", entry)
                employee_no = decrypt_field(entry['employee_no']) if entry.get('employee_no') else ""
                last_name = decrypt_field(entry['last_name']) if entry.get('last_name') else ""
                first_name = decrypt_field(entry['first_name']) if entry.get('first_name') else ""
                middle_name = decrypt_field(entry['middle_name']) if entry.get('middle_name') else ""
                cost_center = decrypt_field(entry['cost_center']) if entry.get('cost_center') else ""
                position_title = decrypt_field(entry['position_title']) if entry.get('position_title') else ""
                rank = decrypt_field(entry['rank']) if entry.get('rank') else ""
                department = decrypt_field(entry['department']) if entry.get('department') else ""

                cleaned_entries.append(ResigneeDisplay(
                    employee_no=employee_no,
                    date_hired=entry.get('date_hired', ""),
                    cost_center=cost_center,
                    name=f"{last_name}, {first_name} {middle_name}",
                    position_title=position_title,
                    rank=rank,
                    department=department,
                    last_day=entry.get('last_day', ""),
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

# Endpoint to mark resignation entry as processed (will now not be returned to client )

@router.put("/resignees/{employee_no}/process")
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


@router.put("/resignees/{employee_no}/unprocess")
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


@router.get("/resignees/report")
async def get_excel_report(start_date: str, end_date: str):
    """
    Generate an Excel report of processed resignees within a selected timeframe.
    """
    try:
        response = supabase.table("ResignedEmployees") \
            .select("*") \
            .lte("processed_date_time", end_date) \
            .gte("processed_date_time", start_date) \
            .execute()
        
        if response.data and len(response.data) > 0:
            # Decrypt fields for the report if needed
            decrypted_data = []
            for entry in response.data:
                decrypted_data.append({
                    "employee_no": decrypt_field(entry['employee_no']),
                    "last_name": decrypt_field(entry['last_name']),
                    "first_name": decrypt_field(entry['first_name']),
                    "middle_name": decrypt_field(entry['middle_name']),
                    "cost_center": decrypt_field(entry['cost_center']),
                    "position_title": decrypt_field(entry['position_title']),
                    "rank": decrypt_field(entry['rank']),
                    "department": decrypt_field(entry['department']),
                    "date_hired": entry.get('date_hired', ""),
                    "last_day": entry.get('last_day', ""),
                    "processed_date_time": entry.get('processed_date_time', "")
                })
            excel_file = BytesIO()
            generate_report(excel_file, decrypted_data)
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

@router.post("/login")
async def login(response: Response, username: str = Form(...), password: str = Form(...)):
    """
    Login endpoint for Accounts table.
    """
    try:
        db_response = supabase.table("Accounts") \
            .select("*") \
            .eq("username", username) \
            .execute()
        print(db_response)
        if not db_response.data or len(db_response.data) == 0:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        account = db_response.data[0]  
        decrypted_password = decrypt_field(account["password"])

        if password != decrypted_password:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        token_data = {
            "sub": username,
            "exp": datetime.now() + timedelta(hours=12)
        }

        secret_key = os.getenv("JWT_SECRET_KEY")
        if not secret_key:
            raise ValueError("SECRET_KEY not found in environment variables")

        token = jwt.encode(token_data, secret_key, "HS256")
        
        response.set_cookie(
            key="access_token",
            value=f"Bearer {token}",
            httponly=True,
            max_age=3600 * 12,
            secure=False,  # For HTTPS, toggle to True
            samesite="lax"
        )

        print(response.headers)
        
        return {"message": "Login successful"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/accounts")
async def create_account(username: str = Form(...), password: str = Form(...)):
    """
    Create a new account with encrypted password.
    """
    try:
        encrypted_password = encrypt_field(password)
        response = supabase.table("Accounts") \
            .insert({"username": username, "password": encrypted_password}) \
            .execute()
        return {"message": "Account created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
