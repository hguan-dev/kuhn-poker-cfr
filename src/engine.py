import random
from enum import Enum


class Action(Enum):
    CHECK = 1
    BET = 2
    CALL = 3
    FOLD = 4


class Card(Enum):
    J = 1
    Q = 2
    K = 3

    def __lt__(self, o: object) -> bool:
        if not isinstance(o, Card):
            return NotImplemented
        return self.value < o.value

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Card):
            return NotImplemented
        return self.value == o.value

    def __str__(self) -> str:
        return str(self.name)


class Deck:
    def __init__(self) -> None:
        self.cards: None | list[Card] = None

    def shuffle(self) -> None:
        self.cards = [Card.K, Card.Q, Card.J]
        random.shuffle(self.cards)

    def draw(self) -> Card:
        if not self.cards:
            raise AssertionError("The deck must be reshuffled!")
        return self.cards.pop()


class Player:
    def __init__(self) -> None:
        self.score = 0
        self.card = Card.J

    def bet(self) -> None:
        self.score -= 1

    def ante(self, amount: int = 1) -> None:
        self.score -= amount

    def win(self, amount: int) -> None:
        self.score += amount


class Game:
    def __init__(self, ante_amount: int = 1) -> None:
        self.deck = Deck()
        self.players = [Player(), Player()]
        self.pot = 0
        self.ante_amount = ante_amount

    def init_round(self) -> None:
        self.pot = self.ante_amount * 2
        self.deck.shuffle()
        for player in self.players:
            player.card = self.deck.draw()
            player.ante(self.ante_amount)

    def betting_round(self, player: Player, prev_action: Action) -> Action:
        print(f"Player has {str(player.card)}")
        if prev_action == Action.BET:
            a = None
            while a not in ["c", "f", "q"]:
                a = input("Player action (call, fold): ")
            if a == "c":
                print("Player calls")
                player.bet()
                self.pot += 1
                return Action.CALL
            elif a == "f":
                print("Player folds")
                return Action.FOLD
            else:
                exit()
        else:
            a = None
            while a not in ["c", "b", "q"]:
                a = input("Player action (check, bet): ")
            if a == "c":
                print("Player checks")
                return Action.CHECK
            elif a == "b":
                print("Player bets")
                player.bet()
                self.pot += 1
                return Action.BET
            else:
                exit()

    def play_round(self) -> None:
        player_1 = self.players[0]
        player_2 = self.players[1]
        print("\n\nPlayer 1's turn!\n\n")
        a = self.betting_round(player_1, Action.CHECK)
        print("\n\nPlayer 2's turn!\n\n")
        a = self.betting_round(player_2, a)
        if a == Action.FOLD:
            player_1.win(self.pot)
            print(f"\n\nPlayer 1 wins {self.pot}")
            return
        elif a == Action.BET:
            print("\n\nPlayer 1's turn!\n\n")
            a = self.betting_round(player_1, a)
            if a == Action.FOLD:
                player_2.win(self.pot)
                print(f"\n\nPlayer 2 wins {self.pot}")
                return
        if player_1.card > player_2.card:
            player_1.win(self.pot)
            print(
                f"\n\nPlayer 1 wins {self.pot} with {str(player_1.card)} over {str(player_2.card)}"
            )
        else:
            player_2.win(self.pot)
            print(
                f"\n\nPlayer 2 wins {self.pot} with {str(player_2.card)} over {str(player_1.card)}"
            )

    def start_game(self) -> None:
        player_1 = self.players[0]
        player_2 = self.players[1]
        while True:
            a = None
            while a not in ["p", "s", "q"]:
                a = input("\n\nPlay round (p), show stats (s), quit (q): ")
            if a == "q":
                break
            elif a == "p":
                self.init_round()
                self.play_round()
            else:
                print(f"\n\nPlayer 1 score: {player_1.score}")
                print(f"Player 2 score: {player_2.score}\n\n")
