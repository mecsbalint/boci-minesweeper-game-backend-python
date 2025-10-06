from enum import Enum, auto
from uuid import UUID
from app.game.game import Game, Player


class MatchState(Enum):
    CREATED = auto(),
    WAITING = auto(),
    READY = auto(),
    ACTIVE = auto(),
    FINISHED = auto()


class Participant:
    def __init__(self,
                 user_id: int,
                 player: Player
                 ):
        self.user_id = user_id
        self.player = player


class Match:
    def __init__(self,
                 game: Game,
                 *,
                 id: UUID | None = None,
                 participants: set[Participant] = set(),
                 state: MatchState = MatchState.CREATED,
                 winner: Participant | None = None,
                 version: int = 0,
                 match_owner: int | None = None
                 ):
        self.game = game
        self.id = id
        self.participants = participants
        self.state = state
        self.winner = winner
        self.version = version
        self.match_owner = match_owner
