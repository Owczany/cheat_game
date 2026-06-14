from abc import ABC, abstractmethod
from typing import Any, List

from game.game import Game, GameState
from models import Card, Player, Rank


class Agent(ABC):
    def __init__(self, player: Player):
        self.player = player
        self.observations: List[dict[str, Any]] = []

    def observe(self, game: Game) -> dict[str, Any]:
        snapshot = {
            "state": game.state,
            "current_player": game.current_player,
            "own_hand_count": len(self.player.hand),
            "player_card_counts": {
                player.name: len(player.hand)
                for player in game.players
            },
            "table_pile_count": game.table_pile.get_card_count(),
            "current_claimed_rank": game.current_claimed_rank,
            "last_move_player": game.last_move.player if game.last_move else None,
            "last_move_card_count": game.last_move.get_card_count() if game.last_move else 0,
        }
        self.observations.append(snapshot)
        return snapshot

    @abstractmethod
    def choose_cards_to_play(self, game: Game) -> tuple[List[Card], Rank]:
        pass

    @abstractmethod
    def should_challenge(self, game: Game) -> bool:
        pass

    def remember_played_cards(self, cards: List[Card]) -> None:
        pass

    def on_challenge_resolved(self) -> None:
        pass

    def act(self, game: Game) -> None:
        self.observe(game)

        if game.state == GameState.WAITING_FOR_MOVE:
            cards, claimed_rank = self.choose_cards_to_play(game)
            game.play_cards(self.player, cards, claimed_rank)
            self.remember_played_cards(cards)
            return

        if game.state == GameState.WAITING_FOR_CHALLENGE:
            if self.should_challenge(game):
                game.challenge(self.player)
                self.on_challenge_resolved()
            else:
                game.pass_challenge(self.player)
            return

        raise ValueError(f"Agent cannot act while game is in state {game.state}")
