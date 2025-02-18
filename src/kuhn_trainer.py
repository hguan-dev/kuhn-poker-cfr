import random
from typing import List, Dict
from kuhn_node import KuhnNode
import pickle
import time
from kuhn_test import KuhnTest

NUM_ACTIONS: int = 2
nodeMap: Dict[str, KuhnNode] = {}


def train(iterations: int, saveName: str) -> None:
    """
    Trains the model for a given number of iterations and saves the result.
    """
    t1 = time.time()
    cards: List[int] = [1, 2, 3]
    util: float = 0.0
    for i in range(1, iterations):
        random.shuffle(cards)
        util += cfr(cards, "", 1.0, 1.0)
        freq_print: int = 100000
        if i % freq_print == 0:
            if time.time() - t1 != 0.0:
                print(
                    f"Kuhn trained {i} iterations. {freq_print / (time.time() - t1)} iterations per second."
                )
            my = KuhnTest()
            my.nodeMap = nodeMap
            print("Average game value: " + str(my.gameValue()))
            print(f"Worst case game value: {my.exploitability()}")
            print(f"Total exploitability: {-sum(my.exploitability())}")
            t1 = time.time()
    my = KuhnTest()
    my.nodeMap = nodeMap
    print("Strategy: ")
    for node in nodeMap.values():
        print(node)
    print("Average game value: " + str(my.gameValue()))
    with open(saveName, "wb") as f:
        pickle.dump(nodeMap, f)


def cfr(cards: List[int], history: str, p0: float, p1: float) -> float:
    """
    Counterfactual Regret Minimization (CFR) implementation.
    """
    plays: int = len(history)
    curr_player: int = plays % 2

    infoSet: str = str(cards[curr_player]) + history

    curr_node: KuhnNode = nodeMap.get(infoSet, KuhnNode())
    curr_node.infoSet = infoSet
    payoff: float | None = curr_node.returnPayoff(cards)
    terminalNode: bool = payoff is not None

    if terminalNode:
        return payoff if payoff is not None else 0.0

    if infoSet not in nodeMap:
        nodeMap[infoSet] = curr_node

    realization_weight: float = p1 if curr_player == 0 else p0
    strategy: List[float] = curr_node.getStrategy(realization_weight)
    util: List[float] = [0.0] * NUM_ACTIONS

    nodeUtil: float = 0.0
    for a in range(NUM_ACTIONS):
        nextHistory: str = history + ("p" if a == 0 else "b")
        if curr_player == 0:
            util[a] = -cfr(cards, nextHistory, p0 * strategy[a], p1)
        else:
            util[a] = -cfr(cards, nextHistory, p0, p1 * strategy[a])
        nodeUtil += strategy[a] * util[a]

    for a in range(NUM_ACTIONS):
        regret: float = util[a] - nodeUtil
        curr_node.regretSum[a] += (p1 if curr_player == 0 else p0) * regret
    return nodeUtil


if __name__ == "__main__":
    start_time: float = time.time()
    train(10**6, "kt-10")
    print("--- %s seconds ---" % (time.time() - start_time))
