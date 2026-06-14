import random

from agents import RandomAgent
from game.game import Game, GameState
from models import Card, Player, Rank, Suit


def test_random_agent_chooses_cards_from_own_hand():
    game = Game()
    player = Player("Random")
    cards = [Card(Suit.HEARTS, Rank.THREE), Card(Suit.SPADES, Rank.KING)]
    player.receive_card(cards[0])
    player.receive_card(cards[1])
    agent = RandomAgent(player, random.Random(0))

    chosen_cards, claimed_rank = agent.choose_cards_to_play(game)

    assert chosen_cards
    assert all(card in player.hand for card in chosen_cards)
    assert claimed_rank in Rank


def test_random_agent_respects_current_claimed_rank():
    game = Game()
    game.current_claimed_rank = Rank.KING
    player = Player("Random")
    player.receive_card(Card(Suit.CLUBS, Rank.TWO))
    agent = RandomAgent(player, random.Random(1))

    _, claimed_rank = agent.choose_cards_to_play(game)

    assert claimed_rank >= Rank.KING


def test_random_agent_can_act_when_waiting_for_move():
    game = Game()
    player1 = Player("Random")
    player2 = Player("Other")
    card = Card(Suit.HEARTS, Rank.ACE)
    player1.receive_card(card)
    game.add_player(player1)
    game.add_player(player2)
    game.current_player = player1
    game.state = GameState.WAITING_FOR_MOVE
    agent = RandomAgent(player1, random.Random(2))

    agent.act(game)

    assert card not in player1.hand
    assert game.table_pile.get_card_count() == 1
    assert game.current_player == player2
    assert game.state == GameState.WAITING_FOR_CHALLENGE
    assert len(agent.observations) == 1
