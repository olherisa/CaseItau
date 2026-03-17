from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.schemas import UserCreate, UserResponse, Token, LoginRequest

router = APIRouter(prefix="/auth", tags=["Autenticação"])

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    repo = UserRepository(db)
    return AuthService(repo)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.register_user(user_in)

@router.post("/login", response_model=Token)
def login(login_req: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.authenticate_user(login_req)
