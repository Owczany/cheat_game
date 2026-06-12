from typing import List
from models.card import Card
from models.player import Player
from models.deck import Rank

class Move():
    def __init__(self, player, cards, claimed_rank):
        self.player: Player = player
        self.cards: List[Card] = cards
        self.claimed_rank: Rank  = claimed_rank

    def is_bluff(self) -> bool:
        return any(card.rank != self.claimed_rank for card in self.cards)
    
    def get_card_count(self) -> int:
        return len(self.cards)

    def __str__(self):
        return f"{self.player.name} claims {self.claimed_rank}"
    

