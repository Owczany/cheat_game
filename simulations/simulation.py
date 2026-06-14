from contextlib import nullcontext, redirect_stdout
from dataclasses import dataclass
from io import StringIO

from agents import Agent
from game.game import Game, GameState
from models import Player


@dataclass
class SimulationResult:
    winner: Player | None
    steps: int


class Simulation:
    def __init__(
        self,
        players: list[Player],
        agent_types: list[type[Agent]],
        max_steps: int = 500,
        show_gameplay: bool = False,
    ):
        if len(players) != len(agent_types):
            raise ValueError("Each player must have exactly one agent type")

        self.players = players
        self.agent_types = agent_types
        self.max_steps = max_steps
        self.show_gameplay = show_gameplay

    def create_game(self) -> Game:
        game = Game()

        for player in self.players:
            game.add_player(player)

        game.start()
        return game

    def create_agents(self, game: Game) -> list[Agent]:
        agents = []

        for player in game.players:
            player_index = self.players.index(player)
            agent_type = self.agent_types[player_index]
            agents.append(agent_type(player))

        return agents

    def find_agent_for_current_player(self, agents: list[Agent], game: Game) -> Agent:
        for agent in agents:
            if agent.player == game.current_player:
                return agent

        raise ValueError("No agent found for current player")

    def find_winner(self, game: Game) -> Player | None:
        for player in game.players:
            if game.is_win(player):
                return player

        return None

    def run_once(self, show_gameplay: bool | None = None) -> SimulationResult:
        should_show_gameplay = self.show_gameplay if show_gameplay is None else show_gameplay
        game = self.create_game()
        agents = self.create_agents(game)

        if should_show_gameplay:
            print("Starting simulation")
            print("Players:", ", ".join(player.name for player in game.players))

        for step in range(1, self.max_steps + 1):
            if game.state == GameState.WAITING_FOR_MOVE:
                winner = self.find_winner(game)
                if winner:
                    game.state = GameState.FINISHED
                    if should_show_gameplay:
                        print(f"Winner: {winner.name}")
                    return SimulationResult(winner, step - 1)

            agent = self.find_agent_for_current_player(agents, game)
            state_before_action = game.state
            player_before_action = game.current_player

            output_context = nullcontext() if should_show_gameplay else redirect_stdout(StringIO())
            with output_context:
                agent.act(game)

            if self.was_challenge_resolved(state_before_action, game):
                self.notify_challenge_resolved(agents)

            if should_show_gameplay:
                self.print_step(step, state_before_action, player_before_action, game)

        if should_show_gameplay:
            print(f"Simulation stopped after {self.max_steps} steps")

        return SimulationResult(None, self.max_steps)

    def run_many(self, count: int = 1000) -> dict[str, int]:
        player_names = [player.name for player in self.players]
        wins = {name: 0 for name in player_names}
        wins["No winner"] = 0

        for _ in range(count):
            self.reset_players()
            result = self.run_once(show_gameplay=False)
            winner_name = result.winner.name if result.winner else "No winner"
            wins[winner_name] += 1

        print(f"Results after {count} simulations:")
        for player_name, win_count in wins.items():
            print(f"{player_name}: {win_count}")

        return wins

    def reset_players(self) -> None:
        for player in self.players:
            player.hand.clear()

    def was_challenge_resolved(self, state_before_action: GameState, game: Game) -> bool:
        return (
            state_before_action == GameState.WAITING_FOR_CHALLENGE
            and game.table_pile.is_empty()
            and game.current_claimed_rank is None
        )

    def notify_challenge_resolved(self, agents: list[Agent]) -> None:
        for agent in agents:
            agent.on_challenge_resolved()

    def print_step(
        self,
        step: int,
        state_before_action: GameState,
        player_before_action: Player,
        game: Game,
    ) -> None:
        if state_before_action == GameState.WAITING_FOR_MOVE and game.last_move:
            print(
                f"{step}. {player_before_action.name} played "
                f"{game.last_move.get_card_count()} card(s) as {game.last_move.claimed_rank.name}"
            )
            return

        if state_before_action == GameState.WAITING_FOR_CHALLENGE:
            print(f"{step}. {player_before_action.name} resolved challenge decision")
