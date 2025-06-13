# list endpoints here
from fastapi import APIRouter, HTTPException, Body, Path, Form
from schemas import ResigneeDisplay, ResigneeCreate
from services import parse_resignee_text
from datetime import datetime
from supabase_client import supabase
from io import BytesIO
from fastapi.responses import Response
import xlsxwriter
from datetime import timedelta
from crypto_utils import encrypt_field, decrypt_field

router = APIRouter()

# Endpoint accepting raw text (details) of resignees; will parse and add data to database
@router.post("/resignees", response_model=list[ResigneeDisplay])
async def add_resignees(resignees: str = Body(..., media_type="text/plain")):
    """
    Handle raw resignee details and return parsed data per employee
    """
    print(resignees)
    try:
        entries: list[ResigneeCreate] = parse_resignee_text(resignees)

        cleaned_entries: list[ResigneeDisplay] = []

        for entry in entries:
            
            # For formatting the name field
            cleaned_entries.append(ResigneeDisplay(
                **entry.model_dump(exclude={'last_name', 'first_name', 'middle_name'}),
                name= entry.last_name + ", " + entry.first_name + " " + entry.middle_name
            ))

            to_db = ResigneeCreate(
                **entry.model_dump(exclude={'date_hired', 'last_day'}),
                date_hired=datetime.strptime(entry.date_hired, "%m/%d/%Y").strftime("%Y-%m-%d"),
                last_day=datetime.strptime(entry.last_day, "%m/%d/%Y").strftime("%Y-%m-%d")
            )
            print(to_db)
            supabase.table("ResignedEmployees").insert(to_db.model_dump()).execute()
            
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

            cleaned_entries.append(ResigneeDisplay(
                employee_no=entry['employee_no'],
                date_hired=entry['date_hired'],
                cost_center=entry['cost_center'],
                name= entry['last_name'] + ", " + entry['first_name'] + " " + entry['middle_name'],
                position_title=entry['position_title'],
                rank=entry['rank'],
                department=entry['department'],
                last_day=entry['last_day'],
                processed_date_time=entry['processed_date_time']
            ))

        return cleaned_entries
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint to mark resignation entry as processed (will now not be returned to client )

@router.put("/resignees/{employee_no}/process")
async def mark_resignee_processed(
    employee_no: int = Path(..., description="Employee number to mark as processed")
):
    """
    Mark a resignee as processed by setting the processed_date_time to now.
    """
    try:
        now = datetime.now().isoformat()
        response = supabase.table("ResignedEmployees") \
            .update({"processed_date_time": now}) \
            .eq("employee_no", employee_no) \
            .execute()
        if response.data and len(response.data) > 0:
            return {"message": f"Employee {employee_no} marked as processed.", "processed_date_time": now}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint serving report of processed resignees within a selected timeframe
@router.get("/resignees/report")
async def get_excel_report(start_date: str, end_date: str):

    try:
        response = supabase.table("ResignedEmployees") \
            .select("*") \
            .lte("processed_date_time", end_date) \
            .gte("processed_date_time", start_date) \
            .execute()
        
        if response.data and len(response.data) > 0:
            excel_file = BytesIO()
            workbook = xlsxwriter.Workbook(excel_file)

            worksheet = workbook.add_worksheet()
            headers = ["Employee no.", "Date hired", "Cost center", "Last Name", "First Name", "Middle Name", "Position Title", "Rank", "Department", "Last day with AUB", "Date processed"]

            worksheet.write_row(0, 0, headers)
            i = 1
            for entry in response.data:
                details = [entry['employee_no'],
                entry['date_hired'],
                entry['cost_center'],
                entry['last_name'],
                entry['first_name'], 
                entry['middle_name'],
                entry['position_title'],
                entry['rank'],
                entry['department'],
                entry['last_day'],
                datetime.fromisoformat(entry['processed_date_time'].replace("Z", "+00:00")).strftime("%B %d, %Y %I:%M %p")]
                worksheet.write_row(i, 0, details)
                i += 1

            workbook.close()

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
async def login(username: str = Form(...), password: str = Form(...)):
    """
    Login endpoint for Accounts table.
    """
    try:
        response = supabase.table("Accounts") \
            .select("*") \
            .eq("username", username) \
            .execute()
        if response.data and len(response.data) > 0:
            account = response.data[0]
            decrypted_password = decrypt_field(account["password"])
            if password == decrypted_password:
                return {"message": "Login successful"}
            else:
                return {"message": "Login failed: Invalid username or password"}
        else:
            return {"message": "Login failed: Invalid username or password"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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
