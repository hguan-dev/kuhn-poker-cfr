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
    # TODO: Start the main training loop over the specified number of iterations
    #   - Shuffle the deck (use `random.shuffle(cards)`)
    #   - Call the `cfr` function with the current card order, history, and probabilities
    #   - Accumulate the utility returned by `cfr`
    # TODO: Add progress reporting for every N iterations:
    #   - Print the number of iterations completed and the iteration speed
    #   - Calculate and display metrics like game value and exploitability
    # TODO: After training, print the final strategy for all information sets
    # TODO: Save the model (strategy and node data) to a file with the provided name
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

    # TODO: Compute utilities for each action.
    util: List[float] = [0.0] * NUM_ACTIONS

    # TODO: Update regrets based on the utilities.
    pass

if __name__ == '__main__':
    start_time: float = time.time()
    train(10 ** 6, "kt-10")
    print("--- %s seconds ---" % (time.time() - start_time))

