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

    def gameValue(self) -> float:
        value = 0.0
        cardList = [[1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2]]

        def valueRecursive(infoSet: str) -> Optional[int]:
            if infoSet not in self.nodeMap:
                node = KuhnNode()
                node.infoSet = infoSet
                return node.returnPayoff(cards)
            else:
                curr_player = (len(infoSet) - 1) % 2
                other = 1 - curr_player
                otherInfo = str(cards[other]) + infoSet[1:]
                strategy = self.nodeMap[infoSet].getAverageStrategy()
                value = 0.0
                for a in range(2):
                    if a == 0:
                        value += -valueRecursive(otherInfo + 'p') * strategy[a]
                    else:
                        value += -valueRecursive(otherInfo + 'b') * strategy[a]
                return value

        for cards in cardList:
            value += valueRecursive(str(cards[0])) / 6
        return value

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

    def prune(self, threshold: float) -> None:
        for item in self.nodeMap:
            self.nodeMap[item].promising_branches = list(range(2))
            for i in range(2):
                if self.nodeMap[item].regretSum[i] < threshold:
                    self.nodeMap[item].promising_branches.remove(i)

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

