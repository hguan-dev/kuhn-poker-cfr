import random
from typing import Dict, List, Optional
from kuhn_node import KuhnNode

class KuhnTest:
    def __init__(self) -> None:
        self.nodeMap: Dict[str, KuhnNode] = buildAverageStrategy()

    # Plays the game against the strategy testNodeMap from a given history,
    # returns the utility of playing the simulated game.
    def test_play(self, testNodeMap: Dict[str, KuhnNode], history: str) -> int:
        cards = [1, 2, 3]
        random.shuffle(cards)
        plays = len(history)
        curr_player = plays % 2
        opponent = 1 - curr_player

        # Return payoff for terminal states
        if plays > 1:
            terminalPass = history[plays - 1] == 'p'
            doubleBet = history[plays - 2: plays] == 'bb'
            isPlayerCardHigher = cards[curr_player] > cards[opponent]
            if terminalPass:
                if history == 'pp':
                    return 1 if isPlayerCardHigher else -1
                else:
                    return 1
            if doubleBet:
                return 2 if isPlayerCardHigher else -2

        # Keep playing if not terminal state
        infoSet = str(cards[curr_player]) + history
        if curr_player == 0:
            curr_strategy = self.nodeMap[infoSet].getAverageStrategy()
        else:
            curr_strategy = testNodeMap[infoSet].getAverageStrategy()
        r = random.random()
        if r < curr_strategy[0]:
            return -self.test_play(testNodeMap, history + 'p')
        else:
            return -self.test_play(testNodeMap, history + 'b')

    def valueRecursive(self, infoSet: str, cards: List[int]) -> float:
        NUM_ACTIONS = 2
        """
        Recursive helper function to compute the value of the game tree from a given state.

        Args:
            infoSet (str): The current information set (e.g., "1p" or "2b").
            cards (List[int]): The card distribution between the players.

        Returns:
            float: The expected value of the game from this state for player 1.
        """

        # TODO 1: Check if the current state is terminal (e.g., "pp", "pbp", "pbb", "bp", "bb").
        #         If it is terminal, return the payoff for the current state.
        if infoSet not in self.nodeMap:
            node = KuhnNode()
            node.infoSet = infoSet
            return node.returnPayoff(cards)

        # TODO 2: Determine the current player based on the length of the infoSet.
        #         Even number of actions -> player 1's turn, odd number -> player 2's turn.
        curr_player: int = len(infoSet) % 2

        # TODO 3: Calculate the value of the game by iterating over all possible actions.
        #         Use the player's strategy to weight the value of each branch.
        value: float = 0.0
        strategy: List[float] = self.nodeMap[infoSet].getAverageStrategy()

        for action in range(NUM_ACTIONS):  # Actions: PASS (0), BET (1)
            # TODO 3.1: Generate the new information set by appending the action to the current infoSet.
            next_infoSet: str = infoSet + ('p' if action == 0 else 'b')

            # TODO 3.2: Recursively calculate the value of the next state.
            #           Flip the sign because the value for one player is the negative for the other.
            next_value: float = -self.valueRecursive(next_infoSet, cards)

            # TODO 3.3: Multiply the value by the probability of taking the action (strategy[action]).
            value += strategy[action] * next_value

        # TODO 4: Return the calculated value for the current state.
        return value


    def gameValue(self) -> float:
        """
        Compute the expected utility for player 1 over all possible games.
        This includes:
        1. Enumerating all possible card distributions between two players.
        2. Recursively evaluating the value of each game path.
        3. Averaging the results over all distributions.
        """

        # TODO 1: Initialize the total game value.
        #         This will accumulate the expected utility for player 1 across all card distributions.
        total_value: float = 0.0

        # TODO 2: Define all possible card distributions for two players.
        #         Each card is unique, and player 1 and player 2 receive one card each.
        card_distributions: List[List[int]] = [[1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2]]

        # TODO 3: Loop over each card distribution.
        for cards in card_distributions:
            # TODO 3.1: Set the initial information set for player 1 based on their card.
            #           Example: If player 1 has card 1, their initial infoSet is "1".
            initial_infoSet: str = str(cards[0])

            # TODO 3.2: Call a recursive helper function (e.g., `valueRecursive`) to calculate
            #           the expected utility of the game starting with this distribution.
            #           Pass the initial information set as an argument.
            game_value: float = self.valueRecursive(initial_infoSet, cards)

            # TODO 3.3: Add the result of the recursive function to the total game value.
            #           Divide by the number of distributions to compute the average later.
            total_value += game_value / len(card_distributions)

        # TODO 4: Return the total game value as the final result.
        return total_value


    def exploitability(self) -> List[float]:
        gt = self.best_response()
        output = [0.0, 0.0]
        for c in range(1, 4):
            output[0] += gt[str(c)]['ev'] / 3
            output[1] -= gt[str(c)]['br'] / 3
        return output

    def best_response(self) -> Dict[str, Dict[str, float]]:
        def traverseRecursive(history: str, reachProb: Dict[str, float], gameTree: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, float]]:
            curr_player = len(history) % 2
            other_player = 1 - curr_player
            childCards = {"1": ["2", "3"], "2": ["1", "3"], "3": ["1", "2"]}
            possibleCards = ["1", "2", "3"]

            for next_move in ['p', 'b']:
                a = ['p', 'b'].index(next_move)
                if isTerminal(history + next_move):
                    for card in possibleCards:
                        br_temp, ev_temp, npEV, npBR = 0.0, 0.0, 0.0, 0.0
                        for other in childCards[card]:
                            evCards = [int(card), int(other)] if curr_player == 1 else [int(other), int(card)]
                            brCards = [int(card), int(other)] if curr_player == 0 else [int(other), int(card)]
                            evRP = other + str(curr_player)
                            brRP = other + str(other_player)
                            evNextNode = KuhnNode()
                            evNextNode.infoSet = card + history + next_move
                            evCurrNode = self.nodeMap[other + history]
                            ev_temp += reachProb[evRP] * evCurrNode.getAverageStrategy()[a] * (-evNextNode.returnPayoff(evCards))
                            npEV += reachProb[evRP]
                            brNextNode = KuhnNode()
                            brNextNode.infoSet = other + history + next_move
                            br_temp += reachProb[brRP] * (-brNextNode.returnPayoff(brCards))
                            npBR += reachProb[brRP]
                        if npEV != 0: ev_temp /= npEV
                        gameTree[card + history]['ev'] += ev_temp
                        if npBR != 0: br_temp /= npBR
                        if 'br' not in gameTree[card + history]:
                            gameTree[card + history]['br'] = br_temp
                        else:
                            gameTree[card + history]['br'] = max(gameTree[card + history]['br'], br_temp)
                else:
                    newRP = {}
                    for card in possibleCards:
                        currNode = self.nodeMap[card + history]
                        if curr_player == 0:
                            newRP[card + '0'] = reachProb[card + '0'] * currNode.getAverageStrategy()[a]
                            newRP[card + '1'] = reachProb[card + '1']
                        else:
                            newRP[card + '0'] = reachProb[card + '0']
                            newRP[card + '1'] = reachProb[card + '1'] * currNode.getAverageStrategy()[a]
                    gameTree = traverseRecursive(history + next_move, newRP, gameTree)
                    for card in possibleCards:
                        ev_temp = 0.0
                        if 'br' not in gameTree[card + history]:
                            gameTree[card + history]['br'] = -gameTree[card + history + next_move]['ev']
                        else:
                            gameTree[card + history]['br'] = max(gameTree[card + history]['br'], -gameTree[card + history + next_move]['ev'])
                        npEV = 0.0
                        for other in childCards[card]:
                            currNode = self.nodeMap[other + history]
                            evRP = other + str(curr_player)
                            npEV += reachProb[evRP]
                            ev_temp += reachProb[evRP] * currNode.getAverageStrategy()[a] * -gameTree[card + history + next_move]['br']
                        if npEV != 0: ev_temp /= npEV
                        gameTree[card + history]['ev'] += ev_temp
            return gameTree

        rp = {f"{card}{p}": 1.0 for card in ['1', '2', '3'] for p in ['0', '1']}
        return traverseRecursive('', rp, buildFullTree())

def isTerminal(history: str) -> bool:
    return history in ['pp', 'pbp', 'pbb', 'bp', 'bb']

def buildFullTree() -> Dict[str, Dict[str, float]]:
    nodeMap = {}
    for card in range(1, 4):
        infoSet = str(card)
        for strategy in ['', 'p', 'b', 'pb']:
            IS = infoSet + strategy
            nodeMap[IS] = {'ev': 0.0}
    return nodeMap

def buildAverageStrategy() -> Dict[str, KuhnNode]:
    nodeMap = {}
    for card in range(1, 4):
        history = str(card)
        infoSet = history
        curr_node = KuhnNode()
        curr_node.infoSet = infoSet
        nodeMap[infoSet] = curr_node
        for strategy in ['p', 'b', 'pb']:
            infoSet = history + strategy
            curr_node = KuhnNode()
            curr_node.infoSet = infoSet
            nodeMap[infoSet] = curr_node
    return nodeMap

if __name__ == '__main__':
    kt = KuhnTest()
    exp = kt.best_response()
    print(kt.gameValue())
    print(kt.exploitability())
    print(exp)

