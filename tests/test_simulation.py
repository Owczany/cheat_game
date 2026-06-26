import random

from agents import AdaptiveAgent, AggressiveAgent, BalancedAgent, PassiveAgent, RandomAgent
from models import Player
from simulations import RandomSimulation, Simulation, SimulationResult


def test_simulation_creates_configured_agent_for_each_player():
    alice = Player("Alice")
    bob = Player("Bob")
    charlie = Player("Charlie")
    simulation = Simulation(
        players=[alice, bob, charlie],
        agent_types=[PassiveAgent, AggressiveAgent, RandomAgent],
    )
    game = simulation.create_game()

    agents = simulation.create_agents(game)
    agents_by_name = {agent.player.name: agent for agent in agents}

    assert isinstance(agents_by_name["Alice"], PassiveAgent)
    assert isinstance(agents_by_name["Bob"], AggressiveAgent)
    assert isinstance(agents_by_name["Charlie"], RandomAgent)


def test_simulation_runs_one_game():
    simulation = RandomSimulation(max_steps=100)

    result = simulation.run_once()

    assert isinstance(result, SimulationResult)
    assert result.steps <= 100


def test_simulation_run_many_counts_results():
    simulation = RandomSimulation(max_steps=100)

    results = simulation.run_many(5)

    assert sum(results.values()) == 5


def test_simulation_keeps_agent_types_attached_to_players_after_shuffle(monkeypatch):
    def reverse_shuffle(items):
        items.reverse()

    monkeypatch.setattr(random, "shuffle", reverse_shuffle)
    alice = Player("Alice")
    bob = Player("Bob")
    charlie = Player("Charlie")
    diana = Player("Diana")
    eve = Player("Eve")
    simulation = Simulation(
        players=[alice, bob, charlie, diana, eve],
        agent_types=[RandomAgent, PassiveAgent, AggressiveAgent, AdaptiveAgent, BalancedAgent],
    )
    game = simulation.create_game()

    agents = simulation.create_agents(game)
    agents_by_name = {agent.player.name: agent for agent in agents}

    assert isinstance(agents_by_name["Alice"], RandomAgent)
    assert isinstance(agents_by_name["Bob"], PassiveAgent)
    assert isinstance(agents_by_name["Charlie"], AggressiveAgent)
    assert isinstance(agents_by_name["Diana"], AdaptiveAgent)
    assert isinstance(agents_by_name["Eve"], BalancedAgent)
