import numpy as np
import random
from kuhn_node import Node
from typing import List, Dict


class KuhnCFR:
    #initialization of the game parameters
    def __init__(self, iterations: int, decksize: int) -> None:
        self.iterations: int = iterations
        self.decksize: int = decksize #3 for kuhn poker, J Q K
        self.cards: List[int] = list(np.arange(decksize))
        self.bet_options: int = 2
        self.nodes: Dict[str, Node] = {}

    #Run CFR algorithm for the specified number of iterations
    #For each interation: The deck is shuffled, two cards dealt to players, external_cfr called to compute utility for each player
        #After all interations: print average game value and final average strategy
            #average strategy: p(each action (pass/bet)for every possible infoset)
    def cfr_iterations_external(self) -> None:
        util: np.ndarray = np.zeros(2)
        for t in range(1, self.iterations + 1):
            for i in range(2):
                random.shuffle(self.cards)
                util[i] += self.external_cfr(self.cards[:2], [], 2, 0, i, t)
        print("Average game value: {:.4f}".format(util[0] / self.iterations))
        print("\nFinal Average Strategy:")
        print("-----------------------")
        card_map = {0: "J", 1: "Q", 2: "K"}
        for infoset in sorted(self.nodes):
            card, history = int(infoset[0]), infoset[1:]
            avg_strategy = self.nodes[infoset].get_average_strategy()
            actions = ["Pass", "Bet"]
            history_str = self.format_history(history)
            strategy_str = ", ".join(
                [
                    f"{actions[i]}: {avg_strategy[i]:.2f}"
                    for i in range(self.bet_options)
                ]
            )
            print(f"Card: {card_map[card]}, History: {history_str} -> {strategy_str}")
    
    #The core of this implementation of the CFR algo: basically it recursively traverse the game tree,
        #compute utilities, and then update regrets hence strategies
    def format_history(self, history: str) -> str:
        action_map = {"0": "P", "1": "B"}
        return "".join(action_map.get(h, h) for h in history)

    def external_cfr(
        self,
        cards: List[int],
        history: List[int],
        pot: int,
        nodes_touched: int,
        traversing_player: int,
        t: int,
    ) -> float:
        plays: int = len(history) #number of actions taken so far
        acting_player: int = plays % 2 #determine player 0 or player 1
        opponent_player: int = 1 - acting_player

         #This following section handles the terminal states in a game
        if plays >= 2:
            if history[-1] == 0 and history[-2] == 1:  #1st scenario: Bet fold, whoever acts wins because the other folds
                if acting_player == traversing_player: #we are calculating the util of traversing_player
                    return 1.0
                else:
                    return -1.0
            if (history[-1] == 0 and history[-2] == 0) or (
                history[-1] == 1 and history[-2] == 1
            ): #2nd Scenario: Showdown (either both pass or both bet)
                if acting_player == traversing_player:
                    if cards[acting_player] > cards[opponent_player]:
                        #pot is divided by 2 because each player contributes equally to the pot (winner gains half the pot and vice versa)
                        return pot / 2.0  #utility is positive because traversing player won
                    else:
                        return -pot / 2.0  
                else:
                    if cards[acting_player] > cards[opponent_player]:
                        return -pot / 2.0 #utility is negative becasue the opponent player won
                    else:
                        return pot / 2.0

        infoset: str = str(cards[acting_player]) + str(history)
        if infoset not in self.nodes:
            self.nodes[infoset] = Node(self.bet_options) #Create a new node if infoset doesn't exist
            #Infoset: unique combination of player's card and the current history (for example, if p1 has 0 and history is [0,1], infoset is 001)


        nodes_touched += 1 #record number of nodes that has been iterated through

        #This following section handles when it's traversing player's turn and when it's the opponent's turn
        if acting_player == traversing_player:
            utility: np.ndarray = np.zeros(self.bet_options) #initiate utility array for each action
            node_util: float = 0.0 #total utility for the current node
            current_strategy: np.ndarray = self.nodes[infoset].get_strategy()
            for a in range(self.bet_options):
                next_history = history + [a]
                next_pot = pot + a
                utility[a] = self.external_cfr(
                    cards, next_history, next_pot, nodes_touched, traversing_player, t
                ) #compute utility (call cfr function) for the next state recursively
                node_util += current_strategy[a] * utility[a] #update total util by weighting util of each action by its p in current strategy


            for a in range(self.bet_options):
                regret = utility[a] - node_util  #Regret = utility of an action and total utility
                self.nodes[infoset].regret_sum[a] += regret #now regret is computed, add it to the infoset so it can be use to update strategy
            return node_util

        else:
            opponent_strategy: np.ndarray = self.nodes[infoset].get_strategy()
            if random.random() < opponent_strategy[0]: #a sample opponent's action that is random
                next_history = history + [0] #0 means opponent chose to pass
                next_pot = pot
            else:
                next_history = history + [1] #1 meanas opponent chose to bet
                next_pot = pot + 1 #add it to the pot
            util: float = self.external_cfr(
                cards, next_history, next_pot, nodes_touched, traversing_player, t
            ) #Same as traversing player, recursively call cfr function to compute utility 
            for a in range(self.bet_options):
                self.nodes[infoset].strategy_sum[a] += opponent_strategy[a] #Add opponent's straetegy to infoset, then used to compute the average strategy over all iterations
            return util
