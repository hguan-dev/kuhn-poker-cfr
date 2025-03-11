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

            outcome = self.playRound(go_first, human_card, ai_card)
            bankroll += outcome

            print(f"New bankroll: ${bankroll}")
            go_first = not go_first
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
        if go_first:
            action1 = input("Enter 'p' to check, or 'b' to bet: ").strip().lower()
            if action1 not in ["p", "b"]:
                print("Invalid input, defaulting to 'p'.")
                action1 = "p"
            if action1 == "b":
                ai_action = self.getAIAction(ai_card, history="b")
                if ai_action == "p":
                    print("AI folds.")
                    return 1
                else:
                    print("AI calls.")
                    print("AI had:", self.card_map[ai_card])
                    return 2 if human_card > ai_card else -2
            else:
                ai_action = self.getAIAction(ai_card, history="p")
                if ai_action == "p":
                    print("AI checks.")
                    print("AI had:", self.card_map[ai_card])
                    return 1 if human_card > ai_card else -1
                else:
                    print("AI bets.")
                    action2 = (
                        input("Enter 'p' to fold, or 'b' to call: ").strip().lower()
                    )
                    if action2 not in ["p", "b"]:
                        print("Invalid input, defaulting to 'b'.")
                        action2 = "b"
                    if action2 == "p":
                        print("You fold.")
                        return -1
                    else:
                        print("AI had:", self.card_map[ai_card])
                        return 2 if human_card > ai_card else -2
        else:
            ai_action = self.getAIAction(ai_card, history="")
            if ai_action == "b":
                print("AI bets.")
                action1 = input("Enter 'p' to fold, or 'b' to call: ").strip().lower()
                if action1 not in ["p", "b"]:
                    print("Invalid input, defaulting to 'b'.")
                    action1 = "b"
                if action1 == "p":
                    print("You fold.")
                    return -1
                else:
                    print("AI had:", self.card_map[ai_card])
                    return 2 if human_card > ai_card else -2
            else:
                print("AI checks.")
                action1 = input("Enter 'p' to check, or 'b' to bet: ").strip().lower()
                if action1 not in ["p", "b"]:
                    print("Invalid input, defaulting to 'p'.")
                    action1 = "p"
                if action1 == "p":
                    print("AI had:", self.card_map[ai_card])
                    return 1 if human_card > ai_card else -1
                else:
                    print("You bet.")
                    ai_response = self.getAIAction(
                        ai_card, history="p" + "b"
                    )
                    if ai_response == "p":
                        print("AI folds.")
                        return 1
                    else:
                        print("AI calls.")
                        print("AI had:", self.card_map[ai_card])
                        return 2 if human_card > ai_card else -2

    def getAIAction(self, ai_card: int, history: str) -> str:
        """
        Determines AI's action using its CFR strategy.
        """
        # Convert 'p' -> '0' and 'b' -> '1' to match CFR format
        history_numeric = "".join(["0" if h == "p" else "1" for h in history])

        # Format history as [0,1] to match CFR training output
        formatted_history = f"[{', '.join(history_numeric)}]" if history_numeric else "[]"
        
        info_set = f"{ai_card}{formatted_history}"
        
        print(f"\n[DEBUG] AI looking up info_set: '{info_set}'")

        if len(self.AI) < 50:  # Avoid excessive prints
            print("[DEBUG] Available AI strategy info_sets:", list(self.AI.keys()))

        if info_set in self.AI:
            strat = self.AI[info_set].get_average_strategy()
            print(f"[DEBUG] Strategy found: {strat}")
            r = random.random()
            return "p" if r < strat[0] else "b"
        else:
            print(f"[DEBUG] ERROR: info_set '{info_set}' NOT FOUND! Falling back to random choice.")
            return random.choice(["p", "b"])

if __name__ == "__main__":
    cfr = KuhnCFR(100000, 3)
    cfr.cfr_iterations_external()
    game = KuhnGame(cfr)
    game.playAI(go_first=False, bankroll=10)
