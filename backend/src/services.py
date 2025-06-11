# place parsing functions and other business logic here

# Parsing function (from raw text from email to labeled data)
from schemas import ResigneeCreate

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
                processed_date_time= None
            )
            employees.append(employee)
        except Exception:
            continue
    return employees
