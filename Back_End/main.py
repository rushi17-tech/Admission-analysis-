from collections.abc import AsyncGenerator
from datetime import date, datetime
from enum import Enum
from typing import Optional, List

from fastapi import FastAPI, Depends, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy import func, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Field, select
import pathlib

# ────────────── DATABASE ──────────────
BASE_DIR = pathlib.Path(__file__).resolve().parent
DB_FILE  = BASE_DIR / "students.db"
SQLALCHEMY_URL = f"sqlite+aiosqlite:///{DB_FILE}"

engine = create_async_engine(SQLALCHEMY_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
# ──────────────────────────────────────

app = FastAPI()

# ─────────────── CORS ────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ──────────────────────────────────────

# ─────────── ENUMS ───────────
class GenderEnum(str, Enum):
    male   = "Male"
    female = "Female"

class StatusEnum(str, Enum):
    pending  = "pending"
    accepted = "accepted"
    rejected = "rejected"
# ────────────────────────────

# ─────────── MODELS ──────────
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr   = Field(index=True, unique=True)
    password_hash: str

class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    school: str
    total_students_enrolled:   int = Field(default=0, nullable=False)
    total_students_waitlisted: int = Field(default=0, nullable=False)
    total_students_leave:      int = Field(default=0, nullable=False)

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    phone_number: int = Field(ge=1_000_000_000, le=9_999_999_999)
    city: str
    state: str
    dob: date
    gender: GenderEnum

class EntranceExamSchedule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="course.id")
    datetime:  datetime
    round_no:  int

class Application(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    course_id:  int = Field(foreign_key="course.id")
    application_date: date
    status: StatusEnum = StatusEnum.pending
    exam_id: int = Field(foreign_key="entranceexamschedule.id")

class Score(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id")
    score: float
# ────────────────────────────

# ────── AUTH HELPERS ──────
class SignupRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(pwd: str)      -> str:  return pwd_context.hash(pwd)
def verify_password(p, hp) -> bool:        return pwd_context.verify(p, hp)
# ──────────────────────────

router = APIRouter()                       # no prefix here

# ───────── PUBLIC ROUTES ─────────
@router.get("/schedule")
async def get_schedules(session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(EntranceExamSchedule))
    items = res.scalars().all()
    return [
        {
            "title": f"Entrance Exam - Round {i.round_no}",
            "description": (
                f"The entrance exam is scheduled for "
                f"<strong>{i.datetime.strftime('%d %B')}</strong>. "
                f"Report by <strong>{i.datetime.strftime('%I:%M %p')}</strong>. "
                f"Round <strong>{i.round_no}</strong>."
            ),
        }
        for i in items
    ]

# ---------- HOME /analytics (kept exactly as before) ----------
@router.get("/analytics", response_model=list[dict])
async def get_analytics(session: AsyncSession = Depends(get_session)):
    """
    Return one row per application, joined with student, course and (optionally) score.
    This powers the Home tab, so its shape is unchanged.
    """
    query = (
        select(
            Application.id,
            Application.status,
            Application.application_date,
            Student.name.label("student_name"),
            Student.city,
            Student.gender,
            Course.name.label("course_name"),
            Score.score
        )
        .join(Student, Student.id == Application.student_id)
        .join(Course,  Course.id  == Application.course_id)
        .outerjoin(Score, Score.application_id == Application.id)
    )
    results = await session.execute(query)
    return [
        {
            "id": row.id,
            "status": row.status.value,
            "application_date": row.application_date.isoformat(),
            "student_name": row.student_name,
            "city": row.city,
            "gender": row.gender.value,
            "course_name": row.course_name,
            "score": row.score if row.score is not None else None,
        }
        for row in results.all()
    ]

# ---------- NEW: all students ----------
@router.get("/students", response_model=list[dict])
async def get_students(session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Student))
    students = res.scalars().all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "phone_number": s.phone_number,
            "city": s.city,
            "state": s.state,
            "dob": s.dob.isoformat(),
            "gender": s.gender.value,
        }
        for s in students
    ]

# ---------- NEW: all applications ----------
@router.get("/applications", response_model=list[dict])
async def get_applications(session: AsyncSession = Depends(get_session)):
    q = (
        select(Application, Student, Course, Score.score)
        .join(Student, Student.id == Application.student_id)
        .join(Course,  Course.id  == Application.course_id)
        .outerjoin(Score, Score.application_id == Application.id)
    )
    res = await session.execute(q)
    return [
        {
            "application_id": a.id,
            "application_date": a.application_date.isoformat(),
            "status": a.status.value,
            "student_id": s.id,
            "student_name": s.name,
            "course_name": c.name,
            "school_name": c.school,
            "score": scr,
        }
        for a, s, c, scr in res.all()
    ]

# ---------- ACCEPTED students ----------
@router.get("/students/accepted")
async def get_accepted_students(session: AsyncSession = Depends(get_session)):
    q = (
        select(
            Student.id,
            Student.name,
            Student.city,
            Student.state,
            Student.gender,
            Course.name.label("course_name"),
            Course.school.label("school_name"),
            Score.score
        )
        .join(Application, Student.id == Application.student_id)
        .join(Course, Course.id == Application.course_id)
        .join(Score, Application.id == Score.application_id)
        .where(Application.status == StatusEnum.accepted)
    )
    res = await session.execute(q)
    return [
        {
            "id": i.id,
            "name": i.name,
            "city": i.city,
            "state": i.state,
            "gender": i.gender.value,
            "course": i.course_name,
            "school": i.school_name,
            "score": i.score,
        }
        for i in res.all()
    ]

# ---------- STATUS‑filtered applications ----------
@router.get("/applications/status/{status}", response_model=list[dict])
async def get_by_status(status: StatusEnum, session: AsyncSession = Depends(get_session)):
    q = (
        select(Application, Student, Course)
        .join(Student, Student.id == Application.student_id)
        .join(Course, Course.id == Application.course_id)
        .where(Application.status == status)
    )
    res = await session.execute(q)
    return [
        {
            "application_id": a.id,
            "application_date": a.application_date.isoformat(),
            "status": a.status.value,
            "student_id": s.id,
            "student_name": s.name,
            "email": s.email,
            "phone_number": s.phone_number,
            "city": s.city,
            "state": s.state,
            "gender": s.gender.value,
            "course_name": c.name,
            "school_name": c.school,
        }
        for a, s, c in res.all()
    ]

# ---------- AUTH ROUTES ----------
@router.post("/signup")
async def signup(data: SignupRequest, session: AsyncSession = Depends(get_session)):
    if (await session.execute(select(User).where(User.email == data.email))).first():
        raise HTTPException(status_code=400, detail="User already exists")
    session.add(User(email=data.email, password_hash=hash_password(data.password)))
    await session.commit()
    return {"message": "Signup successful"}

@router.post("/login")
async def login(data: LoginRequest, session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(User).where(User.email == data.email))
    user = res.scalar_one_or_none()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": user.id}
# ─────────────────────────

# ───── STARTUP: create tables ─────
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
# ──────────────────────────────────

# ─────── MOUNT ROUTES ───────
app.include_router(router)            # root paths  (e.g. /students)
app.include_router(router, prefix="/api")  # same under /api/...
# ────────────────────────────
