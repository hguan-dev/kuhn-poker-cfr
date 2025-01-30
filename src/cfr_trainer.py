import numpy as np
from collections import defaultdict
from engine import Action


class CFRTrainer:

    def __init__(self) -> None:
        """
        Initializes regret and strategy storage.

        TODO:
        - Initialize `self.regret_sum` to store regret values for each game state.
        - Initialize `self.strategy_sum` to store cumulative strategies.
        """
        pass  # TODO: Implement initialization logic

    def get_strategy(self, info_set: str) -> np.ndarray:
        """
        Returns an action probability distribution using regret matching.

        TODO:
        - Retrieve regrets for the given `info_set`.
        - Convert regrets into a probability distribution.
        - If all regrets are negative, return a uniform strategy.

        Args:
            info_set (str): The game state (e.g., "J_CHECK").
        
        Returns:
            np.array: Action probability distribution.
        """
        pass  # TODO: Implement regret matching

    def get_average_strategy(self, info_set: str) -> np.ndarray:
        """
        Returns the average strategy learned over all training iterations.

        TODO:
        - Normalize the cumulative strategy sums.
        - Return the average strategy.

        Args:
            info_set (str): The game state.

        Returns:
            np.array: Average action probability distribution.
        """
        pass  # TODO: Implement average strategy computation

    def update_regrets(self, info_set: str, chosen_action: Action, regret: float):
        """
        Updates regret values for a given information set.

        TODO:
        - Find the index of `chosen_action` in the list of actions.
        - Update regret sums based on the received `regret` value.

        Args:
            info_set (str): The game state.
            chosen_action (Action): The action that was chosen.
            regret (float): The regret value to add.
        """
        pass  # TODO: Implement regret update logic

