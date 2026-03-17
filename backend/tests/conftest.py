import os
os.environ["DB_HOST"] = "ignore"
os.environ["DB_PORT"] = "0"
os.environ["DB_USER"] = "ignore"
os.environ["DB_PASSWORD"] = "ignore"
os.environ["DB_NAME"] = "ignore"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.main import app
from fastapi.testclient import TestClient

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override dependency
from app.core.database import get_db
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

import pytest
@pytest.fixture(autouse=True)
def init_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
