from collections import Counter
from typing import List

from .agent import Agent
from game.game import Game
from models import Card, Player, Rank


class BalancedAgent(Agent):
    def __init__(self, player: Player):
        super().__init__(player)

    def choose_cards_to_play(self, game: Game) -> tuple[List[Card], Rank]:
        if not self.player.hand:
            raise ValueError(f"{self.player.name} has no cards to play")

        min_rank = game.current_claimed_rank or min(Rank)
        legal_ranks = [rank for rank in self._rank_counts() if rank >= min_rank]

        if legal_ranks:
            chosen_rank = max(legal_ranks, key=lambda rank: (self._rank_counts()[rank], -rank))
            cards = [card for card in self.player.hand if card.rank == chosen_rank]
            return cards, chosen_rank

        lowest_rank = min(card.rank for card in self.player.hand)
        cards = [card for card in self.player.hand if card.rank == lowest_rank]
        return cards, min_rank

    def should_challenge(self, game: Game) -> bool:
        if not game.last_move or game.last_move.player == self.player:
            return False

        known_count = self._known_rank_count(game.last_move.claimed_rank)
        if game.last_move.get_card_count() + known_count > 4:
            return True

        return game.last_move.get_card_count() >= 3 and known_count >= 1

    def _rank_counts(self) -> Counter[Rank]:
        return Counter(card.rank for card in self.player.hand)

    def _known_rank_count(self, rank: Rank) -> int:
        known_cards = self.player.hand + self.played_cards
        return sum(1 for card in known_cards if card.rank == rank)
