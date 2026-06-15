from agents import ActionResult, ActionType, PassiveAgent
from game.game import Game, GameState
from game.results import ChallengeResult, PassChallengeResult, PlayCardsResult
from models import Card, Player, Rank, Suit


def test_play_cards_returns_result():
    game = Game()
    player1 = Player("Alice")
    player2 = Player("Bob")
    card = Card(Suit.HEARTS, Rank.ACE)
    player1.receive_card(card)
    game.add_player(player1)
    game.add_player(player2)
    game.current_player = player1
    game.state = GameState.WAITING_FOR_MOVE

    result = game.play_cards(player1, [card], Rank.ACE)

    assert isinstance(result, PlayCardsResult)
    assert result.player == player1
    assert result.cards == (card,)
    assert result.claimed_rank == Rank.ACE
    assert result.next_player == player2


def test_pass_challenge_returns_result():
    game = Game()
    player = Player("Bob")
    game.add_player(Player("Alice"))
    game.add_player(player)
    game.current_player = player
    game.state = GameState.WAITING_FOR_CHALLENGE

    result = game.pass_challenge(player)

    assert isinstance(result, PassChallengeResult)
    assert result.player == player
    assert result.next_player == player


def test_challenge_returns_result():
    game = Game()
    player1 = Player("Alice")
    player2 = Player("Bob")
    card = Card(Suit.HEARTS, Rank.THREE)
    player1.receive_card(card)
    game.add_player(player1)
    game.add_player(player2)
    game.current_player = player1
    game.state = GameState.WAITING_FOR_MOVE
    game.play_cards(player1, [card], Rank.KING)

    result = game.challenge(player2)

    assert isinstance(result, ChallengeResult)
    assert result.challenger == player2
    assert result.challenged_player == player1
    assert result.was_bluff is True
    assert result.pile_receiver == player1
    assert result.cards_taken == (card,)


def test_agent_act_returns_action_result_and_observes_own_play():
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

    result = agent.act(game)

    assert isinstance(result, ActionResult)
    assert result.action_type == ActionType.PLAY_CARDS
    assert isinstance(result.game_result, PlayCardsResult)
    assert agent.played_cards == [card]
