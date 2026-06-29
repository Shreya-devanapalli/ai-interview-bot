from routers.interview import router as interview_router

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool

from database.db import engine
from database.models import Base

from pathlib import Path
import tempfile
import uuid

from fastapi import Depends
from sqlalchemy.orm import Session

from database.db import get_db
from database.crud import (
    create_interview,
    create_analysis_result
)

from services.analysis_service import run_analysis

# ---------------- APP SETUP ----------------

app = FastAPI()
app.include_router(interview_router)
Base.metadata.create_all(bind=engine)


# ✅ CORS (required for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

