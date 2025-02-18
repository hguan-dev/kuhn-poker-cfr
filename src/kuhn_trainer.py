from typing import List, Dict
from kuhn_node import KuhnNode
import time
import random as rd

NUM_ACTIONS: int = 2
nodeMap: Dict[str, KuhnNode] = {}


def train(iterations: int, saveName: str) -> None:
    cards: List[int] = [1, 2, 3]
    total_util: float = 0.0

    for i in range(1, iterations):
        rd.shuffle(cards)
        total_util += cfr(cards, "", 1, 1)

        if i % 100000 == 0:
            avg_game_value = total_util / i
            print(f"Iteration {i}/{iterations} - Avg Game Value: {avg_game_value:.4f}")
    
    print("\nFinal Strategies:")
    for infoSet, node in nodeMap.items():
        avg_strategy = [x / sum(node.strategySum) if sum(node.strategySum) > 0 else 1/NUM_ACTIONS for x in node.strategySum]
        print(f"{infoSet}: {avg_strategy}")

    pass


def cfr(cards: List[int], history: str, p0: float, p1: float) -> float:
    plays: int = len(history)
    curr_player: int = plays % 2
    opponent: int = plays % 2 + 1

    # Base case: returns payoffs in terminal state.
    if history in ["bb", "bp", "pbp", "pbb", "pp"]:
        terminalPass: bool = history[plays - 1] == "p"
        doubleBet: bool = history[plays - 2 :] == "bb"
        isPlayerCardHigher: bool = cards[curr_player] > cards[opponent]

        if terminalPass:
            if history == "pp":
                return 1 if isPlayerCardHigher else -1
            # History is 'pbp' or 'bp'
            return 1

        if doubleBet:
            return 2 if isPlayerCardHigher else -2
    # Recursive case
    infoSet = str(cards[curr_player]) + history
    
    node = nodeMap.get(infoSet, KuhnNode())
    nodeMap[infoSet] = node
    strategy = node.getStrategy(p0 if curr_player == 0 else p1)

    util: List[float] = [0.0] * NUM_ACTIONS
    node_util = 0.0
    for a in range(NUM_ACTIONS):
        next_history = history + ("p" if a == 0 else "b")
        next_p0 = p0 * strategy[a] if curr_player == 0 else p0
        next_p1 = p1 * strategy[a] if curr_player == 1 else p1
        util[a] = -cfr(cards, next_history, next_p0, next_p1)
        node_util += strategy[a] * util[a]

    for a in range(NUM_ACTIONS):
        regret = util[a] - node_util
        node.regretSum[a] += regret if curr_player == 0 else -regret
    
    return node_util

    pass


if __name__ == "__main__":
    start_time: float = time.time()
    train(10**6, "kt-10")
    print("--- %s seconds ---" % (time.time() - start_time))
