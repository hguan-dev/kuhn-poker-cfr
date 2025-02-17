from typing import List, Dict
from kuhn_node import KuhnNode
from kuhn_game import KuhnGame
from kuhn_test import KuhnTest
import pickle
import random
import time

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

    # Initialize utility tracking variables (e.g., total utility)   
    total_utility = 0.0
    
    # Tracking time to measure iteration speed
    start_time = time.time()
    
    # Define how often we want to print progress
    progress_frequency = 100000
    
    # Add progress reporting for every N iterations:
    for i in range(1, iterations + 1):
        # Shuffle the deck (use `random.shuffle(cards)`)
        random.shuffle(cards)
        
        # Call the `cfr` function with the current card order, history, and probabilities
        iteration_utility = cfr(cards, '', 1.0, 1.0)
        # Accumulate the utility returned by `cfr`
        total_utility += iteration_utility
        
        # Print progress at specified intervals
        if i % progress_frequency == 0:
            elapsed = time.time() - start_time
            if elapsed > 0:
                speed = progress_frequency / elapsed
            else:
                speed = 0.0

            print(f"Iteration {i}/{iterations} completed.")
            print(f"Speed: {speed:.2f} iterations/second")
            
            # Evaluate with KuhnTest
            evaluator = KuhnTest()
            evaluator.nodeMap = nodeMap
            
            # Average game value
            avg_value = evaluator.gameValue()
            print(f"Average game value so far: {avg_value:.4f}")
            
            # Exploitability
            expl = evaluator.exploitability()
            worst_case = expl
            print(f"Exploitability: {worst_case}")
            print(f"Total exploitability: {-sum(expl)}")
            
            # Reset timer for the next batch
            start_time = time.time()
    
        # After training completes, evaluate and print final results
        final_evaluator = KuhnTest()
        final_evaluator.nodeMap = nodeMap
        
        print("\n=== Training Complete ===")
        print("Final Strategy:")
        for node in nodeMap.values():
            print(node)
        
        final_value = final_evaluator.gameValue()
        print(f"\nFinal average game value: {final_value:.4f}")
        
        # Save the trained strategy (nodeMap) to a file
        with open(saveName, 'wb') as f:
            pickle.dump(nodeMap, f)
        
        print(f"Strategy saved to '{saveName}'")

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

    infoSet = str(cards[curr_player]) + history
    # Create a temporary node and check if it's terminal
    temp_node = KuhnNode()
    temp_node.infoSet = infoSet
    payoff = temp_node.returnPayoff(cards)

    # If not terminal, retrieve or create the node from nodeMap.
    if infoSet not in nodeMap:
        nodeMap[infoSet] = KuhnNode()
        nodeMap[infoSet].infoSet = infoSet

    curr_node = nodeMap[infoSet]

    # If there is a payoff (terminal node), return it immediately.
    if payoff is not None:
        return payoff

    # If not terminal, retrieve or create the node from nodeMap.
    if infoSet not in nodeMap:
        nodeMap[infoSet] = KuhnNode()
        nodeMap[infoSet].infoSet = infoSet

    curr_node = nodeMap[infoSet]

    realization_weight = p1 if curr_player == 0 else p0
    strategy = curr_node.getStrategy(realization_weight)

    util: List[float] = [0.0] * NUM_ACTIONS
    nodeUtil: float = 0.0

    for a in range(NUM_ACTIONS):
        nextHistory = history + ('p' if a == 0 else 'b')

        # Recursively call CFR with updated probabilities.
        if curr_player == 0:
            util[a] = -cfr(cards, nextHistory, p0 * strategy[a], p1)
        else:
            util[a] = -cfr(cards, nextHistory, p0, p1 * strategy[a])

        nodeUtil += strategy[a] * util[a]

    # TODO: Update regrets based on the utilities.
    for a in range(NUM_ACTIONS):
        regret = util[a] - nodeUtil
        # Accumulate regret in the node.
        if curr_player == 0:
            curr_node.regretSum[a] += p1 * regret
        else:
            curr_node.regretSum[a] += p0 * regret

    return nodeUtil


if __name__ == "__main__":
    start_time: float = time.time()
    train(10**6, "kt-10")
    print("--- %s seconds ---" % (time.time() - start_time))
