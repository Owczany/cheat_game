from agents import PassiveAgent
from game.game import Game, GameState
from game.move import Move
from models import Card, Player, Rank, Suit


def test_passive_agent_plays_honestly_when_possible():
    game = Game()
    player = Player("Passive")
    low_card = Card(Suit.HEARTS, Rank.THREE)
    legal_card = Card(Suit.SPADES, Rank.KING)
    player.receive_card(low_card)
    player.receive_card(legal_card)
    game.current_claimed_rank = Rank.QUEEN
    agent = PassiveAgent(player)

    cards, claimed_rank = agent.choose_cards_to_play(game)

    assert cards == [legal_card]
    assert claimed_rank == Rank.KING


def test_passive_agent_bluffs_lowest_rank_when_honest_play_is_impossible():
    game = Game()
    player = Player("Passive")
    lowest_card = Card(Suit.HEARTS, Rank.THREE)
    higher_card = Card(Suit.SPADES, Rank.FIVE)
    player.receive_card(higher_card)
    player.receive_card(lowest_card)
    game.current_claimed_rank = Rank.QUEEN
    agent = PassiveAgent(player)

    cards, claimed_rank = agent.choose_cards_to_play(game)

    assert cards == [lowest_card]
    assert claimed_rank == Rank.QUEEN


def test_passive_agent_remembers_own_played_cards_after_act():
    game = Game()
    player1 = Player("Passive")
    player2 = Player("Other")
    card = Card(Suit.HEARTS, Rank.ACE)
    player1.receive_card(card)
    game.add_player(player1)
    game.add_player(player2)
    game.current_player = player1
    game.state = GameState.WAITING_FOR_MOVE
    agent = PassiveAgent(player1)

    agent.act(game)

    assert agent.played_cards == [card]


def test_passive_agent_challenges_when_claim_is_impossible_from_known_cards():
    game = Game()
    passive_player = Player("Passive")
    opponent = Player("Opponent")
    known_card_in_hand = Card(Suit.HEARTS, Rank.KING)
    known_card_played = Card(Suit.SPADES, Rank.KING)
    passive_player.receive_card(known_card_in_hand)
    game.last_move = Move(opponent, [
        Card(Suit.CLUBS, Rank.THREE),
        Card(Suit.DIAMONDS, Rank.FOUR),
        Card(Suit.HEARTS, Rank.FIVE),
    ], Rank.KING)
    agent = PassiveAgent(passive_player)
    agent.remember_played_cards([known_card_played])

    assert agent.should_challenge(game) is True


def test_passive_agent_forgets_played_cards_after_challenge_resolves():
    player = Player("Passive")
    card = Card(Suit.SPADES, Rank.KING)
    agent = PassiveAgent(player)
    agent.remember_played_cards([card])

    agent.on_challenge_resolved()

    assert agent.played_cards == []
