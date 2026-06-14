import random
from typing import List

from .agent import Agent
from game.game import Game
from models import Card, Player, Rank


class AggressiveAgent(Agent):
    def __init__(
        self,
        player: Player,
        rng: random.Random | None = None,
        bluff_probability: float = 0.65,
        challenge_probability: float = 0.65,
    ):
        super().__init__(player)
        self.rng = rng or random.Random()
        self.bluff_probability = bluff_probability
        self.challenge_probability = challenge_probability

    def choose_cards_to_play(self, game: Game) -> tuple[List[Card], Rank]:
        if not self.player.hand:
            raise ValueError(f"{self.player.name} has no cards to play")

        min_rank = game.current_claimed_rank or min(Rank)
        legal_honest_ranks = sorted({card.rank for card in self.player.hand if card.rank >= min_rank})
        should_bluff = self.rng.random() < self.bluff_probability

        if legal_honest_ranks and not should_bluff:
            chosen_rank = legal_honest_ranks[0]
            cards = [card for card in self.player.hand if card.rank == chosen_rank]
            return cards, chosen_rank

        cards = self._choose_lowest_cards()
        legal_claims = [rank for rank in Rank if rank >= min_rank]
        honest_rank = cards[0].rank
        bluff_claims = [rank for rank in legal_claims if rank != honest_rank]
        claimed_rank = self.rng.choice(bluff_claims or legal_claims)

        return cards, claimed_rank

    def should_challenge(self, game: Game) -> bool:
        if not game.last_move or game.last_move.player == self.player:
            return False

        known_count = sum(1 for card in self.player.hand if card.rank == game.last_move.claimed_rank)
        if game.last_move.get_card_count() + known_count > 4:
            return True

        if game.last_move.get_card_count() >= 3:
            return self.rng.random() < self.challenge_probability

        return self.rng.random() < self.challenge_probability / 2

    def _choose_lowest_cards(self) -> List[Card]:
        lowest_rank = min(card.rank for card in self.player.hand)
        lowest_cards = [card for card in self.player.hand if card.rank == lowest_rank]
        max_cards = min(3, len(lowest_cards))
        card_count = self.rng.randint(1, max_cards)
        return lowest_cards[:card_count]
