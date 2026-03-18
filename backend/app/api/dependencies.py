from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.security import decode_access_token
from app.core.exceptions import BusinessException
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.models.user import User

from fastapi import Request

def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    token = request.cookies.get("access_token")
    payload = decode_access_token(token)
    
    if not payload or "user_id" not in payload:
        raise BusinessException("Token inválido ou expirado.", status_code=401)
        
    user_id = payload.get("user_id")
    repo = UserRepository(db)
    user = repo.get_user_by_id(user_id)
    
    if not user:
        raise BusinessException("Usuário não encontrado.", status_code=401)
        
    return user
