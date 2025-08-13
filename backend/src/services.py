# place parsing functions and other business logic here

# Parsing function (from raw text from email to labeled data)
from src.schemas import ResigneeCreate, Account, Status
from io import StringIO, BytesIO
import csv
from typing import Sequence, Mapping, Any
import jwt
import os
import xlsxwriter
from datetime import datetime, timedelta, date

headers = [
    "Employee no.", "Date hired", "Cost center", "Last Name", "First Name", "Middle Name",
    "Position Title", "Rank", "Department", "Last day with AUB", "Date HR Emailed", "Batch Deactivation from UM", "3rd party systems/apps", "E-mails", "Windows", "Remarks", "Status", "Processed on"
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
    processed_format = workbook.add_format({'bg_color': "#2BFF00", 'bold': True})
    unprocessed_format = workbook.add_format({'bg_color': "#FF5500", 'bold': True})

    worksheet.write_row(0, 0, headers, header_format)

    i = 1
    try:
        for entry in data:
            
            last_day: date = entry['Last day with AUB']
            hr: datetime = entry['Date HR Emailed']
            um: date = entry['Batch Deactivation from UM']
            tp: date = entry['3rd party systems/apps']
            em: date = entry['E-mails']
            wn: date = entry['Windows']
            processed = entry["Status"]

            details: list[Any] = [entry['Employee no.'],
            entry['Date hired'],
            entry['Cost center'],
            entry['Last Name'],
            entry['First Name'], 
            entry['Middle Name'],
            entry['Position Title'],
            entry['Rank'],
            entry['Department'],
            last_day.strftime("%Y-%m-%d"),
            hr.date(),
            um.strftime("%Y-%m-%d"),
            tp.strftime("%Y-%m-%d"),
            em.strftime("%Y-%m-%d"),
            wn.strftime("%Y-%m-%d"),
            entry['Remarks']]
            worksheet.write_row(i, 0, details)

            # Marking if late
            for col, (deac, acc) in enumerate([(um, Account.UM), (tp, Account.TP), (em, Account.EM), (wn, Account.WN)], 11):
                if decode_deactivation_date(deac) == "No Existing Account":
                    worksheet.write(i, col, "No Existing Account")
                    continue
                if is_late(last_day, deac, hr, acc):
                    worksheet.write(i, col, deac, late_format)
            
            # Marking if processed 
            if processed == Status.PROCESSED:
                worksheet.write(i, 16, processed, processed_format)
                worksheet.write(i, 17, entry["Processed on"])
            else:
                worksheet.write(i, 16, processed, unprocessed_format)

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

def decode_deactivation_date(date: date | None) -> str | None:
    if date is None: return ""

    date_str = date.strftime("%Y-%m-%d")

    if date_str < '2020-01-01': return "No Existing Account"
    return date_str

def is_late(resigned: date, deac: date | None, hr: datetime, acc: Account) -> bool:
    # Tag only if account exists or account has been deactivated
    if deac and deac > date(2020, 1, 1): 
        resigned_d = resigned
        deac_d = deac
        hr_d = hr.date()

        match acc:
            case Account.UM:
                # If HR email was delayed
                if resigned_d < hr_d:
                    return True
                
                # If UM account was deactivated later than last day
                if resigned_d < deac_d:
                    return True
                
                return False

            case _:
                # If employee's last day was Friday and deactivated on or before Monday
                if resigned_d.weekday() == 4 and deac_d.weekday() in (6, 0):
                    return False

                # If account was deactivated the day after last day of employee
                if resigned_d + timedelta(days=1) == deac_d:
                    return False

                # If account was deactivated on or before last day
                if resigned_d >= deac_d:
                    return False

                return True

    return False
            

