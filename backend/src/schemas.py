from pydantic import BaseModel

class ResigneeDisplay(BaseModel):
    employee_no: str
    date_hired: str
    cost_center: str
    name: str
    position_title: str
    rank: str
    department: str 
    last_day: str
    date_hr_emailed: str
    um_date_deac: str | None
    tp_date_deac: str | None
    email_date_deac: str | None
    windows_date_deac: str | None
    remarks: str | None

class ResigneeCreate(BaseModel):
    employee_no: str
    date_hired: str
    cost_center: str
    last_name: str
    first_name: str
    middle_name: str
    position_title: str
    rank: str
    department: str 
    last_day: str