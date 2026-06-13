from models.table_pile import TablePile
from models.card import Card, Suit, Rank

def test_table_pile_initialization():
    table_pile = TablePile()
    assert table_pile.cards == []

def test_table_pile_add_cards():
    table_pile = TablePile()
    cards = [Card(suit, rank) for suit in [Suit.HEARTS, Suit.SPADES] for rank in [Rank.ACE, Rank.KING]]
    table_pile.add_cards(cards)
    assert table_pile.cards == cards

def test_table_pile_clear():
    table_pile = TablePile()
    cards = [Card(Suit.HEARTS, Rank.ACE), Card(Suit.SPADES, Rank.KING)]
    table_pile.add_cards(cards)
    table_pile.clear()
    assert table_pile.cards == []

def test_table_pile_get_card_count():
    table_pile = TablePile()
    cards = [Card(Suit.HEARTS, Rank.ACE), Card(Suit.SPADES, Rank.KING)]
    table_pile.add_cards(cards)
    assert table_pile.get_card_count() == 2

def test_table_pile_is_empty():
    table_pile = TablePile()
    assert table_pile.is_empty() == True
    table_pile.add_cards([Card(Suit.HEARTS, Rank.ACE)])
    assert table_pile.is_empty() == False

def test_general():
    table_pile = TablePile()
    cards = []