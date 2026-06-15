from dataclasses import dataclass

from models import Card, Player, Rank


@dataclass(frozen=True)
class PlayCardsResult:
    player: Player
    cards: tuple[Card, ...]
    claimed_rank: Rank
    next_player: Player


@dataclass(frozen=True)
class PassChallengeResult:
    player: Player
    next_player: Player


@dataclass(frozen=True)
class ChallengeResult:
    challenger: Player
    challenged_player: Player
    was_bluff: bool
    pile_receiver: Player
    cards_taken: tuple[Card, ...]
    next_player: Player


GameResult = PlayCardsResult | PassChallengeResult | ChallengeResult
