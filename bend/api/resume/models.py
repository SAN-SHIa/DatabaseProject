from pydantic import BaseModel
from typing import Optional

class ResumeUpdate(BaseModel):
    ResumeID: Optional[int] = None
    UserID: Optional[int] = None
    Username: Optional[str] = None
    Gender: Optional[str] = None
    Email: Optional[str] = None
    Phone: Optional[str] = None
    Address: Optional[str] = None
    PostalCode: Optional[str] = None
    Education: Optional[str] = None
    Skills: Optional[str] = None
    JobType: Optional[str] = None
    Position: Optional[str] = None
    City: Optional[str] = None
    Salary: Optional[int] = None
    Introduction: Optional[str] = None
    PublishTime: Optional[str] = None
    Clicks: Optional[int] = None