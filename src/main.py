from engine import Game


def main() -> None:
    game = Game()
    print("\nTraining CFR for 100,000 iterations...\n")
    for _ in range(100000):  # Train CFR for 100,000 iterations
        game.init_round()
        game.play_round()

    print("\nFinal Learned Strategies:")
    for info_set, strategy in game.trainer.strategy_sum.items():
        print(f"{info_set}: {game.trainer.get_average_strategy(info_set)}")

if __name__ == "__main__":
    main()
