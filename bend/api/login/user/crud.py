from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import text
from .models import UserCreate, EnterpriseCreate, UserLogin, EnterpriseLogin, AdminCreate  # 添加 AdminCreate
from .auth import create_access_token, hash_password, verify_password
from datetime import timedelta  # 添加此行

def register_user(user: UserCreate, db: Session):
    db_user = db.execute(
        text("SELECT * FROM User WHERE Username = :username"),
        {"username": user.username}
    ).fetchone()
    
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db.execute(
        text("INSERT INTO User ( Username, Password, Name, Email) VALUES ( :username, :password, :name, :email)"),
        {
            # "userid": user.userid,
            "username": user.username,
            "password": hash_password(user.password),  # 使用哈希密码
            "name": user.name,
            "email": user.email
        }
    )
    db.commit()
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
        
    return {"message": "User registered successfully", "access_token": access_token, "token_type": "bearer"}

def register_enterprise(enterprise: EnterpriseCreate, db: Session):
    db_enterprise = db.execute(
        text("SELECT * FROM Enterprise WHERE Username = :username"),
        {"username": enterprise.username}
    ).fetchone()
    
    if db_enterprise:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db.execute(
        text("INSERT INTO Enterprise (EnterpriseName, Username, Password, Address, Email) VALUES ( :enterprisename, :username, :password, :address, :email)"),
        {
            # "enterpriseid": enterprise.enterpriseid,
            "enterprisename": enterprise.enterprisename,
            "username": enterprise.username,
            "password": hash_password(enterprise.password),  # 使用哈希密码
            "address": enterprise.address,
            "email": enterprise.email
        }
    )
    db.commit()
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": enterprise.username}, expires_delta=access_token_expires
    )
        
    return {"message": "Enterprise registered successfully", "access_token": access_token, "token_type": "bearer"}

def login_user(user: UserLogin, db: Session):
    db_user = db.execute(
        text("SELECT * FROM User WHERE Username = :username"),
        {"username": user.username}
    ).fetchone()
    
    if not db_user or not verify_password(user.password, db_user.Password):  # 验证密码
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": db_user.Username}, expires_delta=access_token_expires
    )
    
    return {"message": "Login successful", "access_token": access_token, "token_type": "bearer"}

def login_enterprise(enterprise: EnterpriseLogin, db: Session):
    db_enterprise = db.execute(
        text("SELECT * FROM Enterprise WHERE Username = :username"),
        {"username": enterprise.username}
    ).fetchone()
    
    if not db_enterprise or not verify_password(enterprise.password, db_enterprise.Password):  # 验证密码
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": db_enterprise.Username}, expires_delta=access_token_expires
    )
    
    return {"message": "Login successful", "access_token": access_token, "token_type": "bearer"}

def register_admin(admin: AdminCreate, db: Session):
    db_admin = db.execute(
        text("SELECT * FROM Admin WHERE Username = :username"),
        {"username": admin.username}
    ).fetchone()
    
    if db_admin:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db.execute(
        text("INSERT INTO Admin (Username, Password, Name, Email) VALUES (:username, :password, :name, :email)"),
        {
            "username": admin.username,
            "password": hash_password(admin.password),  # 使用哈希密码
            "name": admin.name,
            "email": admin.email
        }
    )
    db.commit()
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": admin.username}, expires_delta=access_token_expires
    )
        
    return {"message": "Admin registered successfully", "access_token": access_token, "token_type": "bearer"}

def login_admin(admin: UserLogin, db: Session):
    db_admin = db.execute(
        text("SELECT * FROM Admin WHERE Username = :username"),
        {"username": admin.username}
    ).fetchone()
    
    if not db_admin or not verify_password(admin.password, db_admin.Password):  # 验证密码
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": db_admin.Username}, expires_delta=access_token_expires
    )
    
    return {"message": "Login successful", "access_token": access_token, "token_type": "bearer"}
