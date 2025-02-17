from typing import List, Dict
from kuhn_node import KuhnNode
from kuhn_test import KuhnTest
import time
import pickle
import random

NUM_ACTIONS: int = 2
nodeMap: Dict[str, KuhnNode] = {}


def train(iterations: int, saveName: str) -> None:
    """
    Train the Kuhn Poker model using Counterfactual Regret Minimization (CFR).

    TODO:
    - Initialize a deck of cards for the game (e.g., [1, 2, 3]).
    - For each iteration:
        1. Shuffle the deck to simulate chance outcomes.
        2. Call the `cfr` function to compute regrets and update strategies.
    - Periodically print training progress:
        1. Report the current iteration number.
        2. Calculate and display the average game value.
        3. Display the exploitability of the current strategy.
    - After training:
        1. Print the final strategy for each information set.
        2. Compute and display the average game value for the trained model.
    - Save the trained strategy to a file for future use.

    Parameters:
        iterations (int): The number of training iterations to run.
        saveName (str): The name of the file to save the trained model.
    """
    t1 = time.time()
    cards: List[int] = [1, 2, 3]

    # TODO: Initialize utility tracking variables (e.g., total utility)
    total_utility: float = 0.0

    # TODO: Start the main training loop over the specified number of iterations
    #   - Shuffle the deck (use `random.shuffle(cards)`)
    #   - Call the `cfr` function with the current card order, history, and probabilities
    #   - Accumulate the utility returned by `cfr`
    for i in range(1, iterations):
        random.shuffle(cards)
        util = cfr(cards, "", 1, 1)
        total_utility += util

        # TODO: Add progress reporting for every N iterations:
        #   - Print the number of iterations completed and the iteration speed
        #   - Calculate and display metrics like game value and exploitability

        if i % 100000 == 0:
            if time.time() - t1 != 0.:
                print(f"Trained {i} iterations. {str(100000 / (time.time() - t1))} iterations per second.")
            kt = KuhnTest()
            kt.nodeMap = nodeMap
            t1 = time.time()
            print(f"Average game value: {kt.gameValue()}")
            print(f"Exploitability: {sum(kt.exploitability())}")

    # TODO: After training, print the final strategy for all information sets
    print("Final Strategy:")
    for infoSet, node in nodeMap.items():
        avg_strategy = node.getAverageStrategy()
        print(f"{infoSet}: p = {avg_strategy[0]}, b = {avg_strategy[1]}")

    # TODO: Save the model (strategy and node data) to a file with the provided name
    # this i just searched up bc the other files used pickle lol
    with open(saveName, "wb") as file:
        pickle.dump(nodeMap, file)

    pass


def cfr(cards: List[int], history: str, p0: float, p1: float) -> float:
    """
    Counterfactual Regret Minimization (CFR) algorithm.

    TODO:
    - Compute the utility for each possible action.
    - Update the regrets for the current information set.
    - Return the expected utility for the current player.
    """
    plays: int = len(history)
    curr_player: int = plays % 2

    # TODO: Add logic for terminal states.
    infoSet = str(cards[curr_player]) + history

    node = KuhnNode()
    node.infoSet = infoSet
    terminalNode = node.returnPayoff(cards) is not None

    if terminalNode:
        payoff = node.returnPayoff(cards)
        if payoff is not None: 
            return float(payoff)

    if infoSet not in nodeMap:
        node = KuhnNode()
        node.infoSet = infoSet
        nodeMap[infoSet] = node
    else:
        node = nodeMap[infoSet]

    # TODO: Compute utilities for each action.
    util: List[float] = [0.0] * NUM_ACTIONS
    strategy = node.getStrategy(p0 if curr_player == 0 else p1)
    nodeUtil: float = 0.0  # weighted average of the cfr of each branch

    for a in range(NUM_ACTIONS):
        nextHistory = history + ("p" if a == 0 else "b")
        if curr_player == 0:
            util[a] = -cfr(cards, nextHistory, p0 * strategy[a], p1)
        else:
            util[a] = -cfr(cards, nextHistory, p0, p1 * strategy[a])
        nodeUtil += strategy[a] * util[a]

    # TODO: Update regrets based on the utilities.
    for a in range(NUM_ACTIONS):
        regret = util[a] - nodeUtil
        node.regretSum[a] += (p1 if curr_player == 0 else p0) * regret
    return float(nodeUtil)

    pass


if __name__ == "__main__":
    start_time: float = time.time()
    train(10**6, "kt-10")
    print("--- %s seconds ---" % (time.time() - start_time))
