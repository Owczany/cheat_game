import pytest

from game.game import Game, GameState
from models.deck import Deck
from models.player import Player
from models.card import Card, Rank, Suit

def test_game_initialization():
    game = Game()
    assert isinstance(game.deck, Deck)
    assert game.players == []
    assert game.last_move is None

# TODO: Dokończyć ten test
def test():
    game = Game()
    names = [ 'John', 'Peter', 'Tom' ]
    players = [ Player(name) for name in names ]

    for player in players:
        game.add_player(player)

    assert len(game.players) == 3
    assert game.players[0].name == 'John'
    assert game.players[1].name == 'Peter'
    assert game.players[2].name == 'Tom'

    game.start()

    game.deal_cards()
    for player in players:
        assert len(player.hand) > 0
    
    assert len(game.players) == 3
    assert game.deck.get_card_count() == 0
    
    num_cards_before = len(players[0].hand)
    card = players[0].hand[0]
    game.current_player = players[0]
    game.play_cards(players[0], [card], card.rank)
    num_cards_after = len(players[0].hand)

    assert num_cards_after == num_cards_before - 1
    assert game.table_pile.get_card_count() == 1
    assert game.table_pile.cards == [card]


def test_game_play_and_pass_challenge_flow():
    game = Game()
    player1 = Player("John")
    player2 = Player("Peter")

    game.add_player(player1)
    game.add_player(player2)

    assert game.state == GameState.READY_TO_START

    game.start()

    current_player = game.current_player
    next_player = game.next_player()
    card = current_player.hand[0]
    current_player_card_count = len(current_player.hand)

    assert game.state == GameState.WAITING_FOR_MOVE

    game.play_cards(current_player, [card], card.rank)

    assert len(current_player.hand) == current_player_card_count - 1
    assert game.current_player == next_player
    assert game.state == GameState.WAITING_FOR_CHALLENGE
    assert game.last_move is not None
    assert game.last_move.player == current_player
    assert game.table_pile.cards == [card]

    game.pass_challenge(next_player)

    assert game.current_player == next_player
    assert game.state == GameState.WAITING_FOR_MOVE
    assert game.last_move is None
    assert game.table_pile.cards == [card]


def test_game_rejects_claimed_rank_lower_than_current_table_rank():
    game = Game()
    player1 = Player("John")
    player2 = Player("Peter")
    player1.receive_card(Card(Suit.HEARTS, Rank.KING))
    player2.receive_card(Card(Suit.CLUBS, Rank.QUEEN))

    game.add_player(player1)
    game.add_player(player2)
    game.current_player = player1
    game.state = GameState.WAITING_FOR_MOVE

    game.play_cards(player1, [player1.hand[0]], Rank.KING)
    game.pass_challenge(player2)

    with pytest.raises(ValueError):
        game.play_cards(player2, [player2.hand[0]], Rank.QUEEN)
