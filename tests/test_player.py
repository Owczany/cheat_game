from models.player import Player

def test_player_initialization():
    player = Player("Alice")
    assert player.name == "Alice"
    assert player.hand == []