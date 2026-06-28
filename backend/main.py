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

# Temporary directory for uploaded audio
BASE_DIR = Path(tempfile.gettempdir()) / "ai_interview_bot"
BASE_DIR.mkdir(exist_ok=True)


# ---------------- API ENDPOINT ----------------

@app.post("/analyze")
@app.post("/analyze")
async def analyze_interview(
    audio: UploadFile = File(...),
    eye_contact_score: int = Form(5),

    job_role: str = Form("General"),

    question: str = Form(""),

    answer: str = Form(""),

    db: Session = Depends(get_db)
):
    """
    Receives:
    - audio (webm) from frontend
    - eye_contact_score (0–10) computed in browser
    """

    uid = uuid.uuid4().hex
    audio_path = BASE_DIR / f"{uid}_audio.webm"

    # Save uploaded audio
    audio_path.write_bytes(await audio.read())

    # 🔥 Run heavy work in threadpool (no event loop blocking)
    result = await run_in_threadpool(
    run_analysis,
    audio_path,
    eye_contact_score
    )
    
    # ---------------- SAVE INTERVIEW ----------------

    interview = create_interview(
        db=db,
        user_id=None,
        job_role=job_role,
        question=question,
        answer=answer,
        transcript=result["transcript"],
        audio_path=str(audio_path),
        duration=None
    )

    # ---------------- SAVE ANALYSIS ----------------

    create_analysis_result(
        db=db,
        interview_id=interview.id,

        word_count=result["analysis"]["text"]["word_count"],
        sentiment=result["analysis"]["text"]["sentiment"],

        subjectivity=result["analysis"]["text"]["subjectivity"],

        speaking_rate=result["analysis"]["audio"]["speaking_rate"],

        energy=result["analysis"]["audio"]["energy"],

        eye_contact_score=eye_contact_score,

        overall_score=result["score"],

        feedback=result["feedback"]
    )

    return result