from collections.abc import AsyncGenerator
from datetime import date, datetime
from enum import Enum
from typing import List, Optional
from passlib.context import CryptContext
from fastapi import FastAPI, Depends, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, constr
from sqlalchemy import func
from sqlmodel import SQLModel, Field, select , update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = "sqlite+aiosqlite:///./students.db"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) 

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# FastAPI app and CORS
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()


# Enums
class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"
   

class StatusEnum(str, Enum):
    pending = "Pending"
    accepted = "Accepted"
    rejected = "Rejected"

# Models
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(index=True, unique=True)
    password_hash: str
    



class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    school: str 
    total_students_enrolled: int = Field(default=0, nullable=False)     
    total_students_waitlisted: int = Field(default=0, nullable=False)   
    total_students_leave: int = Field(default=0, nullable=False)

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    phone_number: int = Field(ge=1000000000, le=9999999999)  
    city: str
    state: str
    dob: date
    gender: GenderEnum

class EntranceExamSchedule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="course.id")
    datetime: datetime
    round_no: int

class Application(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    course_id: int = Field(foreign_key="course.id")
    application_date: date
    status: StatusEnum = StatusEnum.pending
    exam_id: int = Field(foreign_key="entranceexamschedule.id")

class Score(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id")
    score: float
    
    
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def update_course_stats(session: AsyncSession):
    
    subquery_enrolled = (
        select(Application.course_id, func.count().label("count"))
        .where(Application.status == "Accepted")
        .group_by(Application.course_id)
        .subquery()
    )

    await session.execute(
        update(Course)
        .where(Course.id == subquery_enrolled.c.course_id)
        .values(total_students_enrolled=subquery_enrolled.c.count)
    )

   
    subquery_waitlisted = (
        select(Application.course_id, func.count().label("count"))
        .where(Application.status == "Pending")
        .group_by(Application.course_id)
        .subquery()
    )

    await session.execute(
        update(Course)
        .where(Course.id == subquery_waitlisted.c.course_id)
        .values(total_students_waitlisted=subquery_waitlisted.c.count)
    )

    
    subquery_rejected = (
        select(Application.course_id, func.count().label("count"))
        .where(Application.status == "Rejected")
        .group_by(Application.course_id)
        .subquery()
    )

    await session.execute(
        update(Course)
        .where(Course.id == subquery_rejected.c.course_id)
        .values(total_students_leave=subquery_rejected.c.count)
    )

    await session.commit()
    
    
# Create tables on startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


# Get all entrance exam schedules 
@router.get("/schedule")
async def get_schedules(session: AsyncSession = Depends(get_session)):
    print("Hello from schedule")
    result = await session.execute(select(EntranceExamSchedule))
    schedules = result.all()

    formatted = []
    for s in schedules:
        formatted.append({
            "title": f"Entrance Exam - Round {s.round_no}",
            "description": (
                f"The entrance exam is scheduled for <strong>{s.datetime.strftime('%d %B')}</strong>. "
                f"Report by <strong>{s.datetime.strftime('%I:%M %p')}</strong>. "
                f"Round <strong>{s.round_no}</strong>."
            )
        })
    return formatted

# Get all applications 
@router.get("/analytics", response_model=List[dict])
async def get_all_applications(session: AsyncSession = Depends(get_session)):
    print("Hello from analytics")
    query = (
        select(Application, Student, Course)
        .join(Student, Student.id == Application.student_id)
        .join(Course, Course.id == Application.course_id)
    )
    results = await session.execute(query)
    rows = results.all()
    

    return [
        {
            "id": app.id,
            "student_id": app.student_id,
            "course_id": app.course_id,
            "application_date": app.application_date,
            "status": app.status,
            "student_name": student.name,
            "city": student.city,
            "gender": student.gender,
            "score": student.entrance_score,
            "course_name": course.name
        }
        for app, student, course in rows
    ]




#For Student 
@router.get("/students/accepted")
async def get_accepted_students(session: AsyncSession = Depends(get_session)):
    query = (
        select(
            Student.id,
            Student.name,
            Student.city,
            Student.state,
            Student.gender,
            Application.status,
            Course.name.label("course_name"),
            Course.school.label("school_name"),
            Score.score.label("score")
        )
        .join(Application, Student.id == Application.student_id)
        .join(Course, Application.course_id == Course.id)
        .join(Score, Application.id == Score.application_id)
        .where(Application.status == "Accepted")
    )

    results = await session.execute(query)
    students = results.all()

    return [
        {
            "id": s.id,
            "name": s.name,
            "city": s.city,
            "state": s.state,
            "gender": s.gender,
            "score": s.entrance_score,
            "course": s.course_name,
            "school": s.school_name
        }
        for s in students
    ]


# 
@router.get("/applications", response_model=list[dict])
async def get_applications(session: AsyncSession = Depends(get_session)):
    query = (
        select(Application, Student.name, Course.name)
        .join(Student, Student.id == Application.student_id)
        .join(Course, Course.id == Application.course_id)
    )
    result = await session.execute(query)
    records = result.all()

    return [
        {
            "application_id": app.id,
            "student_name": student_name,
            "course_name": course_name,
            "status": app.status
        }
        for app, student_name, course_name in records
    ]
    


@router.post("/signup")
async def signup(data: SignupRequest, session: AsyncSession = Depends(get_session)):
    # Check if user already exists
    existing = await session.execute(select(User).where(User.email == data.email))
    if existing.first():
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(email=data.email, password_hash=hash_password(data.password))
    session.add(new_user)
    await session.commit()
    return {"message": "Signup successful"}
    
    
@router.post("/login")
async def login(data: LoginRequest, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(User).where(User.email == data.email)
    )
    user = result.scalar_one_or_none()

    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"message": "Login successful", "user_id": user.id}


app.include_router(router)