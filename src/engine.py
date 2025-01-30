import random
from enum import Enum
from cfr_trainer import CFRTrainer


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
        return self.value < o.value if isinstance(o, Card) else NotImplemented

    def __eq__(self, o: object) -> bool:
        return self.value == o.value if isinstance(o, Card) else NotImplemented

    def __str__(self) -> str:
        return str(self.name)


class Deck:
    def __init__(self) -> None:
        self.cards = [Card.K, Card.Q, Card.J]

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def draw(self) -> Card:
        if not self.cards:
            raise AssertionError("The deck must be reshuffled!")
        return self.cards.pop()


class Player:
    def __init__(self, trainer: CFRTrainer) -> None:
        self.score = 0
        self.card = Card.J
        self.trainer = trainer

    def bet(self) -> None:
        self.score -= 1

    def ante(self, amount: int = 1) -> None:
        self.score -= amount

    def win(self, amount: int) -> None:
        self.score += amount

    def choose_action(self, info_set: str) -> Action:
        """
        TODO: Implement CFR-based action selection.
        Currently, this function chooses actions randomly.
        """
        return random.choice(list(Action))


class Game:
    def __init__(self, ante_amount: int = 1) -> None:
        self.deck = Deck()
        self.trainer = CFRTrainer()
        self.players = [Player(self.trainer), Player(self.trainer)]
        self.pot = 0
        self.ante_amount = ante_amount

    def init_round(self) -> None:
        self.pot = self.ante_amount * 2
        self.deck.shuffle()
        for player in self.players:
            player.card = self.deck.draw()
            player.ante(self.ante_amount)

    def betting_round(self, player: Player, prev_action: Action) -> Action:
        info_set = f"{player.card}_{prev_action}"
        action = player.choose_action(info_set)
        print(f"Player ({player.card}) chooses {action}")

        if action == Action.BET or action == Action.CALL:
            player.bet()
            self.pot += 1
        return action

    def play_round(self) -> None:
        player_1, player_2 = self.players
        print("\nPlayer 1's turn!\n")
        a = self.betting_round(player_1, Action.CHECK)
        print("\nPlayer 2's turn!\n")
        a = self.betting_round(player_2, a)

        if a == Action.FOLD:
            player_1.win(self.pot)
            print(f"Player 1 wins {self.pot}")
            return
        elif a == Action.BET:
            print("\nPlayer 1's turn!\n")
            a = self.betting_round(player_1, a)
            if a == Action.FOLD:
                player_2.win(self.pot)
                print(f"Player 2 wins {self.pot}")
                return

        if player_1.card > player_2.card:
            player_1.win(self.pot)
            print(f"Player 1 wins {self.pot} with {player_1.card} over {player_2.card}")
        else:
            player_2.win(self.pot)
            print(f"Player 2 wins {self.pot} with {player_2.card} over {player_1.card}")

    def start_game(self) -> None:
        player_1, player_2 = self.players
        while True:
            a = input("\n\nPlay round (p), show stats (s), quit (q): ").lower()
            if a == "q":
                break
            elif a == "p":
                self.init_round()
                self.play_round()
            else:
                print(f"\nPlayer 1 score: {player_1.score}")
                print(f"Player 2 score: {player_2.score}\n")

