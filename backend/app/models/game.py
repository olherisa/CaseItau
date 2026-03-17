from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.sql import func
from app.core.database import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    secret_code = Column(String(4), nullable=False)
    attempts_matrix = Column(Text, default="[]")  # Store as a JSON string to avoid DB locking dependencies
    score = Column(Integer, default=0)
    duration_seconds = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
