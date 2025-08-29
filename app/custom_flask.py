from flask import Flask
from app.services.game_session_manager import GameSessionManager


class CustomFlask(Flask):
    def __init__(self, *args, **kwargs):  # type: ignore
        super().__init__(*args, **kwargs)  # type: ignore
        self.game_sessions: GameSessionManager = GameSessionManager()
