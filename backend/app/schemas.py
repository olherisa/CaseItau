from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    best_score: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- Auth Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None

class LoginRequest(BaseModel):
    identifier: str
    password: str

# --- Game Schemas ---
class GuessRequest(BaseModel):
    guess: List[str]  # e.g., ["R", "G", "B", "Y"]

class GuessResponse(BaseModel):
    exact_matches: int
    partial_matches: int
    is_winner: bool
    is_game_over: bool
    attempts_left: int
    score: Optional[int] = None

class GameStartResponse(BaseModel):
    game_id: int
    message: str
    max_attempts: int

class GameHistoryItem(BaseModel):
    guess: List[str]
    exact_matches: int
    partial_matches: int

class GameStatusResponse(BaseModel):
    game_id: int
    is_game_over: bool
    is_winner: bool
    attempts: List[GameHistoryItem]
    secret_code: Optional[List[str]] = None # Only revealed if game over!
    score: Optional[int] = None
