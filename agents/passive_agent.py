from collections import Counter
from typing import List

from .agent import Agent
from game.game import Game
from models import Card, Player, Rank


class PassiveAgent(Agent):
    def __init__(self, player: Player):
        super().__init__(player)
        self.played_cards: List[Card] = []

    def choose_cards_to_play(self, game: Game) -> tuple[List[Card], Rank]:
        if not self.player.hand:
            raise ValueError(f"{self.player.name} has no cards to play")

        min_rank = game.current_claimed_rank or min(Rank)
        honest_ranks = sorted({card.rank for card in self.player.hand if card.rank >= min_rank})

        if honest_ranks:
            chosen_rank = honest_ranks[0]
            cards = [card for card in self.player.hand if card.rank == chosen_rank]
            return cards, chosen_rank

        lowest_rank = min(card.rank for card in self.player.hand)
        cards = [card for card in self.player.hand if card.rank == lowest_rank]
        return cards, min_rank

    def should_challenge(self, game: Game) -> bool:
        if not game.last_move or game.last_move.player == self.player:
            return False

        known_count = self._known_rank_count(game.last_move.claimed_rank)
        return game.last_move.get_card_count() + known_count > 4

    def remember_played_cards(self, cards: List[Card]) -> None:
        self.played_cards.extend(cards)

    def on_challenge_resolved(self) -> None:
        self.played_cards.clear()

    def _known_rank_count(self, rank: Rank) -> int:
        known_cards = self.player.hand + self.played_cards
        rank_counts = Counter(card.rank for card in known_cards)
        return rank_counts[rank]
