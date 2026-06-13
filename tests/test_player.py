from models.player import Player

def test_player_initialization():
    player = Player("Alice")
    assert player.name == "Alice"
    assert player.hand == []

def test_player_equality():
    player1 = Player("Alice")
    player2 = player1
    player3 = Player("Bob")

    assert player1 == player2
    assert player1 != player3