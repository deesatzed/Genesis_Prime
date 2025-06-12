"""
Database models for Thousand Questions system
Based on schema from PLAN_Notes.md Section 0.2
"""
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    create_engine, Column, String, Text, Boolean, Integer, 
    Float, DateTime, JSON, ARRAY, ForeignKey, UUID
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel, Field

Base = declarative_base()

# SQLAlchemy Models
class TQQuestion(Base):
    __tablename__ = "tq_questions"
    
    id = Column(String, primary_key=True)
    text = Column(Text, nullable=False)
    category = Column(String)
    themes = Column(ARRAY(String))
    complexity = Column(Integer)
    related_ids = Column(ARRAY(String))
    
    # Relationship to answers
    answers = relationship("TQAnswer", back_populates="question")

class TQAnswer(Base):
    __tablename__ = "tq_answers"
    
    user_id = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    question_id = Column(String, ForeignKey("tq_questions.id"), primary_key=True)
    answer_text = Column(Text)
    is_user_answer = Column(Boolean, default=False)
    confidence = Column(Float)
    version = Column(Integer, default=1, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to question
    question = relationship("TQQuestion", back_populates="answers")

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True)
    traits = Column(JSON)  # Big Five + others
    seed_persona = Column(String)  # For option 4
    seed_score = Column(Float)
    updated_at = Column(DateTime, default=datetime.utcnow)

class UserMemory(Base):
    __tablename__ = "user_memories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(ARRAY(Float))  # Vector embedding
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic Models for API
class TraitVector(BaseModel):
    openness: float = Field(ge=0.0, le=1.0)
    conscientiousness: float = Field(ge=0.0, le=1.0) 
    extraversion: float = Field(ge=0.0, le=1.0)
    agreeableness: float = Field(ge=0.0, le=1.0)
    neuroticism: float = Field(ge=0.0, le=1.0)
    
    def pretty(self) -> str:
        """Format traits for prompt inclusion"""
        return f"""
Openness: {self.openness:.2f} - {'High' if self.openness > 0.6 else 'Moderate' if self.openness > 0.4 else 'Low'}
Conscientiousness: {self.conscientiousness:.2f} - {'High' if self.conscientiousness > 0.6 else 'Moderate' if self.conscientiousness > 0.4 else 'Low'}
Extraversion: {self.extraversion:.2f} - {'High' if self.extraversion > 0.6 else 'Moderate' if self.extraversion > 0.4 else 'Low'}
Agreeableness: {self.agreeableness:.2f} - {'High' if self.agreeableness > 0.6 else 'Moderate' if self.agreeableness > 0.4 else 'Low'}
Neuroticism: {self.neuroticism:.2f} - {'High' if self.neuroticism > 0.6 else 'Moderate' if self.neuroticism > 0.4 else 'Low'}
        """.strip()

class TQQuestionModel(BaseModel):
    id: str
    text: str
    category: str
    themes: List[str]
    complexity: int
    related_ids: List[str]

class TQAnswerModel(BaseModel):
    user_id: str
    question_id: str
    answer_text: Optional[str] = None
    is_user_answer: bool = False
    confidence: Optional[float] = None
    version: int = 1

class UserProfileModel(BaseModel):
    user_id: str
    traits: Optional[TraitVector] = None
    seed_persona: Optional[str] = None
    seed_score: Optional[float] = None

class MemoryModel(BaseModel):
    id: Optional[str] = None
    user_id: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None

# Database utilities
def create_database_engine(database_url: str):
    """Create database engine and tables"""
    engine = create_engine(database_url)
    Base.metadata.create_all(bind=engine)
    return engine

def get_session_maker(engine):
    """Get session maker for database operations"""
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)