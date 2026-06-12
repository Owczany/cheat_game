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
    
    def draw_for_player(self, player: Player):
        card = self.draw()
        if card:
            player.hand.append(card)
    
    def deal(self, players: List[Player], cards_per_player: int):
        num_players = len(players)
        if num_players * cards_per_player > len(self.cards):
            print("Not enough cards to deal!")
            return
        for _ in range(cards_per_player):
            for player in players:
                card = self.draw() # TODO: Przemyśleć sens
                if card:
                    player.hand.append(card)
    
    def deal_all_cards(self, num_players):
        if num_players > len(self.cards):
            print("Not enough cards to deal!")
            return None
        hands = {f"Player {i+1}": [] for i in range(num_players)}
        while self.cards:
            for player in hands:
                if self.cards:
                    hands[player].append(self.draw())
        return hands
    
    def __str__(self):
        return f"{"\n".join(str(card) for card in self.cards)}\nDeck of {len(self.cards)} cards"