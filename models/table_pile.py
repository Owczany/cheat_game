from typing import List
from models.card import Card

class TablePile:
    def __init__(self):
        self.cards: List[Card] = []

    def add_cards(self, cards: List[Card]):
        self.cards.extend(cards)

    def clear(self) -> None:
        self.cards.clear()

    def get_card_count(self) -> int:
        return len(self.cards)
    
    def is_empty(self) -> bool:
        return len(self.cards) == 0
    
    def __str__(self):
        return f"Table Pile: " + ", ".join(str(card) for card in self.cards)