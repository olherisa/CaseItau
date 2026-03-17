from app.api import auth_controller, game_controller, ranking_controller

def include_routers(app):
    app.include_router(auth_controller.router)
    app.include_router(game_controller.router)
    app.include_router(ranking_controller.router)
