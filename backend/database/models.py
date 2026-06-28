from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    Text,
    Float
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, nullable=False)

    password_hash = Column(String, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )

    interviews = relationship(
        "Interview",
        back_populates="user",
        cascade="all, delete-orphan"
    )

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    job_role = Column(String(100), nullable=False)

    question = Column(Text, nullable=False)

    answer = Column(Text, nullable=False)

    transcript = Column(Text)

    audio_path = Column(String(255))
    duration = Column(Float)

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="interviews"
    )

    analysis_result = relationship(
    "AnalysisResult",
    back_populates="interview",
    uselist=False,
    cascade="all, delete-orphan"
)

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)

    interview_id = Column(
        Integer,
        ForeignKey("interviews.id"),
        unique=True,
        nullable=False
    )

    word_count = Column(Integer)

    sentiment = Column(Float)

    subjectivity = Column(Float)

    speaking_rate = Column(Float)

    energy = Column(Float)

    eye_contact_score = Column(Integer)

    overall_score = Column(Float)

    feedback = Column(Text)

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )

    interview = relationship(
        "Interview",
        back_populates="analysis_result"
    )