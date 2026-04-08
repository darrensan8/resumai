from sqlalchemy import Column, String, Text, LargeBinary, JSON
from app.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    session_id = Column(String, primary_key=True, index=True)
    resume_text = Column(Text, nullable=False)
    resume_data = Column(LargeBinary, nullable=False)

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    session_id = Column(String, primary_key=True, index=True)
    job_description = Column(Text, nullable=False)

class AnalysisScores(Base):
    __tablename__ = "analysis_scores"

    session_id = Column(String, primary_key=True, index=True)
    analysis_data = Column(JSON, nullable=False)

class ResumeFeedback(Base):
    __tablename__ = "resume_feedback"

    session_id = Column(String, primary_key=True, index=True)
    improvements_data = Column(JSON, nullable=False)