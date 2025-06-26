# place parsing functions and other business logic here

# Parsing function (from raw text from email to labeled data)
from src.schemas import ResigneeCreate, Account
from io import StringIO, BytesIO
import csv
from typing import Sequence, Mapping, Any
import jwt
import os
import xlsxwriter
from datetime import datetime, timedelta

headers = [
    "Employee no.", "Date hired", "Cost center", "Last Name", "First Name", "Middle Name",
    "Position Title", "Rank", "Department", "Last day with AUB", "Date HR Emailed", "Batch Deactivation from UM", "3rd party systems/apps", "E-mails", "Windows", "Remarks", "Processed on"
]

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
                last_day=chunk[9]
            )
            employees.append(employee)
        except Exception:
            continue
    return employees

def generate_csv_report(buffer: StringIO, data: Sequence[Mapping[str, Any]]) -> None:

    writer = csv.DictWriter(buffer, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)

def generate_xls_report(file: BytesIO, data: Sequence[Mapping[str, Any]]) -> None:
    workbook = xlsxwriter.Workbook(file)
    worksheet = workbook.add_worksheet()

    header_format = workbook.add_format({'bold': True})
    late_format = workbook.add_format({'bg_color': "#F9808E"})

    worksheet.write_row(0, 0, headers, header_format)

    i = 1
    try:
        for entry in data:
            
            last_day = entry['Last day with AUB']
            hr = entry['Date HR Emailed']
            um = entry['Batch Deactivation from UM']
            tp = entry['3rd party systems/apps']
            em = entry['E-mails']
            wn = entry['Windows']

            details: list[Any] = [entry['Employee no.'],
            entry['Date hired'],
            entry['Cost center'],
            entry['Last Name'],
            entry['First Name'], 
            entry['Middle Name'],
            entry['Position Title'],
            entry['Rank'],
            entry['Department'],
            last_day,
            hr,
            um,
            tp,
            em,
            wn,
            entry['Remarks'],
            entry['Processed on']]
            worksheet.write_row(i, 0, details)

            for col, (deac, acc) in enumerate([(um, Account.UM), (tp, Account.TP), (em, Account.EM), (wn, Account.WN)], 11):
                if decode_deactivation_date(deac) == "No Existing Account":
                    worksheet.write(i, col, "No Existing Account")
                    continue
                if is_late(last_day, deac, hr, acc):
                    worksheet.write(i, col, deac, late_format)
            i += 1

    except Exception as e:
        print(e)

    worksheet.autofit()
    workbook.close()

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

def decode_deactivation_date(date: str | None) -> str | None:
    if date is None: return ""
    if date < '2020-01-01': return "No Existing Account"
    return date

def is_late(resigned: str, deac: str | None, hr: str, acc: Account) -> bool:
    
    # Tag only if account exists or account has been deactivated
    if (deac and deac > '2020-01-01'): 

        resigned_d = datetime.strptime(resigned, "%Y-%m-%d").date()
        deac_d = datetime.strptime(deac, "%Y-%m-%d").date()
        hr_d = datetime.strptime(hr, "%Y-%m-%d").date()

        match acc:
            case Account.UM:
                # If HR email was delayed
                if (resigned_d < hr_d): return True
                
                # If UM account was deactivated later than last day
                if (resigned_d < deac_d): return True
                
                # Else, on time
                return False
            case _:
                # If employee last day on Friday and deactivated on or before Monday
                if (resigned_d.weekday() == 4 and (deac_d.weekday() == 0 or deac_d.weekday() == 6)): return False

                # If account was deactivated the day after last day of employee
                if (resigned_d + timedelta(days=1)) == deac_d: return False

                # If account was deactivated on or before last day
                if (resigned_d >= deac_d): return False

                # Else, late
                return True
            
    return False
            

