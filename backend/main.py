from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from pathlib import Path
import tempfile
import uuid

from analysis.speech_to_text import transcribe_audio
from analysis.text_analysis import analyze_text
from analysis.audio_analysis import analyze_audio
from feedback.feedback_generator import generate_feedback
from utils.convert_audio import convert_webm_to_wav

# ---------------- APP SETUP ----------------

app = FastAPI()

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
async def analyze_interview(
    audio: UploadFile = File(...),
    eye_contact_score: int = Form(5)
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

    return result
