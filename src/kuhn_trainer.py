from typing import List, Dict
from kuhn_node import KuhnNode
from kuhn_test import KuhnTest
import random
import time
import pickle

NUM_ACTIONS: int = 2
nodeMap: Dict[str, KuhnNode] = {}
action = ["p", "b"]

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
    cards: List[int] = [1, 2, 3]
    # TODO: Initialize utility tracking variables (e.g., total utility)
    total_utility: float = 0.0 

    # TODO: Start the main training loop over the specified number of iterations
    #   - Shuffle the deck (use `random.shuffle(cards)`)
    #   - Call the `cfr` function with the current card order, history, and probabilities
    #   - Accumulate the utility returned by `cfr`
    for i in range(iterations):
        random.shuffle(cards)
        total_utility += cfr(cards, "", 1.0, 1.0)

    # TODO: Add progress reporting for every N iterations:
    #   - Print the number of iterations completed and the iteration speed
    #   - Calculate and display metrics like game value and exploitability
        if (i + 1) % 100000 == 0:
            test = KuhnTest()
            test.nodeMap = nodeMap
            print(f'Average game value: {test.gameValue()}')
            print(f'Exploitability: {sum(test.exploitability())}')
    
    # TODO: After training, print the final strategy for all information sets
    print("\nFinal Strategy:")
    for infoSet, node in sorted(nodeMap.items()):
        print(f"{infoSet}: {node.getAverageStrategy()}")

    # TODO: Save the model (strategy and node data) to a file with the provided name
    with open(saveName, "wb") as f:
        pickle.dump(nodeMap, f)

    return

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

    # Check for terminal states
    if plays > 1:
        terminalPass: bool = history[-1] == "p"
        doubleBet: bool = history[-2:] == "bb"
        isPlayerCardHigher: bool = cards[curr_player] > cards[1 - curr_player]

        if terminalPass:
            if history == "pp":
                return 1 if isPlayerCardHigher else -1
            else:
                return 1
        if doubleBet:
            return 2 if isPlayerCardHigher else -2

    # Get the current information set
    infoSet: str = str(cards[curr_player]) + history
    if infoSet not in nodeMap:
        nodeMap[infoSet] = KuhnNode()

    node: KuhnNode = nodeMap[infoSet]

    strategy: List[float] = node.getStrategy(p0 if curr_player == 0 else p1) # Get the current strategy
    util: List[float] = [0.0] * NUM_ACTIONS
    nodeUtil: float = 0.0

    # Compute utilities for each action
    for a in range(NUM_ACTIONS):
        nextHistory: str = history + ("p" if a == 0 else "b")
        if curr_player == 0:
            util[a] = -cfr(cards, nextHistory, p0 * strategy[a], p1)
        else:
            util[a] = -cfr(cards, nextHistory, p0, p1 * strategy[a])
        nodeUtil += strategy[a] * util[a]

    for a in range(NUM_ACTIONS):
        regret: float = util[a] - nodeUtil
        node.regretSum[a] += (p1 if curr_player == 0 else p0) * regret # Update regrets

    return nodeUtil


if __name__ == "__main__":
    start_time: float = time.time()
    train(10**6, "kt-10")
    print("--- %s seconds ---" % (time.time() - start_time))
    