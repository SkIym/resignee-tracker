from datetime import datetime, date
from sqlmodel import Field, SQLModel

class Resignee(SQLModel, table=True):
    employee_no: str = Field(primary_key=True)
    date_hired: str = Field(..., description="Date employee was hired")
    cost_center: str = Field(..., description="Cost Center")
    last_name: str = Field(..., description="Last Name")
    first_name: str = Field(..., description="First Name")
    middle_name: str = Field(..., description="Middle Name")
    position_title: str = Field(..., description="Position Title ")
    rank: str = Field(..., description="Rank")
    department: str = Field(..., description="Department")
    last_day: date = Field(..., description="Last Day")
    processed_date_time: datetime = Field(..., description="Date and time accounts were deleted")
    um_date_deac: datetime = Field(..., description="Batch UM Deactivation Date")
    tp_date_deac: datetime = Field(..., description="Third party accounts Deactivation Date")
    email_date_deac: datetime = Field(..., description="Email Deactivate Date")
    windows_date_deac: datetime = Field(..., description="Windows Deactivation Date")
    remarks: str = Field(..., description="Remarks")
    date_hr_emailed: datetime = Field(..., description="Date HR emailed about resignation")

class Account(SQLModel, table=True):
    username: str = Field(primary_key=True)
    password: str = Field(..., description="Password")