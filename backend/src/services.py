# place parsing functions and other business logic here

# Parsing function (from raw text from email to labeled data)
from schemas import ResigneeCreate
from io import StringIO
import csv
from typing import Sequence, Mapping, Any
import jwt
import os

def parse_resignee_text(raw_text: str) -> list[ResigneeCreate]:
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
                employee_no=chunk[0],
                date_hired=chunk[1],
                cost_center=chunk[2],
                last_name=chunk[3],
                first_name=chunk[4],
                middle_name=chunk[5],
                position_title=chunk[6],
                rank=chunk[7],
                department=chunk[8],
                last_day=chunk[9],
                processed_date_time= None
            )
            employees.append(employee)
        except Exception:
            continue
    return employees

def generate_report(buffer: StringIO, data: Sequence[Mapping[str, Any]]) -> None:

    headers = [
        "Employee no.", "Date hired", "Cost center", "Last Name", "First Name", "Middle Name",
        "Position Title", "Rank", "Department", "Last day with AUB", "Date and Time processed"
    ]

    writer = csv.DictWriter(buffer, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)


async def verify_token(token: str):
    secret_key = os.getenv("JWT_SECRET_KEY")
    if not secret_key:
        raise ValueError("SECRET_KEY not found in environment variables")
    
    # print(jwt.decode(token, secret_key, "HS256"))
    try:
        token_data = jwt.decode(token[7:], secret_key, algorithms=["HS256"]) # Remove "Bearer "
        print(token_data)
        return token_data
    except jwt.PyJWTError as e:
        return None