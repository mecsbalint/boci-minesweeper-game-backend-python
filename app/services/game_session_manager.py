from app.game.models import Game


class GameSessionManager():
    def __init__(self):
        self.__sessions = {}

    @property
    def game_sessions(self):
        return self.__sessions

    def add_game(self, user_id: int, game: Game):
        self.__sessions[user_id] = game

    def remove_game(self, user_id: int) -> Game | None:
        return self.__sessions.pop(user_id, None)

    def get_game(self, user_id: int) -> Game | None:
        return self.__sessions.get(user_id)
