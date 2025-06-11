# place parsing functions and other business logic here


# Parsing function (from raw text from email to labeled data)

from datetime import datetime
from schemas import ResigneeCreate
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase_client import supabase
from datetime import datetime

def parse_resignee_text(raw_text: str):
    """
    Parses raw text input (fields separated by newlines, possibly with blank lines)
    and returns a list of ResigneeCreate objects.
    """
    employees = []
    # Get all non-empty lines
    lines = [line.strip() for line in raw_text.strip().split('\n') if line.strip()]
    # Group every 10 lines as one employee
    for i in range(0, len(lines), 10):
        chunk = lines[i:i+10]
        if len(chunk) < 10:
            continue
        try:
            employee = ResigneeCreate(
                employee_no=int(chunk[0]),
                date_hired=chunk[1],
                cost_center=chunk[2],
                last_name=chunk[3],
                first_name=chunk[4],
                middle_name=chunk[5],
                position_title=chunk[6],
                rank=chunk[7],
                department=chunk[8],
                last_day=chunk[9],
                processed_date= None
            )
            employees.append(employee)
        except Exception:
            continue
    return employees


emp1 = parse_resignee_text(
    """153

    01/15/22

    Cost Center 1

    Doe

    John

    Smith

    Software Engineer

    Senior

    Engineering

    01/15/23
    """
)

# Send each employee to the FastAPI endpoint
for resignee in emp1:
    resignee_dict = resignee.model_dump()
    response = requests.post(
        "http://localhost:8000/ResignedEmployees",  # Change port if needed
        json=resignee_dict
    )
    print(response.status_code, response.json())

def create_item(item: dict):
    try:
        # Format date fields to YYYY-MM-DD
        for date_field in ["date_hired", "last_day"]:
            if item.get(date_field):
                try:
                    # Accept both string and date objects
                    if isinstance(item[date_field], str):
                        dt = datetime.strptime(item[date_field], "%m/%d/%y")
                    else:
                        dt = item[date_field]
                    item[date_field] = dt.strftime("%Y-%m-%d")
                except Exception:
                    item[date_field] = None
        # Ensure processed_date is null if not provided
        if "processed_date" not in item or item["processed_date"] is None:
            item["processed_date"] = None

        response = supabase.table("ResignedEmployees").insert(item).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Encoding data to XCEL file function (for reports)