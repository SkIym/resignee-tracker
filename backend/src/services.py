# place parsing functions and other business logic here

# Parsing function (from raw text from email to labeled data)
from schemas import ResigneeCreate
from io import BytesIO
import xlsxwriter
from datetime import datetime
from typing import Sequence, Mapping, Any

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
                employee_no=int(chunk[0]),
                date_hired=chunk[1],
                cost_center=int(chunk[2]),
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

def generate_report(file: BytesIO, data: Sequence[Mapping[str, Any]]) -> None:
    workbook = xlsxwriter.Workbook(file)
    worksheet = workbook.add_worksheet()
    headers = ["Employee no.", "Date hired", "Cost center", "Last Name", "First Name", "Middle Name", "Position Title", "Rank", "Department", "Last day with AUB", "Date processed"]
    worksheet.write_row(0, 0, headers)

    i = 1

    for entry in data:
        details: list[Any] = [entry['employee_no'],
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