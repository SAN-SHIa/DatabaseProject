from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.database import get_db
from api.login.user.models import UserCreate, UserLogin, EnterpriseCreate, EnterpriseLogin, EnterpriseInfo, AdminCreate  # 新增导入
from api.login.user.auth import verify_token
from api.login.user.crud import register_user, register_enterprise, login_user, login_enterprise as crud_login_enterprise, register_admin as crud_register_admin, login_admin as crud_login_admin

from api.resume.models import ResumeUpdate
from api.resume.crud import get_resume, create_resume, update_resume

from api.job.crud import job_details
from api.job.models import JobCreate  # 新增导入

from fastapi.middleware.cors import CORSMiddleware

from api.application.models import ApplicationCreate
from api.news.models import NewsCreate  # 新增导入

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 用户相关
@app.post("/register_user/", tags=["用户管理"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)

@app.post("/register_enterprise/", tags=["企业管理"])
def register_enterprise_api(enterprise: EnterpriseCreate, db: Session = Depends(get_db)):
    return register_enterprise(enterprise, db)

@app.post("/login_user/", tags=["用户管理"])
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(user, db)

@app.post("/login_enterprise/", tags=["企业管理"])
def login_enterprise(enterprise: EnterpriseLogin, db: Session = Depends(get_db)):
    return crud_login_enterprise(enterprise, db)

@app.post("/register_admin/", tags=["管理员管理"])
def register_admin(admin: UserCreate, db: Session = Depends(get_db)):
    return crud_register_admin(admin, db)

@app.post("/login_admin/", tags=["管理员管理"])
def login_admin(admin: UserLogin, db: Session = Depends(get_db)):
    try:
        result = crud_login_admin(admin, db)
        if not result:
            raise HTTPException(status_code=400, detail="Invalid username or password")
        return result
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=f"Login failed: {e.detail}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")

@app.get("/users/me", tags=["用户管理"])
def read_users_me(username: str = Depends(verify_token)):
    return {"username": username}

@app.get("/allUsers/", tags=["超级管理员"])
def get_all_users(db: Session = Depends(get_db)):
    query = text("SELECT * FROM User")
    result = db.execute(query).fetchall()
    return [dict(row._asdict()) for row in result]

@app.get("/allEnterprises/", tags=["超级管理员"])
def get_all_enterprises(db: Session = Depends(get_db)):
    query = text("SELECT * FROM Enterprise")
    result = db.execute(query).fetchall()
    return [dict(row._asdict()) for row in result]

@app.delete("/deleteUser/{user_id}", tags=["超级管理员"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    query = text("DELETE FROM User WHERE UserID = :user_id")
    result = db.execute(query, {"user_id": user_id})
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@app.delete("/deleteEnterprise/{enterprise_id}", tags=["超级管理员"])
def delete_enterprise(enterprise_id: int, db: Session = Depends(get_db)):
    query = text("DELETE FROM Enterprise WHERE EnterpriseID = :enterprise_id")
    result = db.execute(query, {"enterprise_id": enterprise_id})
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    return {"message": "Enterprise deleted successfully"}

# 职位相关
@app.get("/jobList/", tags=["职位管理"])
def get_job_list(db: Session = Depends(get_db)):
    return job_details(db)

@app.get("/jobDetail/{job_id}", tags=["职位管理"])
def get_job_details_by_id(job_id: int, db: Session = Depends(get_db)):
    query = text("SELECT * FROM Job WHERE JobID = :job_id")
    result = db.execute(query, {"job_id": job_id}).fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return dict(result._asdict())

@app.get("/apply/{job_id}", tags=["职位管理"])
def get_job_application_details(job_id: int, db: Session = Depends(get_db)):
    query = text("SELECT * FROM Job WHERE JobID = :job_id")
    result = db.execute(query, {"job_id": job_id}).fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return dict(result._asdict())

@app.delete("/manageJob/{job_id}", tags=["超级管理员"])
def delete_job(job_id: int, db: Session = Depends(get_db)):
    query = text("DELETE FROM Job WHERE JobID = :job_id")
    result = db.execute(query, {"job_id": job_id})
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Job deleted successfully"}

@app.post("/incrementClicks/{job_id}", tags=["职位管理"])
def increment_clicks(job_id: int, db: Session = Depends(get_db)):
    query = text("UPDATE Job SET Clicks = Clicks + 1 WHERE JobID = :job_id")
    result = db.execute(query, {"job_id": job_id})
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Clicks incremented successfully"}

# 简历相关
@app.get("/getResume/", tags=["简历管理"])
def get_resume_api(username: str = Depends(verify_token), db: Session = Depends(get_db)):
    query = text("""
        SELECT * FROM ResumeView WHERE Username = :username
    """)
    result = db.execute(query, {"username": username}).fetchone()
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
        return {"resume": resume, "username": username}
    return {"error": "Resume not found", "username": username}

@app.post("/createResume/", tags=["简历管理"])
def create_resume_api(resume: ResumeUpdate, db: Session = Depends(get_db)):
    return create_resume(resume, db)

@app.post("/updateResume/", tags=["简历管理"])
def update_resume_api(resume: ResumeUpdate, db: Session = Depends(get_db)):
    return update_resume(resume, db)

# 新闻相关
@app.get("/newsList/", tags=["新闻管理"])
def get_news_list(db: Session = Depends(get_db)):
    query = text("SELECT * FROM News")
    result = db.execute(query).fetchall()
    return [dict(row._asdict()) for row in result]

@app.get("/news/{news_id}", tags=["新闻管理"])
def get_news_detail(news_id: int, db: Session = Depends(get_db)):
    query = text("SELECT * FROM News WHERE NewsID = :news_id")
    result = db.execute(query, {"news_id": news_id}).fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="News not found")
    return dict(result._asdict())

@app.post("/news/{news_id}/increment_views", tags=["新闻管理"])
def increment_news_views(news_id: int, db: Session = Depends(get_db)):
    query = text("UPDATE News SET Views = Views + 1 WHERE NewsID = :news_id")
    result = db.execute(query, {"news_id": news_id})
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="News not found")
    return {"message": "Views incremented successfully"}

