import unittest
from unittest.mock import patch

from loader import load_module

game = load_module("games/tic-tac-toe/tic_tac_toe.py")


def board_from(rows):
    return [list(row) for row in rows]


class WinnerTests(unittest.TestCase):
    def test_row_column_and_diagonals(self):
        self.assertTrue(game.check_winner(board_from(["XXX", "   ", "   "]), "X"))
        self.assertTrue(game.check_winner(board_from(["O  ", "O  ", "O  "]), "O"))
        self.assertTrue(game.check_winner(board_from(["X  ", " X ", "  X"]), "X"))
        self.assertTrue(game.check_winner(board_from(["  O", " O ", "O  "]), "O"))

    def test_no_winner(self):
        self.assertFalse(game.check_winner(board_from(["XO ", "   ", "   "]), "X"))

    def test_coordinates(self):
        self.assertEqual(game.get_coords(1), (0, 0))
        self.assertEqual(game.get_coords(5), (1, 1))
        self.assertEqual(game.get_coords(9), (2, 2))


class RoundTests(unittest.TestCase):
    def play(self, inputs):
        with patch("builtins.input", side_effect=inputs), patch("builtins.print"):
            return game.play_round()

    def test_x_wins_top_row(self):
        self.assertEqual(self.play(["x", "1", "4", "2", "5", "3"]), "X")

    def test_draw(self):
        moves = ["1", "2", "3", "5", "4", "6", "8", "7", "9"]
        self.assertIsNone(self.play(["X"] + moves))

    def test_bad_symbol_and_bad_moves_are_asked_again(self):
        inputs = ["Z", "O", "abc", "0", "1", "1", "4", "2", "5", "3", "6", "7", "8", "9"]
        result = self.play(inputs)
        self.assertIn(result, ("O", "X", None))


class PlayAgainTests(unittest.TestCase):
    def test_invalid_answer_asks_again_instead_of_starting_a_game(self):
        with patch("builtins.input", side_effect=["maybe", "", "y"]) as fake_input, patch("builtins.print"):
            self.assertTrue(game.ask_play_again())
        self.assertEqual(fake_input.call_count, 3)

    def test_no_ends_the_game(self):
        with patch("builtins.input", return_value="no"):
            self.assertFalse(game.ask_play_again())

    def test_full_session_with_score(self):
        inputs = ["X", "1", "4", "2", "5", "3", "n"]
        with patch("builtins.input", side_effect=inputs), patch("builtins.print") as fake_print:
            game.tic_tac_toe()
        printed = [str(call.args[0]) for call in fake_print.call_args_list if call.args]
        self.assertTrue(any("X: 1" in line and "Draws: 0" in line for line in printed))


if __name__ == "__main__":
    unittest.main()
