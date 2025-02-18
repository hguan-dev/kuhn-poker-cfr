import random
from typing import Dict, List
from kuhn_node import KuhnNode


class KuhnTest:
    def __init__(self) -> None:
        self.nodeMap: Dict[str, KuhnNode] = buildAverageStrategy()

    def test_play(self, testNodeMap: Dict[str, KuhnNode], history: str) -> float:
        cards = [1, 2, 3]
        random.shuffle(cards)
        plays = len(history)
        curr_player = plays % 2
        opponent = 1 - curr_player

        # Return payoff for terminal states
        if plays > 1:
            terminalPass = history[plays - 1] == "p"
            doubleBet = history[plays - 2 : plays] == "bb"
            isPlayerCardHigher = cards[curr_player] > cards[opponent]
            if terminalPass:
                if history == "pp":
                    return 1.0 if isPlayerCardHigher else -1.0
                else:
                    return 1.0
            if doubleBet:
                return 2.0 if isPlayerCardHigher else -2.0

        # Keep playing if not terminal state
        infoSet = str(cards[curr_player]) + history
        if infoSet not in self.nodeMap or infoSet not in testNodeMap:
            return 0.0  # Ensure valid return

        curr_strategy = (
            self.nodeMap[infoSet].getAverageStrategy()
            if curr_player == 0
            else testNodeMap[infoSet].getAverageStrategy()
        )
        r = random.random()
        return (
            -self.test_play(testNodeMap, history + "p")
            if r < curr_strategy[0]
            else -self.test_play(testNodeMap, history + "b")
        )

    def gameValue(self) -> float:
        value = 0.0
        cardList = [[1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2]]

        def valueRecursive(infoSet: str) -> float:
            if infoSet not in self.nodeMap:
                node = KuhnNode()
                node.infoSet = infoSet
                payoff = node.returnPayoff(cards)
                return payoff if payoff is not None else 0.0
                # return (
                #     node.returnPayoff(cards)
                #     if node.returnPayoff(cards) is not None
                #     else 0.0
                # )

            curr_player = (len(infoSet) - 1) % 2
            other = 1 - curr_player
            otherInfo = str(cards[other]) + infoSet[1:]
            strategy = self.nodeMap[infoSet].getAverageStrategy()
            value = 0.0

            for a in range(2):
                recursive_value = valueRecursive(otherInfo + ("p" if a == 0 else "b"))
                value += -recursive_value * strategy[a]

            return value

        for cards in cardList:
            value += valueRecursive(str(cards[0])) / 6
        return value

    def exploitability(self) -> List[float]:
        gt = self.best_response()
        output = [0.0, 0.0]
        for c in range(1, 4):
            output[0] += gt[str(c)]["ev"] / 3
            output[1] -= gt[str(c)]["br"] / 3
        return output

    def best_response(self) -> Dict[str, Dict[str, float]]:
        def traverseRecursive(
            history: str,
            reachProb: Dict[str, float],
            gameTree: Dict[str, Dict[str, float]],
        ) -> Dict[str, Dict[str, float]]:
            curr_player = len(history) % 2
            other_player = 1 - curr_player
            childCards = {"1": ["2", "3"], "2": ["1", "3"], "3": ["1", "2"]}
            possibleCards = ["1", "2", "3"]

            for next_move in ["p", "b"]:
                a = ["p", "b"].index(next_move)
                if isTerminal(history + next_move):
                    for card in possibleCards:
                        br_temp, ev_temp, npEV, npBR = 0.0, 0.0, 0.0, 0.0
                        for other in childCards[card]:
                            evCards = (
                                [int(card), int(other)]
                                if curr_player == 1
                                else [int(other), int(card)]
                            )
                            brCards = (
                                [int(card), int(other)]
                                if curr_player == 0
                                else [int(other), int(card)]
                            )
                            evRP = other + str(curr_player)
                            brRP = other + str(other_player)

                            evNextNode = KuhnNode()
                            evNextNode.infoSet = card + history + next_move
                            evCurrNode = self.nodeMap.get(other + history)
                            if evCurrNode is not None:
                                strategy_value = evCurrNode.getAverageStrategy()[a]
                                payoff = evNextNode.returnPayoff(evCards) or 0.0
                                ev_temp += reachProb[evRP] * strategy_value * (-payoff)
                            npEV += reachProb[evRP]

                            brNextNode = KuhnNode()
                            brNextNode.infoSet = other + history + next_move
                            payoff = brNextNode.returnPayoff(brCards) or 0.0
                            br_temp += reachProb[brRP] * (-payoff)
                            npBR += reachProb[brRP]

                        if npEV != 0:
                            ev_temp /= npEV
                        gameTree[card + history]["ev"] += ev_temp

                        if npBR != 0:
                            br_temp /= npBR
                        gameTree[card + history]["br"] = max(
                            gameTree[card + history].get("br", br_temp), br_temp
                        )
                else:
                    gameTree = traverseRecursive(
                        history + next_move, reachProb, gameTree
                    )

            return gameTree

        rp = {f"{card}{p}": 1.0 for card in ["1", "2", "3"] for p in ["0", "1"]}
        return traverseRecursive("", rp, buildFullTree())


def isTerminal(history: str) -> bool:
    return history in ["pp", "pbp", "pbb", "bp", "bb"]


def buildFullTree() -> Dict[str, Dict[str, float]]:
    return {
        f"{card}{strategy}": {"ev": 0.0, "br": 0.0}
        for card in ["1", "2", "3"]
        for strategy in ["", "p", "b", "pb"]
    }


def buildAverageStrategy() -> Dict[str, KuhnNode]:
    nodeMap = {}
    for card in range(1, 4):
        for strategy in ["", "p", "b", "pb"]:
            infoSet = str(card) + strategy
            curr_node = KuhnNode()
            curr_node.infoSet = infoSet
            nodeMap[infoSet] = curr_node
    return nodeMap


if __name__ == "__main__":
    kt = KuhnTest()
    print(kt.gameValue())
    print(kt.exploitability())
