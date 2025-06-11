# list endpoints here
from fastapi import APIRouter, HTTPException, Body
from schemas import ResigneeDisplay, ResigneeCreate
from services import parse_resignee_text

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
            cleaned_entries.append(ResigneeDisplay(
                **entry.model_dump(exclude={'last_name', 'first_name', 'middle_name'}),
                name= entry.last_name + ", " + entry.first_name + " " + entry.middle_name
            ))

        return cleaned_entries

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Endpoint serving list of unprocessed resignees to client (frontend) 

# Endpoint to mark resignation entry as processed (will now not be returned to client )

# Endpoint serving report of processed resignees within a selected timeframe
