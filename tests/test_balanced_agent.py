from agents import BalancedAgent
from game.game import Game
from game.move import Move
from models import Card, Player, Rank, Suit


def test_balanced_agent_plays_largest_legal_group():
    game = Game()
    player = Player("Balanced")
    queen_1 = Card(Suit.HEARTS, Rank.QUEEN)
    queen_2 = Card(Suit.SPADES, Rank.QUEEN)
    king = Card(Suit.CLUBS, Rank.KING)
    player.receive_card(king)
    player.receive_card(queen_1)
    player.receive_card(queen_2)
    game.current_claimed_rank = Rank.JACK
    agent = BalancedAgent(player)

    cards, claimed_rank = agent.choose_cards_to_play(game)

    assert cards == [queen_1, queen_2]
    assert claimed_rank == Rank.QUEEN


def test_balanced_agent_challenges_large_suspicious_claim():
    game = Game()
    player = Player("Balanced")
    opponent = Player("Opponent")
    player.receive_card(Card(Suit.HEARTS, Rank.KING))
    game.last_move = Move(
        opponent,
        [Card(Suit.SPADES, Rank.TWO), Card(Suit.CLUBS, Rank.THREE), Card(Suit.DIAMONDS, Rank.FOUR)],
        Rank.KING,
    )
    agent = BalancedAgent(player)

    assert agent.should_challenge(game) is True
