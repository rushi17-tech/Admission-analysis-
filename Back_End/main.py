from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import EmailStr, constr
from sqlmodel import SQLModel, Field, select, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# ---------- DATABASE SETUP ----------
DATABASE_URL = "sqlite+aiosqlite:///./students.db"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

# ---------- FASTAPI APP ----------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- ENUMS ----------
class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class StatusEnum(str, Enum):
    pending = "Pending"
    accepted = "Accepted"
    rejected = "Rejected"

# ---------- MODELS ----------
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

# ---------- STARTUP ----------
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# ---------- ROUTES ----------
@app.post("/")
def home():
    return {"message": "Welcome to the Student Admission System API"}

@app.get("/api/schedules")
async def get_schedules(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(EntranceExamSchedule))
    schedules = result.all()

    # Format the output for front-end
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
