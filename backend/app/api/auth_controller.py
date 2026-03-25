from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.schemas import UserCreate, UserResponse, Token, LoginRequest
from fastapi import Response
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Autenticação"])

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    repo = UserRepository(db)
    return AuthService(repo)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.register_user(user_in)

@router.post("/login")
def login(login_req: LoginRequest, response: Response, auth_service: AuthService = Depends(get_auth_service)):
    token = auth_service.authenticate_user(login_req)
    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        max_age=1800,
        samesite="lax",
        secure=False
    )
    # Return user details without token
    user = auth_service.user_repo.get_user_by_username(login_req.identifier)
    if not user:
        user = auth_service.user_repo.get_user_by_email(login_req.identifier)
    return {"message": "Login successful", "user_id": user.id, "username": user.username}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logout successful"}

@router.get("/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {"user_id": current_user.id, "username": current_user.username}
