import random

from agents import AggressiveAgent
from game.game import Game
from game.move import Move
from models import Card, Player, Rank, Suit


def test_aggressive_agent_can_bluff_with_low_cards():
    game = Game()
    player = Player("Aggressive")
    low_card = Card(Suit.HEARTS, Rank.THREE)
    player.receive_card(low_card)
    game.current_claimed_rank = Rank.QUEEN
    agent = AggressiveAgent(player, random.Random(0), bluff_probability=1.0)

    cards, claimed_rank = agent.choose_cards_to_play(game)

    assert cards == [low_card]
    assert claimed_rank >= Rank.QUEEN
    assert claimed_rank != low_card.rank


def test_aggressive_agent_plays_honestly_when_not_bluffing():
    game = Game()
    player = Player("Aggressive")
    legal_card = Card(Suit.HEARTS, Rank.KING)
    player.receive_card(legal_card)
    game.current_claimed_rank = Rank.QUEEN
    agent = AggressiveAgent(player, random.Random(0), bluff_probability=0.0)

    cards, claimed_rank = agent.choose_cards_to_play(game)

    assert cards == [legal_card]
    assert claimed_rank == Rank.KING


def test_aggressive_agent_challenges_impossible_claim():
    game = Game()
    player = Player("Aggressive")
    opponent = Player("Opponent")
    player.receive_card(Card(Suit.HEARTS, Rank.ACE))
    player.receive_card(Card(Suit.SPADES, Rank.ACE))
    game.last_move = Move(opponent, [
        Card(Suit.CLUBS, Rank.TWO),
        Card(Suit.DIAMONDS, Rank.THREE),
        Card(Suit.HEARTS, Rank.FOUR),
    ], Rank.ACE)
    agent = AggressiveAgent(player, random.Random(0))

    assert agent.should_challenge(game) is True
