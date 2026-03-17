import random
import json
from datetime import datetime, timezone
from app.repositories.game_repository import GameRepository
from app.repositories.user_repository import UserRepository
from app.models.game import Game
from app.schemas import GuessRequest, GuessResponse, GameStartResponse, GameStatusResponse, GameHistoryItem
from app.core.exceptions import BusinessException

# Standard Mastermind Colors
AVAILABLE_COLORS = ["R", "G", "B", "Y", "O", "P"] # Red, Green, Blue, Yellow, Orange, Purple
MAX_ATTEMPTS = 10
CODE_LENGTH = 4

class GameService:
    def __init__(self, game_repo: GameRepository, user_repo: UserRepository):
        self.game_repo = game_repo
        self.user_repo = user_repo

    def _generate_secret_code(self) -> str:
        # Mastermind allows duplicate colors
        code = [random.choice(AVAILABLE_COLORS) for _ in range(CODE_LENGTH)]
        return "".join(code)

    def start_game(self, user_id: int) -> GameStartResponse:
        secret = self._generate_secret_code()
        game = Game(
            user_id=user_id,
            secret_code=secret,
            attempts_matrix="[]", 
            score=0
        )
        created_game = self.game_repo.create_game(game)
        
        return GameStartResponse(
            game_id=created_game.id,
            message="Jogo iniciado! Tente adivinhar a sequência de 4 cores.",
            max_attempts=MAX_ATTEMPTS
        )

    def make_guess(self, game_id: int, user_id: int, guess_req: GuessRequest) -> GuessResponse:
        game = self.game_repo.get_game_by_id(game_id)
        
        if not game:
            raise BusinessException("Jogo não encontrado.", status_code=404)
        if game.user_id != user_id:
            raise BusinessException("Este jogo não pertence a você.", status_code=403)

        attempts = json.loads(game.attempts_matrix)
        
        # Check if already over
        is_winner = len(attempts) > 0 and attempts[-1]["exact_matches"] == CODE_LENGTH
        if is_winner or len(attempts) >= MAX_ATTEMPTS:
            raise BusinessException("Este jogo já foi encerrado.", status_code=400)

        guess_list = guess_req.guess
        if len(guess_list) != CODE_LENGTH:
            raise BusinessException(f"O palpite deve conter exatamente {CODE_LENGTH} cores.", status_code=400)
        for color in guess_list:
            if color not in AVAILABLE_COLORS:
                raise BusinessException(f"Cor inválida. Cores permitidas: {AVAILABLE_COLORS}", status_code=400)

        # Calculate matches
        secret_list = list(game.secret_code)
        guess_copy = list(guess_list)
        
        exact_matches = 0
        partial_matches = 0
        
        # First pass: Exact matches
        for i in range(CODE_LENGTH):
            if guess_copy[i] == secret_list[i]:
                exact_matches += 1
                secret_list[i] = None # Mark as used
                guess_copy[i] = None

        # Second pass: Partial matches (correct color, wrong position)
        for i in range(CODE_LENGTH):
            if guess_copy[i] is not None and guess_copy[i] in secret_list:
                partial_matches += 1
                # Mark as used in secret list to avoid double counting
                secret_list[secret_list.index(guess_copy[i])] = None 
                
        # Register attempt
        new_attempt = {
            "guess": guess_list,
            "exact_matches": exact_matches,
            "partial_matches": partial_matches
        }
        attempts.append(new_attempt)
        game.attempts_matrix = json.dumps(attempts)
        
        is_winner = exact_matches == CODE_LENGTH
        is_game_over = is_winner or len(attempts) >= MAX_ATTEMPTS
        attempts_left = MAX_ATTEMPTS - len(attempts)
        
        if is_game_over:
            # Calculate score: Time + Minimum Attempts is better
            # Basic Score logic for Mastermind:
            # max base = 1000 (if solved in 1 attempt)
            if is_winner:
                base_score = 1000 - (len(attempts) - 1) * 100
                game.score = base_score
                # Update user best score
                self.user_repo.update_best_score(user_id, base_score)
            else:
                game.score = 0
            
            # Calculate duration
            now = datetime.now(timezone.utc)
            # Ensure game.created_at has timezone info before subtraction if needed
            created = game.created_at
            if created.tzinfo is None:
                created = created.replace(tzinfo=timezone.utc)
                
            delta = now - created
            game.duration_seconds = delta.total_seconds()
            
        self.game_repo.update_game(game)

        return GuessResponse(
            exact_matches=exact_matches,
            partial_matches=partial_matches,
            is_winner=is_winner,
            is_game_over=is_game_over,
            attempts_left=attempts_left,
            score=game.score if is_game_over else None
        )

    def get_game_status(self, game_id: int, user_id: int) -> GameStatusResponse:
        game = self.game_repo.get_game_by_id(game_id)
        if not game:
            raise BusinessException("Jogo não encontrado.", status_code=404)
        if game.user_id != user_id:
            raise BusinessException("Acesso negado.", status_code=403)

        attempts = json.loads(game.attempts_matrix)
        is_winner = len(attempts) > 0 and attempts[-1]["exact_matches"] == CODE_LENGTH
        is_game_over = is_winner or len(attempts) >= MAX_ATTEMPTS
        
        history = [GameHistoryItem(**att) for att in attempts]
        
        return GameStatusResponse(
            game_id=game.id,
            is_game_over=is_game_over,
            is_winner=is_winner,
            attempts=history,
            secret_code=list(game.secret_code) if is_game_over else None,
            score=game.score if is_game_over else None
        )
