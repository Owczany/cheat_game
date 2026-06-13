# TODO: Uzupełnić ten plik

from game.move import Move
from models import Card, Rank, Player

def test_move_initialization():
    move = Move("Player1", ["Card1", "Card2"], "Rank1")

    assert move.player == "Player1"
    assert move.cards == ["Card1", "Card2"]
    assert move.claimed_rank == "Rank1"