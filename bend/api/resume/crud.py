from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException
from .models import ResumeUpdate

def get_resume(username: str, db: Session):
    result = db.execute(
        text("SELECT * FROM Resume WHERE Username = :username"), {"username": username}
    ).fetchone()
    if result:
        resume = {
            "ResumeID": result[0],
            "UserID": result[1],
            "Username": result[2],
            "Gender": result[3],
            "Email": result[4],
            "Phone": result[5],
            "Address": result[6],
            "PostalCode": result[7],
            "Education": result[8],
            "Skills": result[9],
            "JobType": result[10],
            "Position": result[11],
            "City": result[12],
            "Salary": result[13],
            "Introduction": result[14],
            "PublishTime": result[15],
            "Clicks": result[16]
        }
        return {"resume": resume}
    return {"error": "Resume not found"}

def create_resume(resume: ResumeUpdate, db: Session):
    user_result = db.execute(
        text("SELECT UserID FROM User WHERE Username = :username"), {"username": resume.Username}
    ).fetchone()
    if not user_result:
        raise HTTPException(status_code=404, detail="User not found")
    
    resume.UserID = user_result[0]
    
    result = db.execute(
        text("""
            INSERT INTO Resume (
                UserID, Username, Gender, Email, Phone, Address, PostalCode, 
                Education, Skills, JobType, Position, City, Salary, Introduction, 
                PublishTime, Clicks
            ) VALUES (
                :UserID, :Username, :Gender, :Email, :Phone, :Address, :PostalCode, 
                :Education, :Skills, :JobType, :Position, :City, :Salary, :Introduction, 
                :PublishTime, :Clicks
            )
        """), resume.dict()
    )
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=400, detail="Failed to create resume")
    return {"message": "Resume created successfully"}

def update_resume(resume: ResumeUpdate, db: Session):
    result = db.execute(
        text("""
            UPDATE Resume SET 
                Username = :Username,
                Gender = :Gender,
                Email = :Email,
                Phone = :Phone,
                Address = :Address,
                PostalCode = :PostalCode,
                Education = :Education,
                Skills = :Skills,
                JobType = :JobType,
                Position = :Position,
                City = :City,
                Salary = :Salary,
                Introduction = :Introduction,
                PublishTime = :PublishTime,
                Clicks = :Clicks
            WHERE ResumeID = :ResumeID
        """), resume.dict()
    )
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Resume not found")
    return {"message": "Resume updated successfully"}