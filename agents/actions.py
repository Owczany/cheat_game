from dataclasses import dataclass
from enum import Enum

from game.results import GameResult
from models import Player


class ActionType(Enum):
    PLAY_CARDS = "play_cards"
    CHALLENGE = "challenge"
    PASS_CHALLENGE = "pass_challenge"


@dataclass(frozen=True)
class ActionResult:
    player: Player
    action_type: ActionType
    game_result: GameResult
