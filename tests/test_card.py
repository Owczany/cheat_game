from models.card import Card, Suit, Rank


def test_card_has_suit_and_rank():
    card = Card(Suit.HEARTS, Rank.ACE)

    assert card.suit == Suit.HEARTS
    assert card.rank == Rank.ACE