@app.delete("/manageNews/{news_id}", tags=["超级管理员"])
def delete_news(news_id: int, db: Session = Depends(get_db)):
    query = text("DELETE FROM News WHERE NewsID = :news_id")
    result = db.execute(query, {"news_id": news_id})
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="News not found")
    return {"message": "News deleted successfully"}

# 申请相关
@app.get("/myApply/", tags=["申请管理"])
def get_user_applications(username: str = Depends(verify_token), db: Session = Depends(get_db)):
    query = text("""
        SELECT * FROM myApplyView
        WHERE UserID = (SELECT UserID FROM User WHERE Username = :username)
    """)
    result = db.execute(query, {"username": username}).fetchall()
    return [dict(row._asdict()) for row in result]

@app.post("/submitApply/", tags=["申请管理"])
def submit_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    query = text("""
        INSERT INTO Application (UserID, EnterpriseID, Name, EnterpriseName, HiringDepartment, Position, ApplicationDate)
        VALUES (:user_id, :enterprise_id, :name, :enterprise_name, :hiring_department, :position, :application_date)
    """)
    db.execute(query, {
        "user_id": application.UserID,
        "enterprise_id": application.EnterpriseID,
        "name": application.Name,
        "enterprise_name": application.EnterpriseName,
        "hiring_department": application.HiringDepartment,
        "position": application.Position,
        "application_date": application.ApplicationDate
    })
    db.commit()
    return {"message": "Application submitted successfully"}

@app.delete("/revokeApply/{application_id}", tags=["申请管理"])
def revoke_application(application_id: int, db: Session = Depends(get_db)):
    query = text("DELETE FROM Application WHERE ApplicationID = :application_id")
    result = db.execute(query, {"application_id": application_id})
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"message": "Application revoked successfully"}

@app.get("/enterpriseInfo/{username}", tags=["企业信息"])
def get_enterprise_info(username: str, db: Session = Depends(get_db)):
    query = text("SELECT * FROM Enterprise WHERE Username = :username")
    result = db.execute(query, {"username": username}).fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    return dict(result._asdict())

@app.put("/enterpriseInfoUpdate/{username}", tags=["企业信息"])
def update_enterprise_info(username: str, enterprise: EnterpriseInfo, db: Session = Depends(get_db)):
    query = text("""
        UPDATE Enterprise
        SET EnterpriseName = :enterprisename, Address = :address, Email = :email
        WHERE Username = :username
    """)
    result = db.execute(query, {
        "enterprisename": enterprise.enterprisename,
        "address": enterprise.address,
        "email": enterprise.email,
        "username": username
    })
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    return {"message": "Enterprise information updated successfully"}


@app.get("/enterpriseManageApply/", tags=["企业审批"])
def enterprise_get_applications(username: str = Depends(verify_token), db: Session = Depends(get_db)):
    query = text("""
        SELECT * FROM Application
        WHERE EnterpriseID = (SELECT EnterpriseID FROM Enterprise WHERE Username = :username)
    """)
    result = db.execute(query, {"username": username}).fetchall()
    return [dict(row._asdict()) for row in result]


@app.get("/enterpriseCheckResume/{user_id}", tags=["企业审批"])
def enterprise_check_resume(user_id: int, db: Session = Depends(get_db)):
    query = text("SELECT * FROM Resume WHERE UserID = :user_id")
    result = db.execute(query, {"user_id": user_id}).fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Resume not found")
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

@app.post("/enterpriseResponse/{application_id}", tags=["企业审批"])
def enterprise_response(application_id: int, response: dict = Body(...), db: Session = Depends(get_db)):
    query = text("""
        UPDATE Application
        SET ResponseResult = :response_result, EnterpriseMessage = :enterprise_message
        WHERE ApplicationID = :application_id
    """)
    result = db.execute(query, {
        "response_result": response["ResponseResult"],
        "enterprise_message": response["EnterpriseMessage"],
        "application_id": application_id
    })
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"message": "Response updated successfully"}


