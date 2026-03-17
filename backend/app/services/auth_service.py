from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate, Token, LoginRequest
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.exceptions import BusinessException

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, user_in: UserCreate) -> User:
        if self.user_repo.get_user_by_email(user_in.email):
            raise BusinessException("Email já registrado.", status_code=400)
        
        if self.user_repo.get_user_by_username(user_in.username):
            raise BusinessException("Nome de usuário já está em uso.", status_code=400)

        hashed_password = get_password_hash(user_in.password)
        user = User(
            username=user_in.username,
            email=user_in.email,
            password_hash=hashed_password
        )
        return self.user_repo.create_user(user)

    def authenticate_user(self, login_req: LoginRequest) -> Token:
        # Check if input is email or username
        user = self.user_repo.get_user_by_email(login_req.username_or_email)
        if not user:
            user = self.user_repo.get_user_by_username(login_req.username_or_email)

        if not user or not verify_password(login_req.password, user.password_hash):
            raise BusinessException("Credenciais inválidas. Verifique seu usuário/email e senha.", status_code=401)

        access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
        return Token(access_token=access_token, token_type="bearer")
