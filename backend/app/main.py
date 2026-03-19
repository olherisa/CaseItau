from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.exceptions import setup_exception_handlers

# Don't create tables on import, handled by migration/scripts
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mastermind API",
    description="API para o jogo Mastermind - Desenvolvido em FastAPI com Python",
    version="1.0.0"
)

# CORS configs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"], # Explicit origin for credentials
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api import include_routers

setup_exception_handlers(app)
include_routers(app)

@app.get("/health")
def health_check():
    return {"status": "ok"}
