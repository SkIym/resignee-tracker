# list endpoints here
from fastapi import APIRouter, HTTPException, Body
from schemas import ResigneeDisplay, ResigneeCreate
from services import parse_resignee_text
from datetime import datetime
from supabase_client import supabase

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
                date_hired=datetime.strptime(entry.date_hired, "%m/%d/%y").strftime("%Y-%m-%d"),
                last_day=datetime.strptime(entry.last_day, "%m/%d/%y").strftime("%Y-%m-%d")
            )
            print(to_db)
            supabase.table("ResignedEmployees").insert(to_db.model_dump()).execute()
            
        return cleaned_entries

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Endpoint serving list of unprocessed resignees to client (frontend) 
@router.get('/resignees')
async def get_all_resignees():
    try:
        response = supabase.table("ResignedEmployees").select("*").execute()

        cleaned_entries: list[ResigneeDisplay] = []

        for entry in response.data:

            cleaned_entries.append(ResigneeDisplay(
                employee_no=entry['employee_no'],
                date_hired=entry['date_hired'],
                cost_center=entry['cost_center'],
                name= entry['last_name'] + ", " + entry['first_name'] + " " + entry['middle_name'],
                position_title=entry['position_title'],
                rank=entry['rank'],
                department=entry['department'],
                last_day=entry['last_day'],
                processed_date=entry['processed_date']
            ))

        return cleaned_entries
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint to mark resignation entry as processed (will now not be returned to client )

# Endpoint serving report of processed resignees within a selected timeframe
