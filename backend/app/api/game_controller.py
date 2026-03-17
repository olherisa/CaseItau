from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas import GuessRequest, GuessResponse, GameStartResponse, GameStatusResponse
from app.repositories.game_repository import GameRepository
from app.repositories.user_repository import UserRepository
from app.services.game_service import GameService

router = APIRouter(prefix="/games", tags=["Jogo"])

def get_game_service(db: Session = Depends(get_db)) -> GameService:
    game_repo = GameRepository(db)
    user_repo = UserRepository(db)
    return GameService(game_repo, user_repo)

@router.post("/start", response_model=GameStartResponse, status_code=status.HTTP_201_CREATED)
def start_game(
    current_user: User = Depends(get_current_user),
    game_service: GameService = Depends(get_game_service)
):
    """
    Inicia uma nova partida para o usuário autenticado.
    """
    return game_service.start_game(current_user.id)

@router.post("/{game_id}/guess", response_model=GuessResponse)
def make_guess(
    game_id: int,
    guess: GuessRequest,
    current_user: User = Depends(get_current_user),
    game_service: GameService = Depends(get_game_service)
):
    """
    Envia um palpite (guess) para o jogo ativo.
    """
    return game_service.make_guess(game_id, current_user.id, guess)

@router.get("/{game_id}/status", response_model=GameStatusResponse)
def get_status(
    game_id: int,
    current_user: User = Depends(get_current_user),
    game_service: GameService = Depends(get_game_service)
):
    """
    Recupera o estado atual de uma partida.
    """
    return game_service.get_game_status(game_id, current_user.id)
