from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException
# from .models import
from fastapi import FastAPI, Depends, HTTPException
from database.database import get_db


def job_details(db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT EnterpriseID, EnterpriseType, Position, City, Clicks, Salary,EnterpriseName,JobID, HiringDepartment FROM Job")
    ).fetchall()
    job_list = []
    for row in result:
        job_list.append({
            "EnterpriseID": row[0],
            "EnterpriseType": row[1],
            "Position": row[2],
            "City": row[3],
            "Clicks": row[4],
            "Salary": row[5],
            "EnterpriseName": row[6],
            "JobID": row[7],
            "HiringDepartment": row[8]
        })
    return {"jobList": job_list}