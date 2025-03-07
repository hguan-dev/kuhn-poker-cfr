# kuhn_cfr.py
import numpy as np
import random
from kuhn_node import Node
from typing import List, Dict


class KuhnCFR:
    def __init__(self, iterations: int, decksize: int) -> None:
        self.iterations: int = iterations
        self.decksize: int = decksize
        self.cards: List[int] = list(np.arange(decksize))
        self.bet_options: int = 2
        self.nodes: Dict[str, Node] = {}

    def cfr_iterations_external(self) -> None:
        util: np.ndarray = np.zeros(2)
        for t in range(1, self.iterations + 1):
            for i in range(2):
                random.shuffle(self.cards)
                util[i] += self.external_cfr(self.cards[:2], [], 2, 0, i, t)
        print("Average game value: {:.4f}".format(util[0] / self.iterations))
        print("\nFinal Average Strategy:")
        print("-----------------------")
        card_map = {0: "J", 1: "Q", 2: "K"}
        for infoset in sorted(self.nodes):
            card, history = int(infoset[0]), infoset[1:]
            avg_strategy = self.nodes[infoset].get_average_strategy()
            actions = ["Pass", "Bet"]
            history_str = self.format_history(history)
            strategy_str = ", ".join(
                [
                    f"{actions[i]}: {avg_strategy[i]:.2f}"
                    for i in range(self.bet_options)
                ]
            )
            print(f"Card: {card_map[card]}, History: {history_str} -> {strategy_str}")

    def format_history(self, history: str) -> str:
        action_map = {"0": "P", "1": "B"}
        return "".join(action_map.get(h, h) for h in history)

    def external_cfr(
        self,
        cards: List[int],
        history: List[int],
        pot: int,
        nodes_touched: int,
        traversing_player: int,
        t: int,
    ) -> float:
        plays: int = len(history)
        acting_player: int = plays % 2
        opponent_player: int = 1 - acting_player

        if plays >= 2:
            if history[-1] == 0 and history[-2] == 1:  # bet fold
                if acting_player == traversing_player:
                    return 1.0
                else:
                    return -1.0
            if (history[-1] == 0 and history[-2] == 0) or (
                history[-1] == 1 and history[-2] == 1
            ):
                if acting_player == traversing_player:
                    if cards[acting_player] > cards[opponent_player]:
                        return pot / 2.0
                    else:
                        return -pot / 2.0
                else:
                    if cards[acting_player] > cards[opponent_player]:
                        return -pot / 2.0
                    else:
                        return pot / 2.0

        infoset: str = str(cards[acting_player]) + str(history)
        if infoset not in self.nodes:
            self.nodes[infoset] = Node(self.bet_options)

        nodes_touched += 1

        if acting_player == traversing_player:
            utility: np.ndarray = np.zeros(self.bet_options)
            node_util: float = 0.0
            current_strategy: np.ndarray = self.nodes[infoset].get_strategy()
            for a in range(self.bet_options):
                next_history = history + [a]
                next_pot = pot + a
                utility[a] = self.external_cfr(
                    cards, next_history, next_pot, nodes_touched, traversing_player, t
                )
                node_util += current_strategy[a] * utility[a]

            for a in range(self.bet_options):
                regret = utility[a] - node_util
                self.nodes[infoset].regret_sum[a] += regret
            return node_util

        else:
            opponent_strategy: np.ndarray = self.nodes[infoset].get_strategy()
            if random.random() < opponent_strategy[0]:
                next_history = history + [0]
                next_pot = pot
            else:
                next_history = history + [1]
                next_pot = pot + 1
            util: float = self.external_cfr(
                cards, next_history, next_pot, nodes_touched, traversing_player, t
            )
            for a in range(self.bet_options):
                self.nodes[infoset].strategy_sum[a] += opponent_strategy[a]
            return util
