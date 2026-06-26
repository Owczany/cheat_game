from agents import AdaptiveAgent, AggressiveAgent, BalancedAgent, PassiveAgent, RandomAgent
from models import Player
from simulations import Simulation


def main():
    simulation = Simulation(
        players=[
            Player("Random"),
            Player("Passive"),
            Player("Aggressive"),
            Player("Adaptive"),
            Player("Balanced"),
        ],
        agent_types=[
            RandomAgent,
            PassiveAgent,
            AggressiveAgent,
            AdaptiveAgent,
            BalancedAgent,
        ],
    )
    simulation.run_many(10_000)


if __name__ == "__main__":
    main()
