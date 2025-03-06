import random
from typing import Dict
from kuhn_cfr import KuhnCFR
from kuhn_node import Node

class KuhnGame:
    def __init__(self, trained_cfr: KuhnCFR) -> None:
        self.AI: Dict[str, Node] = trained_cfr.nodes
        self.card_map = {0: "J", 1: "Q", 2: "K"}
    
    def playAI(self, go_first: bool, bankroll: int) -> None:
        """Play successive rounds until the human runs out of money."""
        while bankroll > 0:
            # Shuffle and deal cards.
            cards = [0, 1, 2]
            random.shuffle(cards)
            if go_first:
                human_card, ai_card = cards[0], cards[1]
            else:
                ai_card, human_card = cards[0], cards[1]
            
            print("\n=============== New Round ===============")
            print(f"You have: ${bankroll}")
            print(f"Your card is: {self.card_map[human_card]}")
            
            # Play a round and get the net outcome.
            outcome = self.playRound(go_first, human_card, ai_card)
            bankroll += outcome
            
            print(f"New bankroll: ${bankroll}")
            go_first = not go_first  # alternate who goes first
        print("Game over. You're broke.")
    
    def playRound(self, go_first: bool, human_card: int, ai_card: int) -> int:
        """
        Plays one round in a linear, nonrecursive manner.
        Returns the net change to the human’s bankroll:
          +1 for winning a fold,
          +1 for winning a check–showdown,
          +2 for winning a bet–call showdown,
          or the negative of those amounts if losing.
        """
        # Case 1: Human acts first.
        if go_first:
            action1 = input("Enter 'p' to check, or 'b' to bet: ").strip().lower()
            if action1 not in ["p", "b"]:
                print("Invalid input, defaulting to 'p'.")
                action1 = "p"
            if action1 == "b":
                # Human bets.
                # Now AI must respond in active mode: "p" = fold, "b" = call.
                ai_action = self.getAIAction(ai_card, history="b", active=True)
                if ai_action == "p":
                    print("AI folds.")
                    # Human wins the bet; net gain: +1.
                    return 1
                else:
                    print("AI calls.")
                    print("AI had:", self.card_map[ai_card])
                    # Showdown with pot = 4.
                    return 2 if human_card > ai_card else -2
            else:
                # Human checks.
                # AI acts in non-active mode.
                ai_action = self.getAIAction(ai_card, history="p", active=False)
                if ai_action == "p":
                    print("AI checks.")
                    # showdown with pot = 2.
                    print("AI had:", self.card_map[ai_card])
                    return 1 if human_card > ai_card else -1
                else:
                    print("AI bets.")
                    # Now human responds in active mode.
                    action2 = input("Enter 'p' to fold, or 'b' to call: ").strip().lower()
                    if action2 not in ["p", "b"]:
                        print("Invalid input, defaulting to 'b'.")
                        action2 = "b"
                    if action2 == "p":
                        print("You fold.")
                        return -1
                    else:
                        # Call → showdown with pot = 4.
                        print("AI had:", self.card_map[ai_card])
                        return 2 if human_card > ai_card else -2
        # Case 2: AI acts first.
        else:
            ai_action = self.getAIAction(ai_card, history="", active=False)
            if ai_action == "b":
                print("AI bets.")
                # Human response in active mode.
                action1 = input("Enter 'p' to fold, or 'b' to call: ").strip().lower()
                if action1 not in ["p", "b"]:
                    print("Invalid input, defaulting to 'b'.")
                    action1 = "b"
                if action1 == "p":
                    print("You fold.")
                    return -1
                else:
                    # Call → showdown with pot = 4.
                    print("AI had:", self.card_map[ai_card])
                    return 2 if human_card > ai_card else -2
            else:
                print("AI checks.")
                # Human acts in non-active mode.
                action1 = input("Enter 'p' to check, or 'b' to bet: ").strip().lower()
                if action1 not in ["p", "b"]:
                    print("Invalid input, defaulting to 'p'.")
                    action1 = "p"
                if action1 == "p":
                    # Both checked.
                    print("AI had:", self.card_map[ai_card])
                    return 1 if human_card > ai_card else -1
                else:
                    print("You bet.")
                    # Now AI responds in active mode.
                    ai_response = self.getAIAction(ai_card, history="p" + "b", active=True)
                    if ai_response == "p":
                        print("AI folds.")
                        return 1
                    else:
                        print("AI calls.")
                        print("AI had:", self.card_map[ai_card])
                        return 2 if human_card > ai_card else -2

    def getAIAction(self, ai_card: int, history: str, active: bool) -> str:
        """
        Determines AI's action using its CFR strategy.
        The info-set is defined as the AI's card (as a letter) concatenated with the history.
        In non-active mode, "p" means check and "b" means bet.
        In active mode, "p" means fold and "b" means call.
        """
        info_set = self.card_map[ai_card] + history
        if info_set in self.AI:
            strat = self.AI[info_set].get_average_strategy()  # e.g., [prob_p, prob_b]
            r = random.random()
            # Same mapping for active and non-active: strategy[0] is for "p".
            return "p" if r < strat[0] else "b"
        else:
            return random.choice(["p", "b"])

if __name__ == "__main__":
    cfr = KuhnCFR(100000, 3)
    cfr.cfr_iterations_external()
    game = KuhnGame(cfr)
    game.playAI(go_first=False, bankroll=10)

