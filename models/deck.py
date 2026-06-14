from models.card import Card
from models.player import Player

from typing import List

class Deck:
    def __init__(self):
        self.cards: List[Card] = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]

    def shuffle(self) -> None:
        import random
        random.shuffle(self.cards)

    def draw(self) -> Card | None:
        if not self.cards: print("The deck is empty!")
        return self.cards.pop() if self.cards else None
    
    def get_card_count(self) -> int:
        return len(self.cards)
    
    def __str__(self):
        return f"{"\n".join(str(card) for card in self.cards)}\nDeck of {len(self.cards)} cards"