from game.game import Game
from models.deck import Deck
from models.player import Player

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

    game.deal_cards()
    for player in players:
        assert len(player.hand) > 0
    
    assert len(game.players) == 3
    assert game.deck.get_card_count() == 0
    
    num_cards_before = len(players[0].hand)
    card = players[0].hand[0]
    game.play_cards(players[0], [card], card.rank)
    num_cards_after = len(players[0].hand)

    assert num_cards_after == num_cards_before - 1
    assert game.table_pile.get_card_count() == 1




    