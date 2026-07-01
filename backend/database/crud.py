from sqlalchemy.orm import Session

from .models import Interview, AnalysisResult


def create_interview(
    db: Session,
    user_id: int,
    job_role: str,
    question: str,
    answer: str,
    transcript: str,
    audio_path: str,
    duration: float | None = None
):
    interview = Interview(
        user_id=user_id,
        job_role=job_role,
        question=question,
        answer=answer,
        transcript=transcript,
        audio_path=audio_path,
        duration=duration
    )

    db.add(interview)
    db.commit()
    db.refresh(interview)

    return interview


def create_analysis_result(
    db: Session,
    interview_id: int,
    word_count: int,
    sentiment: float,
    subjectivity: float,
    speaking_rate: float,
    energy: float,
    eye_contact_score: int,
    overall_score: float,
    feedback: list[str]
):
    analysis = AnalysisResult(
        interview_id=interview_id,
        word_count=word_count,
        sentiment=sentiment,
        subjectivity=subjectivity,
        speaking_rate=speaking_rate,
        energy=energy,
        eye_contact_score=eye_contact_score,
        overall_score=overall_score,
        feedback="\n".join(feedback)
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis

def get_all_interviews(db: Session):
    return (
        db.query(Interview)
        .order_by(Interview.created_at.desc())
        .all()
    )

def get_user_interviews(
    db: Session,
    user_id: int
):
    return (
        db.query(Interview)
        .filter(Interview.user_id == user_id)
        .order_by(Interview.created_at.desc())
        .all()
    )
    

from .models import User

def get_user_by_email(
    db: Session,
    email: str
):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def create_user(
    db: Session,
    name: str,
    email: str,
    password_hash: str
):
    user = User(
        name=name,
        email=email,
        password_hash=password_hash
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_user_by_id(
    db: Session,
    user_id: int
):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )