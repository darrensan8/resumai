from fastapi import APIRouter, Depends, Cookie, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Resume, JobDescription, AnalysisScores, ResumeFeedback
from app.services.analysis import analyze_resume
from pydantic import BaseModel

router = APIRouter()

class AnalysisRequest(BaseModel):
    role_level: str = "intern"

@router.post("/analyze")
async def analyze(
    request: AnalysisRequest,
    session_id: str = Cookie(default=None),
    x_session_id: str = None,
    db: Session = Depends(get_db)
):
    effective_session_id = session_id or x_session_id
    if not effective_session_id:
        raise HTTPException(status_code=400, detail="No session found. Please upload a resume first.")

    resume = db.query(Resume).filter(Resume.session_id == effective_session_id).first()
    if not resume:
        raise HTTPException(status_code=400, detail="No resume found. Please upload a resume first.")

    job_desc = db.query(JobDescription).filter(JobDescription.session_id == effective_session_id).first()
    if not job_desc:
        raise HTTPException(status_code=400, detail="No job description found. Please upload a job description first.")

    existing_score = db.query(AnalysisScores).filter(AnalysisScores.session_id == effective_session_id).first()
    if existing_score:
        db.delete(existing_score)

    existing_feedback = db.query(ResumeFeedback).filter(ResumeFeedback.session_id == effective_session_id).first()
    if existing_feedback:
        db.delete(existing_feedback)

    db.commit()

    try:
        analysis = analyze_resume(resume.resume_text, job_desc.job_description, request.role_level)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

    new_score = AnalysisScores(
        session_id=effective_session_id,
        analysis_data=analysis
    )
    db.add(new_score)

    new_feedback = ResumeFeedback(
        session_id=effective_session_id,
        improvements_data=analysis.get("improvements", [])
    )
    db.add(new_feedback)

    db.commit()
    return analysis