@app.post("/enterprisePostNews/", tags=["新闻发布"])
def enterprise_post_news(news: NewsCreate, username: str = Depends(verify_token), db: Session = Depends(get_db)):
    query = text("""
        INSERT INTO News (Title, Content, Source, Publish_time)
        VALUES (:title, :content, (SELECT EnterpriseName FROM Enterprise WHERE Username = :username), NOW())
    """)
    db.execute(query, {
        "title": news.title,
        "content": news.content,
        "username": username
    })
    db.commit()
    return {"message": "News posted successfully"}

@app.post("/adminPostNews/", tags=["超级管理员"])
def admin_post_news(news: NewsCreate, db: Session = Depends(get_db)):
    query = text("""
        INSERT INTO News (Title, Content, Source, Publish_time)
        VALUES (:title, :content, '系统管理员', NOW())
    """)
    db.execute(query, {
        "title": news.title,
        "content": news.content
    })
    db.commit()
    return {"message": "News posted successfully"}

@app.post("/enterpriseReleaseJob/", tags=["职位发布"])
def enterprise_release_job(job: JobCreate, username: str = Depends(verify_token), db: Session = Depends(get_db)):
    enterprise_query = text("SELECT EnterpriseID, EnterpriseName FROM Enterprise WHERE Username = :username")
    enterprise_result = db.execute(enterprise_query, {"username": username}).fetchone()
    if enterprise_result is None:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    
    enterprise_id = enterprise_result[0]  # 修改为元组索引
    enterprise_name = enterprise_result[1]  # 修改为元组索引
    
    query = text("""
        INSERT INTO Job (EnterpriseID, EnterpriseName, EnterpriseType, Email, Phone, Address, PostalCode, Position, Vacancies, City, Description, PublishTime, Clicks, Salary, HiringDepartment)
        VALUES (:enterprise_id, :enterprise_name, :enterprise_type, :email, :phone, :address, :postal_code, :position, :vacancies, :city, :description, NOW(), 0, :salary, :hiring_department)
    """)
    db.execute(query, {
        "enterprise_id": enterprise_id,
        "enterprise_name": enterprise_name,
        "enterprise_type": job.enterprise_type,
        "email": job.email,
        "phone": job.phone,
        "address": job.address,
        "postal_code": job.postal_code,
        "position": job.position,
        "vacancies": job.vacancies,
        "city": job.city,
        "description": job.description,
        "salary": job.salary,
        "hiring_department": job.hiring_department
    })
    db.commit()
    return {"message": "Job posted successfully"}

@app.get("/CheckReleasedJob/", tags=["职位管理"])
def get_released_jobs(username: str = Depends(verify_token), db: Session = Depends(get_db)):
    enterprise_query = text("SELECT EnterpriseID FROM Enterprise WHERE Username = :username")
    enterprise_result = db.execute(enterprise_query, {"username": username}).fetchone()
    if enterprise_result is None:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    
    enterprise_id = enterprise_result[0]
    
    job_query = text("SELECT * FROM Job WHERE EnterpriseID = :enterprise_id")
    job_results = db.execute(job_query, {"enterprise_id": enterprise_id}).fetchall()
    return [dict(row._asdict()) for row in job_results]

@app.get("/applicationDetails/", tags=["申请管理"])
def get_application_details(enterprise_name: str, hiring_department: str, position: str, db: Session = Depends(get_db)):
    query = text("""
        SELECT Name, ApplicationDate,ResponseResult FROM Application
        WHERE EnterpriseName = :enterprise_name AND HiringDepartment = :hiring_department AND Position = :position
    """)
    result = db.execute(query, {
        "enterprise_name": enterprise_name,
        "hiring_department": hiring_department,
        "position": position
    }).fetchall()
    return [dict(row._asdict()) for row in result]

@app.put("/updateReleasedJob/{job_id}", tags=["职位发布"])
def update_released_job(job_id: int, job: JobCreate, db: Session = Depends(get_db)):
    query = text("""
        UPDATE Job
        SET EnterpriseType = :enterprise_type, Email = :email, Phone = :phone, Address = :address, PostalCode = :postal_code,
            Position = :position, Vacancies = :vacancies, City = :city, Description = :description, Salary = :salary, HiringDepartment = :hiring_department
        WHERE JobID = :job_id
    """)
    result = db.execute(query, {
        "enterprise_type": job.enterprise_type,
        "email": job.email,
        "phone": job.phone,
        "address": job.address,
        "postal_code": job.postal_code,
        "position": job.position,
        "vacancies": job.vacancies,
        "city": job.city,
        "description": job.description,
        "salary": job.salary,
        "hiring_department": job.hiring_department,
        "job_id": job_id
    })
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Job updated successfully"}

@app.delete("/deleteReleasedJob/{job_id}", tags=["职位发布"])
def delete_released_job(job_id: int, db: Session = Depends(get_db)):
    query = text("DELETE FROM Job WHERE JobID = :job_id")
    result = db.execute(query, {"job_id": job_id})
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Job deleted successfully"}


