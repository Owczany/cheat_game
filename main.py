from agents import AggressiveAgent, PassiveAgent, RandomAgent
from models import Player
from simulations import Simulation


def main():
    simulation = Simulation(
        players=[
            Player("Random"),
            Player("Passive"),
            Player("Aggressive"),
        ],
        agent_types=[
            RandomAgent,
            PassiveAgent,
            AggressiveAgent,
        ],
    )
    simulation.run_many(10_000)


if __name__ == "__main__":
    main()
