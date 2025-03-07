import unittest
from unittest.mock import patch, MagicMock
from src.kuhn_cfr import KuhnCFR
from src.kuhn_game import KuhnGame

class TestKuhnGame(unittest.TestCase):
    cfr: KuhnCFR
    game: KuhnGame

    @classmethod
    def setUpClass(cls) -> None:
        """Train a CFR AI once for use in all tests."""
        cls.cfr = KuhnCFR(100000, 3)
        cls.cfr.cfr_iterations_external()
        cls.game = KuhnGame(cls.cfr)

    def test_ai_action_selection(self) -> None:
        """Ensure AI selects actions based on trained strategy."""
        ai_card = 2  # AI has 'K'
        history = "b"  # Simulate a previous bet
        action = self.game.getAIAction(ai_card, history)
        self.assertIn(action, ["p", "b"], "AI action should be 'p' or 'b'")

    @patch("builtins.input", side_effect=["p"])  # Human checks
    def test_play_round_human_checks(self, _mock_input: MagicMock) -> None:
        """Test a round where the human checks."""
        human_card, ai_card = 1, 2  # Q vs K
        result = self.game.playRound(go_first=True, human_card=human_card, ai_card=ai_card)
        self.assertIn(result, [-1, 1], "Outcome should be a check showdown")

    @patch("builtins.input", side_effect=["b", "b"])  # Human bets, AI calls
    def test_play_round_human_bets_ai_calls(self, _mock_input: MagicMock) -> None:
        """Test a round where the human bets and AI calls."""
        human_card, ai_card = 2, 1  # K vs Q
        result = self.game.playRound(go_first=True, human_card=human_card, ai_card=ai_card)
        self.assertIn(result, [-2, 2], "Outcome should be a bet-call showdown")

    @patch("builtins.input", side_effect=["b", "p"])  # Human bets, AI folds
    def test_play_round_human_bets_ai_folds(self, _mock_input: MagicMock) -> None:
        """Test a round where the human bets and AI folds."""
        human_card, ai_card = 0, 2  # J vs K
        result = self.game.playRound(go_first=True, human_card=human_card, ai_card=ai_card)
        self.assertEqual(result, 1, "Human should win if AI folds")

    @patch("builtins.input", side_effect=["b", "p"])  # AI bets, human folds
    def test_play_round_ai_bets_human_folds(self, _mock_input: MagicMock) -> None:
        """Test a round where the AI bets and human folds."""
        human_card, ai_card = 0, 2  # J vs K
        result = self.game.playRound(go_first=False, human_card=human_card, ai_card=ai_card)
        self.assertEqual(result, -1, "Human should lose if they fold")

    @patch("builtins.input", side_effect=["invalid", "b"])  # Invalid input first
    def test_invalid_input_defaults_to_valid_choice(self, _mock_input: MagicMock) -> None:
        """Test that invalid inputs default to expected choices."""
        human_card, ai_card = 1, 0  # Q vs J
        result = self.game.playRound(go_first=True, human_card=human_card, ai_card=ai_card)
        self.assertIn(result, [-1, 1], "Invalid input should default correctly")

    @patch("builtins.input", side_effect=["p", "b"])  # Human checks, AI bets, human calls
    def test_play_round_human_checks_ai_bets_human_calls(self, _mock_input: MagicMock) -> None:
        """Test a round where human checks, AI bets, and human calls."""
        human_card, ai_card = 1, 2  # Q vs K
        result = self.game.playRound(go_first=True, human_card=human_card, ai_card=ai_card)
        self.assertIn(result, [-2, 2], "Outcome should be a check-bet-call showdown")

    def test_ai_plays_full_game(self) -> None:
        """Simulates AI playing until bankroll depletes."""
        with patch("builtins.input", side_effect=["p"] * 100):  # Simulate passive human play
            self.game.playAI(go_first=True, bankroll=3)  # Small bankroll to end quickly

    @patch("builtins.input", side_effect=["p", "p", "b", "p"])  # Different actions
    def test_game_flows_correctly(self, _mock_input: MagicMock) -> None:
        """Ensure multiple rounds process correctly with mixed actions."""
        human_card, ai_card = 2, 0  # K vs J
        result1 = self.game.playRound(go_first=True, human_card=human_card, ai_card=ai_card)
        result2 = self.game.playRound(go_first=False, human_card=human_card, ai_card=ai_card)
        self.assertIn(result1, [-1, 1, -2, 2], "Valid game result expected")
        self.assertIn(result2, [-1, 1, -2, 2], "Valid game result expected")

if __name__ == "__main__":
    unittest.main()

