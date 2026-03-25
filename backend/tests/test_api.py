from fastapi.testclient import TestClient
from tests.conftest import client

def test_register_user():
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data

def test_login_user():
    # Register first
    client.post(
        "/auth/register",
        json={"username": "testuser2", "email": "test2@example.com", "password": "password123"}
    )
    # Login
    response = client.post(
        "/auth/login",
        json={"identifier": "testuser2", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.cookies

def test_start_game():
    client.post("/auth/register", json={"username": "player1", "email": "player1@mail.com", "password": "pass"})
    login_res = client.post("/auth/login", json={"identifier": "player1", "password": "pass"})
    token = login_res.cookies.get("access_token")

    res = client.post("/games/start", cookies={"access_token": token})
    assert res.status_code == 201
    assert "game_id" in res.json()

def test_make_guess():
    client.post("/auth/register", json={"username": "player2", "email": "player2@mail.com", "password": "pass"})
    token = client.post("/auth/login", json={"identifier": "player2", "password": "pass"}).cookies.get("access_token")
    cookies = {"access_token": token}
    
    game = client.post("/games/start", cookies=cookies).json()
    game_id = game["game_id"]

    guess_res = client.post(f"/games/{game_id}/guess", json={"guess": ["R", "R", "G", "B"]}, cookies=cookies)
    assert guess_res.status_code == 200
    data = guess_res.json()
    assert "exact_matches" in data
    assert "partial_matches" in data
