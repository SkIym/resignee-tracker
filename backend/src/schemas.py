from pydantic import BaseModel

class ResigneeDisplay(BaseModel):
    employee_no: int
    date_hired: str
    cost_center: str
    name: str
    position_title: str
    rank: str
    department: str 
    last_day: str
    processed_date: str | None

class ResigneeCreate(BaseModel):
    employee_no: int
    date_hired: str
    cost_center: str
    last_name: str
    first_name: str
    middle_name: str
    position_title: str
    rank: str
    department: str 
    last_day: str
    processed_date: str | None