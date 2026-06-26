from agents import ActionResult, ActionType, AdaptiveAgent
from game.move import Move
from game.results import ChallengeResult
from models import Card, Player, Rank, Suit


def test_adaptive_agent_updates_bluff_memory_from_challenge_result():
    adaptive_player = Player("Adaptive")
    challenger = Player("Challenger")
    bluffer = Player("Bluffer")
    agent = AdaptiveAgent(adaptive_player)
    result = ChallengeResult(
        challenger=challenger,
        challenged_player=bluffer,
        was_bluff=True,
        pile_receiver=bluffer,
        cards_taken=(Card(Suit.HEARTS, Rank.THREE),),
        next_player=challenger,
    )

    agent.observe_action(ActionResult(challenger, ActionType.CHALLENGE, result))

    assert agent.challenge_attempts["Challenger"] == 1
    assert agent.successful_challenges["Challenger"] == 1
    assert agent.exposed_bluffs["Bluffer"] == 1


def test_adaptive_agent_challenges_known_bluffer():
    adaptive_player = Player("Adaptive")
    bluffer = Player("Bluffer")
    agent = AdaptiveAgent(adaptive_player)
    agent.exposed_bluffs["Bluffer"] = 3
    game = type("GameStub", (), {})()
    game.last_move = Move(
        bluffer,
        [Card(Suit.HEARTS, Rank.TWO), Card(Suit.SPADES, Rank.THREE), Card(Suit.CLUBS, Rank.FOUR)],
        Rank.ACE,
    )

    assert agent.should_challenge(game) is True
