import random
from collections import defaultdict
from typing import List

from .actions import ActionResult
from .agent import Agent
from game.game import Game
from game.results import ChallengeResult
from models import Card, Player, Rank


class AdaptiveAgent(Agent):
    def __init__(self, player: Player, rng: random.Random | None = None):
        super().__init__(player)
        self.rng = rng or random.Random()
        self.challenge_attempts: dict[str, int] = defaultdict(int)
        self.successful_challenges: dict[str, int] = defaultdict(int)
        self.exposed_bluffs: dict[str, int] = defaultdict(int)

    def choose_cards_to_play(self, game: Game) -> tuple[List[Card], Rank]:
        if not self.player.hand:
            raise ValueError(f"{self.player.name} has no cards to play")

        min_rank = game.current_claimed_rank or min(Rank)
        honest_ranks = sorted({card.rank for card in self.player.hand if card.rank >= min_rank})
        next_player = game.next_player()
        pressure = self._challenge_success_rate(next_player)

        if honest_ranks and (pressure > 0.4 or self.rng.random() > 0.45):
            chosen_rank = self._rank_with_most_cards(honest_ranks)
            cards = [card for card in self.player.hand if card.rank == chosen_rank]
            return cards, chosen_rank

        cards = self._lowest_cards(limit=3)
        legal_claims = [rank for rank in Rank if rank >= min_rank]
        bluff_claims = [rank for rank in legal_claims if rank != cards[0].rank]
        claimed_rank = self.rng.choice(bluff_claims or legal_claims)
        return cards, claimed_rank

    def should_challenge(self, game: Game) -> bool:
        if not game.last_move or game.last_move.player == self.player:
            return False

        known_count = self._known_rank_count(game.last_move.claimed_rank)
        if game.last_move.get_card_count() + known_count > 4:
            return True

        bluff_rate = self._exposed_bluff_rate(game.last_move.player)
        if game.last_move.get_card_count() >= 3 and bluff_rate > 0.2:
            return True

        return self.rng.random() < bluff_rate

    def observe_action(self, action_result: ActionResult) -> None:
        super().observe_action(action_result)

        if isinstance(action_result.game_result, ChallengeResult):
            result = action_result.game_result
            challenger_name = result.challenger.name
            challenged_name = result.challenged_player.name
            self.challenge_attempts[challenger_name] += 1

            if result.was_bluff:
                self.successful_challenges[challenger_name] += 1
                self.exposed_bluffs[challenged_name] += 1

    def _challenge_success_rate(self, player: Player) -> float:
        attempts = self.challenge_attempts[player.name]
        if attempts == 0:
            return 0.0
        return self.successful_challenges[player.name] / attempts

    def _exposed_bluff_rate(self, player: Player) -> float:
        attempts_against_player = sum(self.exposed_bluffs.values())
        if attempts_against_player == 0:
            return 0.0
        return self.exposed_bluffs[player.name] / attempts_against_player

    def _known_rank_count(self, rank: Rank) -> int:
        known_cards = self.player.hand + self.played_cards
        return sum(1 for card in known_cards if card.rank == rank)

    def _rank_with_most_cards(self, ranks: list[Rank]) -> Rank:
        return max(
            ranks,
            key=lambda rank: (sum(1 for card in self.player.hand if card.rank == rank), -rank),
        )

    def _lowest_cards(self, limit: int) -> List[Card]:
        lowest_rank = min(card.rank for card in self.player.hand)
        cards = [card for card in self.player.hand if card.rank == lowest_rank]
        return cards[:limit]
