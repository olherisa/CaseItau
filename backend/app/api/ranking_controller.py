from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas import UserResponse

router = APIRouter(prefix="/ranking", tags=["Ranking"])

@router.get("/", response_model=List[UserResponse])
def get_ranking(limit: int = 10, db: Session = Depends(get_db)):
    """
    Retorna o ranking global de jogadores ordenado pela melhor pontuação.
    """
    repo = UserRepository(db)
    return repo.get_ranking(limit=limit)
