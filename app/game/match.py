from enum import Enum, auto
from app.game.game import Game, Player


class MatchState(Enum):
    CREATED = auto(),
    WAITING = auto(),
    READY = auto(),
    ACTIVE = auto(),
    FINISHED = auto()


class Participant:
    def __init__(self,
                 *,
                 user_id: int | None = None,
                 player: Player | None = None
                 ):
        self.user_id = user_id
        self.player = player


class Match:
    def __init__(self,
                 game: Game,
                 *,
                 participants: set[Participant] = set(),
                 state: MatchState = MatchState.CREATED,
                 winner: Participant | None = None
                 ):
        self.game = game
        self.participants = participants
        self.state = state
        self.winner = winner
