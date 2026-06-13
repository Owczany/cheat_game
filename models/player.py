from typing import List
from .card import Card

class Player:
    def __init__(self, name: str):
        self.id: int = id(self)
        self.name: str = name
        self.hand: List[Card] = []

    def show_hand(self) -> str:
        return f"{self.name}'s hand: " + ", ".join(str(card) for card in self.hand)
    
    def receive_card(self, card: Card):
        self.hand.append(card)

    def discard_card(self, card: Card):
        if card in self.hand:
            self.hand.remove(card)
        else:
            print(f"{self.name} does not have {card} in hand!")

    def discard_cards(self, cards: List[Card]):
        for card in cards:
            self.discard_card(card)

    def __eq__(self, other):
        if not isinstance(other, Player):
            return False
        return self.id == other.id