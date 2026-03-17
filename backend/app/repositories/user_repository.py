from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_best_score(self, user_id: int, new_score: int) -> User | None:
        user = self.get_user_by_id(user_id)
        if user and (user.best_score == 0 or new_score > user.best_score):
            user.best_score = new_score
            self.db.commit()
            self.db.refresh(user)
        return user

    def get_ranking(self, limit: int = 10) -> list[User]:
        # Filter users that have actually played (best_score > 0)
        return self.db.query(User).filter(User.best_score > 0).order_by(User.best_score.desc()).limit(limit).all()
