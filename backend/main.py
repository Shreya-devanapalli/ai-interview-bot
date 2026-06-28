from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from database.db import engine
from database.models import Base
from pathlib import Path
import tempfile
import uuid

from analysis.speech_to_text import transcribe_audio
from analysis.text_analysis import analyze_text
from analysis.audio_analysis import analyze_audio
from feedback.feedback_generator import generate_feedback
from utils.convert_audio import convert_webm_to_wav

from fastapi import Depends
from sqlalchemy.orm import Session

from database.db import get_db
from database.crud import (
    create_interview,
    create_analysis_result
)

# ---------------- APP SETUP ----------------

app = FastAPI()
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

# ---------------- ANALYSIS LOGIC ----------------

def run_analysis(audio_path: Path, eye_contact_score: int):
    """
    Stable, CPU-safe analysis:
    - Convert WebM → WAV
    - Whisper transcription
    - Text + audio confidence analysis
    - Eye-contact score comes from frontend
    """

    # 🔑 Convert audio first (CRITICAL)
    wav_path = convert_webm_to_wav(audio_path)

    # Transcription
    transcript = transcribe_audio(str(wav_path))

    # Analysis
    text_result = analyze_text(transcript)
    audio_result = analyze_audio(str(wav_path))

    video_result = {
        "eye_contact_score": eye_contact_score
    }

    # Feedback + scoring
    feedback_data = generate_feedback(
        text_result,
        audio_result,
        video_result
    )

    return {
        "transcript": transcript,
        "analysis": {
            "text": text_result,
            "audio": audio_result,
            "video": video_result
        },
        "feedback": feedback_data["remarks"],
        "score": feedback_data["score"]
    }

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