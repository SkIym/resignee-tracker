from pydantic import BaseModel
from enum import Enum
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
    um_late: bool
    third_party_late: bool
    email_late: bool
    windows_late: bool
    processed_date_time: str | None

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

class EditDate(BaseModel):
    message: str
    date: str
    late: bool
class Account(Enum):
    UM = 1
    TP = 2
    EM = 3
    WN = 4