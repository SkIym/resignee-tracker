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
    um: str | None
    third_party: str | None
    email: str | None
    windows: str | None
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