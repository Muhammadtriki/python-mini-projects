import unittest
from unittest.mock import patch

from loader import load_module

hub = load_module("tools/multi-tool-hub/multi_tool_hub.py")


class CalculatorTests(unittest.TestCase):
    def test_basic_operations(self):
        self.assertEqual(hub.calculate(6, 3, "+"), 9)
        self.assertEqual(hub.calculate(6, 3, "-"), 3)
        self.assertEqual(hub.calculate(6, 3, "*"), 18)
        self.assertEqual(hub.calculate(6, 3, "x"), 18)
        self.assertEqual(hub.calculate(6, 3, "/"), 2)

    def test_errors(self):
        with self.assertRaises(ZeroDivisionError):
            hub.calculate(1, 0, "/")
        with self.assertRaises(ValueError):
            hub.calculate(1, 1, "%")

    def test_interactive_result_drops_trailing_zero(self):
        with patch("builtins.input", side_effect=["6", "3", "/"]):
            self.assertEqual(hub.calculator(), "The result for the calculation is 2")

    def test_interactive_bad_number(self):
        with patch("builtins.input", side_effect=["abc"]):
            self.assertIn("must be numbers", hub.calculator())


class CaesarTests(unittest.TestCase):
    def test_round_trip(self):
        original = "Hello, World! 123"
        encrypted = hub.caesar_shift(original, 3)
        self.assertEqual(encrypted, "Khoor, Zruog! 123")
        self.assertEqual(hub.caesar_shift(encrypted, -3), original)

    def test_non_english_letters_are_left_alone(self):
        text = "مرحبا café"
        shifted = hub.caesar_shift(text, 5)
        self.assertTrue(shifted.startswith("مرحبا "))
        self.assertIn("é", shifted)
        self.assertEqual(hub.caesar_shift(shifted, -5), text)

    def test_interactive_decrypt(self):
        with patch("builtins.input", side_effect=["Khoor", "2", "3"]):
            self.assertIn("'Hello'", hub.caesar_cipher())


class TextCheckerTests(unittest.TestCase):
    def test_palindrome_ignores_punctuation_and_case(self):
        self.assertTrue(hub.is_palindrome("A man, a plan, a canal: Panama"))
        self.assertFalse(hub.is_palindrome("Hello"))
        self.assertTrue(hub.is_palindrome("ابا"))

    def test_empty_text_is_not_a_palindrome(self):
        self.assertFalse(hub.is_palindrome("  !! "))

    def test_anagram(self):
        self.assertTrue(hub.is_anagram("Dormitory", "Dirty room!"))
        self.assertFalse(hub.is_anagram("abc", "abd"))
        self.assertFalse(hub.is_anagram("", ""))


class ToDoTests(unittest.TestCase):
    def test_add_show_delete_and_quit(self):
        inputs = ["1", "Buy milk", "3", "2", "1", "3", "4"]
        with patch("builtins.input", side_effect=inputs), patch("builtins.print") as fake_print:
            result = hub.to_do_list()
        self.assertEqual(result, "Exiting To-Do List.")
        printed = [call.args[0] for call in fake_print.call_args_list]
        self.assertIn("1. Buy milk", printed)
        self.assertIn("Removed: 'Buy milk'", printed)
        self.assertIn("Your list is empty!", printed)


class MainMenuTests(unittest.TestCase):
    def test_menu_loops_until_quit(self):
        with patch("builtins.input", side_effect=["9", "5"]), patch("builtins.print") as fake_print:
            hub.main()
        printed = [call.args[0] for call in fake_print.call_args_list]
        self.assertIn("Enter a valid choice (1-5).", printed)
        self.assertIn("Goodbye.", printed)


if __name__ == "__main__":
    unittest.main()
