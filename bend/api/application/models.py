from pydantic import BaseModel
from datetime import datetime

class ApplicationCreate(BaseModel):
    UserID: int
    EnterpriseID: int
    Name: str
    EnterpriseName: str
    HiringDepartment: str
    Position: str
    ApplicationDate: datetime
