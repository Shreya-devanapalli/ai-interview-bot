from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form
)

from fastapi.concurrency import run_in_threadpool

from sqlalchemy.orm import Session

from pathlib import Path
import tempfile
import uuid

from database.db import get_db

from database.crud import (
    get_user_interviews,
    create_interview,
    create_analysis_result
)

from services.analysis_service import run_analysis
from auth.dependencies import get_current_user
from database.models import User

router = APIRouter(
    prefix="",
    tags=["Interview"]
)

BASE_DIR = Path(tempfile.gettempdir()) / "ai_interview_bot"
BASE_DIR.mkdir(exist_ok=True)


@router.post("/analyze")
async def analyze_interview(
    audio: UploadFile = File(...),
    eye_contact_score: int = Form(5),

    job_role: str = Form("General"),

    question: str = Form(""),

    answer: str = Form(""),

    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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
        user_id=current_user.id,
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

@router.get("/interviews")
def get_interviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    interviews = get_user_interviews(
    db,
    current_user.id
)

    results = []

    for interview in interviews:

        score = None

        if interview.analysis_result:
            score = interview.analysis_result.overall_score

        results.append({
            "id": interview.id,
            "job_role": interview.job_role,
            "score": score,
            "created_at": interview.created_at,
            "transcript": interview.transcript
        })

    return results

