import random
from typing import List, Optional

PASS: int = 0
BET: int = 1
NUM_ACTIONS: int = 2
r: float = random.random()


class KuhnNode:
    def __init__(self) -> None:
        self.infoSet: str = ""
        self.regretSum: List[float] = [0.0] * NUM_ACTIONS
        self.strategy: List[float] = [0.0] * NUM_ACTIONS
        self.strategySum: List[float] = [0.0] * NUM_ACTIONS

    def __str__(self) -> str:
        return self.infoSet + " " + ", ".join(str(e) for e in self.getAverageStrategy())

    def getStrategy(self, realization_weight: float) -> List[float]:
        """
        Update the current information set mixed strategy through regret-matching.

        Args:
            realization_weight (float): Realization weight for updating the strategy sum.

        Returns:
            List[float]: Updated strategy for the node.
        """
        normalizingSum: float = 0.0
        for a in range(NUM_ACTIONS):
            if self.regretSum[a] > 0:
                self.strategy[a] = self.regretSum[a]
            else:
                self.strategy[a] = 0.0
            normalizingSum += self.strategy[a]

        for a in range(NUM_ACTIONS):
            if normalizingSum > 0:
                self.strategy[a] /= normalizingSum
            else:
                self.strategy[a] = 1.0 / NUM_ACTIONS
            self.strategySum[a] += realization_weight * self.strategy[a]
        return self.strategy

    def getAverageStrategy(self) -> List[float]:
        """
        Get the average information set mixed strategy across all training iterations.

        Returns:
            List[float]: Average strategy over all iterations.
        """
        avgStrategy: List[float] = [0.0] * NUM_ACTIONS
        normalizingSum: float = sum(self.strategySum)

        for a in range(NUM_ACTIONS):
            if normalizingSum > 0:
                avgStrategy[a] = self.strategySum[a] / normalizingSum
            else:
                avgStrategy[a] = 1.0 / NUM_ACTIONS

        for a in range(NUM_ACTIONS):
            if avgStrategy[a] < 0.01:
                avgStrategy[a] = 0.0

        normalizingSum = sum(avgStrategy)
        for a in range(NUM_ACTIONS):
            if normalizingSum > 0:
                avgStrategy[a] /= normalizingSum

        return avgStrategy

    def returnPayoff(self, cards: List[int]) -> Optional[int]:
        """
        Calculate the payoff for terminal states.

        Args:
            cards (List[int]): List of cards held by the players.

        Returns:
            Optional[int]: The payoff value for terminal states, or None if not terminal.
        """
        history: str = self.infoSet[1:]
        plays: int = len(history)
        curr_player: int = plays % 2
        opponent: int = 1 - curr_player

        # Return payoff for terminal states
        if plays > 1:
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

        return None
