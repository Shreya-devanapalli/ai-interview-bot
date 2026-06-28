from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db
from database.crud import get_all_interviews

router = APIRouter(
    prefix="",
    tags=["Interview"]
)


@router.get("/interviews")
def get_interviews(
    db: Session = Depends(get_db)
):

    interviews = get_all_interviews(db)

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