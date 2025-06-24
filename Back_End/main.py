from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import EmailStr, constr
from sqlmodel import SQLModel, Field, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = "sqlite+aiosqlite:///./students.db"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncSession:
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
    other = "Other"

class StatusEnum(str, Enum):
    pending = "Pending"
    accepted = "Accepted"
    rejected = "Rejected"

# Models
class School(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    school_id: int = Field(foreign_key="school.id")
    total_students_enrolled: int = 0
    total_students_waitlisted: int = 0
    total_students_leave: int = 0

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: EmailStr
    phone_number: constr(min_length=10, max_length=15)
    city: str
    state: str
    entrance_score: float
    dob: date
    gender: GenderEnum
    fee: float

class Application(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    course_id: int = Field(foreign_key="course.id")
    application_date: date
    status: StatusEnum = StatusEnum.pending

class Score(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id")
    score: float
    test_date: date

class EntranceExamSchedule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="course.id")
    datetime: datetime
    round_no: int

# Create tables on startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Root route
@app.post("/")
def home():
    return {"message": "Welcome to the Student Admission System API"}

# Get all entrance exam schedules
@router.get("/schedules")
async def get_schedules(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(EntranceExamSchedule))
    schedules = result.all()

    formatted = []
    for s in schedules:
        formatted.append({
            "title": f"Entrance Exam - Round {s.round_no}",
            "description": (
                f"The entrance exam is scheduled for <strong>{s.datetime.strftime('%d %B')}</strong>. "
                f"Report by <strong>{s.datetime.strftime('%I:%M %p')}</strong>. "
                f"Round <strong>{s.round_no}</strong>. Please carry ID and admit card."
            )
        })
    return formatted

# Get all applications 
@router.get("/applications", response_model=List[dict])
async def get_all_applications(session: AsyncSession = Depends(get_session)):
    query = (
        select(Application, Student, Course)
        .join(Student, Student.id == Application.student_id)
        .join(Course, Course.id == Application.course_id)
    )
    results = await session.exec(query)
    rows = results.all()

    return [
        {
            "id": app.id,
            "student_id": app.student_id,
            "course_id": app.course_id,
            "application_date": app.application_date,
            "status": app.status,
            "student_name": student.full_name,
            "city": student.city,
            "gender": student.gender,
            "score": student.entrance_score,
            "course_name": course.name
        }
        for app, student, course in rows
    ]


app.include_router(router, prefix="/api")

#For Student 
@router.get("/api/students/accepted")
async def get_accepted_students(session: AsyncSession = Depends(get_session)):
    query = (
        select(
            Student.id,
            Student.full_name,
            Student.city,
            Student.state,
            Student.gender,
            Student.entrance_score,
            Application.status,
            Course.name.label("course_name"),
            School.name.label("school_name")
        )
        .join(Application, Student.id == Application.student_id)
        .join(Course, Application.course_id == Course.id)
        .join(School, Course.school_id == School.id)
        .where(Application.status == "Accepted")
    )

    results = await session.exec(query)
    students = results.all()

    return [
        {
            "id": s.id,
            "name": s.full_name,
            "city": s.city,
            "state": s.state,
            "gender": s.gender,
            "score": s.entrance_score,
            "course": s.course_name,
            "school": s.school_name
        }
        for s in students
    ]

@router.get("/applications", response_model=list[dict])
async def get_applications(session: AsyncSession = Depends(get_session)):
    query = (
        select(Application, Student.full_name, Course.name)
        .join(Student, Student.id == Application.student_id)
        .join(Course, Course.id == Application.course_id)
    )
    result = await session.exec(query)
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