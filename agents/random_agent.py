import random
from typing import List

from .agent import Agent
from game.game import Game
from models import Card, Player, Rank


class RandomAgent(Agent):
    def __init__(self, player: Player, rng: random.Random | None = None):
        super().__init__(player)
        self.rng = rng or random.Random()

    def choose_cards_to_play(self, game: Game) -> tuple[List[Card], Rank]:
        if not self.player.hand:
            raise ValueError(f"{self.player.name} has no cards to play")

        card_count = self.rng.randint(1, min(4, len(self.player.hand)))
        cards = self.rng.sample(self.player.hand, card_count)
        min_rank = game.current_claimed_rank or min(Rank)
        legal_ranks = [rank for rank in Rank if rank >= min_rank]
        claimed_rank = self.rng.choice(legal_ranks)

        return cards, claimed_rank

    def should_challenge(self, game: Game) -> bool:
        return self.rng.choice([True, False])
