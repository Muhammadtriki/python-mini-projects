import unittest
from unittest.mock import patch

from loader import load_module

mad_libs = load_module("games/mad-libs/mad_libs.py")


class StoryFileTests(unittest.TestCase):
    def test_every_story_loads_and_matches_its_prompts(self):
        stories = mad_libs.load_stories()
        self.assertEqual(len(stories), 3)
        for story in stories.values():
            self.assertTrue(story["prompts"])

    def test_mismatched_story_is_rejected(self):
        import json
        import tempfile
        from pathlib import Path

        bad = {"Bad": {"template": "Hi {name} and {pet}", "prompts": {"name": "Enter a name"}}}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "stories.json"
            path.write_text(json.dumps(bad))
            with self.assertRaises(ValueError):
                mad_libs.load_stories(path)


class GameTests(unittest.TestCase):
    def setUp(self):
        self.game = mad_libs.MadLibs(typing_delay=0)
        patcher = patch.object(mad_libs.MadLibs, "clear_screen", lambda self: None)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_create_story_fills_every_placeholder(self):
        for name, story in self.game.stories.items():
            answers = {key: "word" for key in story["prompts"]}
            text = self.game.create_story(name, answers)
            self.assertNotIn("{", text)

    def test_blank_and_non_digit_answers_are_asked_again(self):
        prompts = {"name": "Enter a name", "number": "Enter a number"}
        inputs = ["", "   ", "Sara", "many", "7"]
        with patch("builtins.input", side_effect=inputs), patch("builtins.print"):
            answers = self.game.collect_answers(prompts)
        self.assertEqual(answers, {"name": "Sara", "number": "7"})

    def test_story_choice_rejects_bad_input(self):
        with patch("builtins.input", side_effect=["x", "9", "2"]), patch("builtins.print"):
            self.assertEqual(self.game.get_story_choice(), "Fairy Tale")

    def test_full_game_runs_once(self):
        prompts = self.game.stories["Space Adventure"]["prompts"]
        answers = ["2150" if key.startswith("number") else "word" for key in prompts]
        inputs = ["1"] + answers + ["no"]
        with patch("builtins.input", side_effect=inputs), patch("builtins.print"):
            self.game.play()


if __name__ == "__main__":
    unittest.main()
