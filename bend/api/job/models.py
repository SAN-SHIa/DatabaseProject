from pydantic import BaseModel
from typing import Optional

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from api.login.user.models import Base

class Job(Base):
    __tablename__ = 'Job'
    
    JobID = Column(Integer, primary_key=True, index=True)
    EnterpriseID = Column(Integer, ForeignKey('Enterprise.EnterpriseID'))
    EnterpriseName = Column(String(255))
    EnterpriseType = Column(String(255))
    Email = Column(String(255))
    Phone = Column(String(20))
    Address = Column(String(255))
    PostalCode = Column(String(10))
    Position = Column(String(255))
    Vacancies = Column(Integer)
    City = Column(String(255))
    Description = Column(Text)
    PublishTime = Column(DateTime)
    Clicks = Column(Integer)
    Salary = Column(String(10))
    enterprise = relationship("Enterprise")

class JobCreate(BaseModel):
    enterprise_type: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    postal_code: Optional[str]
    position: str
    vacancies: Optional[int]
    city: str
    description: Optional[str]
    salary: Optional[str]
    hiring_department: Optional[str]