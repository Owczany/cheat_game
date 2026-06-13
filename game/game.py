from models.deck import Deck
from models.player import Player
from models.card import Card, Rank
from models.table_pile import TablePile
from .move import Move
from typing import List

class Game:
    def __init__(self):
        self.deck = Deck()
        self.table_pile: TablePile = TablePile()
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
    
    def play_cards(self, player: Player, cards: List[Card], claimed_rank: Rank):
        move = Move(player, cards, claimed_rank)
        self.last_move = move
        self.table_pile.add_cards(cards) # TODO: Jeszcze walidacja
        player.discard_cards(cards)
    
    def challenge(self, player: Player) -> bool:
        if not self.last_move:
            print("No move to challenge!")
            return False
        
        is_bluff = self.last_move.is_bluff()
        
        if is_bluff:
            print(f"{player.name} successfully challenged {self.last_move.player.name}'s bluff!")
            self.last_move.player.hand.extend(self.table_pile.cards)
        else:
            print(f"{player.name} failed to challenge {self.last_move.player.name}'s move.")
            player.hand.extend(self.table_pile.cards)

        self.table_pile.clear()
        
        self.last_move = None
        return is_bluff

    def next_turn(self):
        pass

    