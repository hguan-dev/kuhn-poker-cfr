import numpy as np


class Node:
    def __init__(self, num_actions: int) -> None:
        self.regret_sum: np.ndarray = np.zeros(num_actions)
        self.strategy: np.ndarray = np.zeros(num_actions)
        self.strategy_sum: np.ndarray = np.zeros(num_actions)
        self.num_actions: int = num_actions

    def get_strategy(self) -> np.ndarray:
        normalizing_sum: float = 0.0
        for a in range(self.num_actions):
            if self.regret_sum[a] > 0:
                self.strategy[a] = self.regret_sum[a]
            else:
                self.strategy[a] = 0
            normalizing_sum += self.strategy[a]

        for a in range(self.num_actions):
            if normalizing_sum > 0:
                self.strategy[a] /= normalizing_sum
            else:
                self.strategy[a] = 1.0 / self.num_actions

        return self.strategy

    def get_average_strategy(self) -> np.ndarray:
        avg_strategy: np.ndarray = np.zeros(self.num_actions)
        normalizing_sum: float = np.sum(self.strategy_sum)

        for a in range(self.num_actions):
            if normalizing_sum > 0:
                avg_strategy[a] = self.strategy_sum[a] / normalizing_sum
            else:
                avg_strategy[a] = 1.0 / self.num_actions

        return avg_strategy
