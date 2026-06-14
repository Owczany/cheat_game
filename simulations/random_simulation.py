from agents import RandomAgent
from models import Player

from .simulation import Simulation


class RandomSimulation(Simulation):
    def __init__(
        self,
        player_names: list[str] | None = None,
        max_steps: int = 500,
        show_gameplay: bool = False,
    ):
        names = player_names or ["Alice", "Bob", "Charlie", "Diana"]
        players = [Player(name) for name in names]
        agent_types = [RandomAgent for _ in players]

        super().__init__(
            players=players,
            agent_types=agent_types,
            max_steps=max_steps,
            show_gameplay=show_gameplay,
        )
