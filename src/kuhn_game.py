from typing import Dict, List
import random
from kuhn_cfr import KuhnCFR
from kuhn_node import Node


class KuhnGame:
    def __init__(self, trained_cfr: KuhnCFR) -> None:
        self.AI: Dict[str, Node] = trained_cfr.nodes
        self.card_map = {0: "J", 1: "Q", 2: "K"}

    def playAI(self, go_first: bool, bankroll: int) -> None:
        """Runs the game loop for AI vs Human"""
        while True:
            cards = [0, 1, 2]
            random.shuffle(cards)
            if bankroll < 0:
                print(f"\nYou have: - ${0 - bankroll}")
            else:
                print(f"\nYou have: ${bankroll}")
            print("=============== Game start ===============")
            player_card = self.card_map[cards[0] if go_first else cards[1]]
            print(f"Your card is: {player_card}")

            game_result = self.gameRecursive(cards, "", go_first)
            bankroll += game_result

            go_first = not go_first

    def gameRecursive(self, cards: List[int], history: str, go_first: bool) -> int:
        """Handles recursive game actions and AI logic"""
        players = ["You", "AI"]
        plays = len(history)
        AI_turn = (plays % 2 == 1) if go_first else (plays % 2 == 0)
        curr_player = plays % 2
        AI_card = self.card_map[cards[1] if go_first else cards[0]]

        if plays > 1:
            terminal_pass = history[-1] == "p"
            double_bet = history[-2:] == "bb"
            player_card = cards[0] if go_first else cards[1]
            ai_card = cards[1] if go_first else cards[0]
            is_player_card_higher = player_card > ai_card

            if terminal_pass:
                if history == "pp":
                    winner = players[0] if is_player_card_higher else players[1]
                    print(f"AI had card {AI_card}. Game ended with history: {history}.")
                    print(f"{winner} won $1.\n")
                    return 1 if is_player_card_higher else -1

                if history[-2] == "b":
                    betting_player = (len(history) - 2) % 2
                    winner = players[betting_player]
                    print(f"AI had card {AI_card}. Game ended with history: {history}.")
                    print(f"{winner} won $1.\n")
                    return 1 if winner == "You" else -1
                else:
                    winner_idx = curr_player
                    winner = players[winner_idx]
                    print(f"AI had card {AI_card}. Game ended with history: {history}.")
                    print(f"{winner} won $1.\n")
                    return 1 if winner == "You" else -1

            if double_bet:
                winner = players[0] if is_player_card_higher else players[1]
                print(f"AI had card {AI_card}. Game ended with history: {history}.")
                print(f"{winner} won $2.\n")
                return 2 if is_player_card_higher else -2

        info_set = str(cards[curr_player]) + history
        if AI_turn:
            if info_set in self.AI:
                AIStrategy = self.AI[info_set].get_average_strategy()
                r = random.random()
                if r < AIStrategy[0]:
                    print("AI checked/passed.\n")
                    return self.gameRecursive(cards, history + "p", go_first)
                else:
                    print("AI bet $1.\n")
                    return self.gameRecursive(cards, history + "b", go_first)
            else:
                action = random.choice(["p", "b"])
                print(f"AI {'checked/passed' if action == 'p' else 'bet $1'}.\n")
                return self.gameRecursive(cards, history + action, go_first)

        while True:
            action = (
                input("Your turn. Enter 'p' for pass/check, 'b' for bet:\n")
                .strip()
                .lower()
            )
            if action in ["p", "b"]:
                break
            print("Invalid input. Please enter 'p' or 'b'.")

        print(f"You {'passed' if action == 'p' else 'bet $1'}.\n")
        return self.gameRecursive(cards, history + action, go_first)


if __name__ == "__main__":
    cfr = KuhnCFR(100000, 3)
    cfr.cfr_iterations_external()
    game = KuhnGame(cfr)
    game.playAI(go_first=False, bankroll=0)
