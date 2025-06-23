from datetime import date
from xmlrpc.client import _datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from git import Optional
from pydantic import BaseModel, EmailStr, constr
from typing import List, Literal
from sqlmodel import SQLModel, Field, create_engine, Session, select

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class School(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
class Course(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    school_id: int = Field(foreign_key="school.id")
    total_students_enrolled: int = 0
    total_students_waitlisted: int = 0
    total_students_leave: int = 0
class Student(SQLModel, table=True):
    full_name: str
    email: EmailStr
    phone_number: constr(min_length=10, max_length=15)
    city: str
    state: str
    entrance_score: float
    dob: date
    gender:  Literal["Male", "Female"]
    fee: float   

sqlite_url = "sqlite:///./students.db"
engine = create_engine(sqlite_url, echo=True)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/students/")
def create_student(student: Student):
    with Session(engine) as session:
        session.add(student)
        session.commit()
        session.refresh(student)
        return student

class Application(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    course_id: int = Field(foreign_key="course.id")
    application_date: date
    status:  Literal["Pending", "Accepted", "Rejected"] = "Pending"
    
class Score(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id")
    score: float
    test_date: date
    
class EntranceExamSchedule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="course.id")
    datetime: _datetime
    round_no: int

