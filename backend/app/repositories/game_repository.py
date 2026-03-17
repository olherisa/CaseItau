from sqlalchemy.orm import Session
from app.models.game import Game

class GameRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_game_by_id(self, game_id: int) -> Game | None:
        return self.db.query(Game).filter(Game.id == game_id).first()

    def create_game(self, game: Game) -> Game:
        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)
        return game

    def update_game(self, game: Game) -> Game:
        self.db.commit()
        self.db.refresh(game)
        return game
