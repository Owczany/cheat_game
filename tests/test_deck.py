from models.deck import Deck

def test_deck_has_52_cards():
    deck = Deck()
    assert len(deck.cards) == 52

def test_deck_draw_card_reduces_deck_size():
    deck = Deck()
    initial_size = len(deck.cards)
    deck.draw()
    assert len(deck.cards) == initial_size - 1