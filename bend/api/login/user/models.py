from sqlalchemy import Column, Integer, String
from database.database import Base, engine
from pydantic import BaseModel
from typing import Optional

class User(Base):
    __tablename__ = "User"
    UserID = Column(Integer, primary_key=True, index=True)
    Username = Column(String(255), unique=True, index=True)
    Password = Column(String(255))
    Name = Column(String(255))
    Email = Column(String(255))

class Enterprise(Base):
    __tablename__ = "Enterprise"
    EnterpriseID = Column(Integer, primary_key=True, index=True)
    EnterpriseName = Column(String(255))
    Username = Column(String(255), unique=True, index=True)
    Password = Column(String(255))
    Address = Column(String(255))
    Email = Column(String(255))

class Admin(Base):
    __tablename__ = "Admin"
    AdminID = Column(Integer, primary_key=True, index=True)
    Username = Column(String(255), unique=True, index=True)
    Password = Column(String(255))
    Name = Column(String(255))
    Email = Column(String(255))

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    # userid: str
    username: str
    password: str
    name: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str

class EnterpriseCreate(BaseModel):
    # enterpriseid: str
    enterprisename: str
    username: str
    password: str
    address: str
    email: str

class EnterpriseLogin(BaseModel):
    username: str
    password: str

class EnterpriseInfo(BaseModel):
    enterprisename: str
    username: Optional[str] = None
    address: str
    email: str

class AdminCreate(BaseModel):
    username: str
    password: str
    name: str
    email: str