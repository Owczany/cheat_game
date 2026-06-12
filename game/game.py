from models.deck import Deck
from models.player import Player
from .move import Move
from typing import List

class Game:
    def __init__(self):
        self.deck = Deck()
        self.players: List[Player] = []
        self.last_move: Move | None = None

    def deal_cards(self) -> None:
        while self.deck.cards:
            for player in self.players:
                card = self.deck.draw()

                if not card:
                    break

                player.receive_card(card)


    def add_player(self, player: Player):
        self.players.append(player)

    def remove_player(self, player: Player):
        self.players.remove(player)

    def start(self):
        self.deck.shuffle()
        self.deal_cards()

    def is_win(self, player: Player) -> bool:
        return len(player.hand) == 0
    
    def play_cards(self):
        pass
    
    def challange(self, player):
        pass

    def next_turn(self):
        pass

    