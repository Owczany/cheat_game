from models.deck import Deck
from models.player import Player
from models.card import Card, Rank
from models.table_pile import TablePile
from enum import Enum
from .move import Move
from typing import List

class GameState(Enum):
    WAITING_FOR_PLAYERS = 1
    READY_TO_START = 2
    WAITING_FOR_MOVE = 3
    WAITING_FOR_CHALLENGE = 4
    FINISHED = 5

class Game:
    def __init__(self):
        self.deck = Deck()
        self.table_pile: TablePile = TablePile()
        self.players: List[Player] = []
        self.current_player: Player | None = None
        self.last_move: Move | None = None
        self.current_claimed_rank: Rank | None = None
        self.state: GameState = GameState.WAITING_FOR_PLAYERS

    def _validate_player_turn(self, player: Player) -> None:
        if player != self.current_player:
            raise ValueError(f"It's not {player.name}'s turn")

    def _validate_player_in_game(self, player: Player) -> None:
        if player not in self.players:
            raise ValueError(f"{player.name} is not in this game")
        
    def _validate_player_has_cards(self, player: Player, cards: List[Card]) -> None:
        for card in cards:
            if card not in player.hand:
                raise ValueError(f"{player.name} does not have {card} in hand")
            
    def _validate_cards_not_empty(self, cards: List[Card]) -> None:
        if not cards:
            raise ValueError("No cards provided")
        
    def _validate_can_start_game(self) -> None:
        if len(self.players) < 2:
            raise ValueError("At least 2 players are required to start the game")

    def _validate_has_players(self) -> None:
        if not self.players:
            raise ValueError("Cannot deal cards without players")
        
    def _validate_game_state(self, required_state: GameState) -> None:
        if self.state != required_state:
            raise ValueError(f"Game must be in state {required_state} to perform this action")

    def _validate_can_manage_players(self) -> None:
        if self.state not in [GameState.WAITING_FOR_PLAYERS, GameState.READY_TO_START]:
            raise ValueError("Players cannot be changed after the game starts")

    def _validate_has_last_move(self) -> None:
        if self.last_move is None:
            raise ValueError("No move to challenge")
        
    def _validate_claimed_rank_not_lower(self, claimed_rank: Rank) -> None:
        if self.current_claimed_rank is not None and claimed_rank < self.current_claimed_rank:
            raise ValueError(f"Claimed rank cannot be lower than {self.current_claimed_rank}")

    def deal_cards(self) -> None:
        self._validate_has_players()

        while self.deck.cards:
            for player in self.players:
                if not self.deck.cards:
                    break

                card = self.deck.draw()
                if not card:
                    break
                player.receive_card(card)

    def add_player(self, player: Player) -> None:
        self._validate_can_manage_players()
        self.players.append(player)

        if len(self.players) >= 2 and self.state == GameState.WAITING_FOR_PLAYERS:
            self.state = GameState.READY_TO_START

    def remove_player(self, player: Player) -> None:
        self._validate_can_manage_players()
        self._validate_player_in_game(player)
        self.players.remove(player)

        if len(self.players) < 2 and self.state == GameState.READY_TO_START:
            self.state = GameState.WAITING_FOR_PLAYERS

    def shuffle_players(self):
        import random
        random.shuffle(self.players)

    def start(self):
        self._validate_game_state(GameState.READY_TO_START)
        self._validate_can_start_game()

        self.shuffle_players()
        self.deck.shuffle()
        self.deal_cards()
        self.current_player = self.players[0]
        self.state = GameState.WAITING_FOR_MOVE


    def is_win(self, player: Player) -> bool:
        self.game_state = GameState.FINISHED
        return len(player.hand) == 0
    
    def play_cards(self, player: Player, cards: List[Card], claimed_rank: Rank):
        self._validate_game_state(GameState.WAITING_FOR_MOVE)
        self._validate_player_in_game(player)
        self._validate_cards_not_empty(cards)
        self._validate_player_turn(player)
        self._validate_player_has_cards(player, cards)
        self._validate_claimed_rank_not_lower(claimed_rank)
            
        self.last_move = Move(player, cards, claimed_rank)
        self.current_claimed_rank = claimed_rank
        player.discard_cards(cards)
        self.table_pile.add_cards(cards)
        self.next_turn()
        self.state = GameState.WAITING_FOR_CHALLENGE

    def pass_challenge(self, player: Player) -> None:
        self._validate_game_state(GameState.WAITING_FOR_CHALLENGE)
        self._validate_player_in_game(player)
        self._validate_player_turn(player)
        self.last_move = None
        self.state = GameState.WAITING_FOR_MOVE
    
    def challenge(self, player: Player) -> bool:
        self._validate_game_state(GameState.WAITING_FOR_CHALLENGE)
        self._validate_player_in_game(player)
        self._validate_player_turn(player)
        self._validate_has_last_move()
        
        is_bluff = self.last_move.is_bluff()
        
        if is_bluff:
            print(f"{player.name} successfully challenged {self.last_move.player.name}'s bluff!")
            self.last_move.player.hand.extend(self.table_pile.cards)
        else:
            print(f"{player.name} failed to challenge {self.last_move.player.name}'s move.")
            player.hand.extend(self.table_pile.cards)

        self.table_pile.clear()
        self.last_move = None
        self.current_claimed_rank = None
        self.state = GameState.WAITING_FOR_MOVE

        return is_bluff
    
    def get_number_of_players(self) -> int:
        return len(self.players)
    
    def next_player(self) -> Player:
        next_player_idx = (self.players.index(self.current_player) + 1) % self.get_number_of_players()
        return self.players[next_player_idx]

    def next_turn(self) -> None:
        self.current_player = self.next_player()
    
