"""Mad Libs: pick a story, fill in the blanks, read the result.

The stories live in stories.json. To add one, give it a title, a template with
{placeholders}, and a prompts dictionary with one question per placeholder.
"""

import json
import os
import string
import sys
import time
from pathlib import Path

STORIES_FILE = Path(__file__).with_name("stories.json")
TYPING_DELAY = 0.03  # seconds per character; set to 0 for instant output


def load_stories(path=STORIES_FILE):
    """Load the stories and check that every placeholder has a prompt."""
    with open(path, encoding="utf-8") as f:
        stories = json.load(f)

    for title, story in stories.items():
        fields = {name for _, name, _, _ in string.Formatter().parse(story["template"]) if name}
        if fields != set(story["prompts"]):
            raise ValueError(f"Story '{title}': template placeholders and prompts do not match")
    return stories


class MadLibs:
    def __init__(self, stories=None, typing_delay=TYPING_DELAY):
        self.stories = stories if stories is not None else load_stories()
        self.typing_delay = typing_delay

    def clear_screen(self):
        """Clear the console screen."""
        os.system("cls" if os.name == "nt" else "clear")

    def print_slowly(self, text, delay=None):
        """Print text character by character with a delay."""
        delay = self.typing_delay if delay is None else delay
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            if delay:
                time.sleep(delay)
        print()

    def get_story_choice(self):
        """Let the user choose a story."""
        self.clear_screen()
        print("\n=== CHOOSE A MADLIBS STORY ===\n")
        titles = list(self.stories)
        for i, title in enumerate(titles, 1):
            print(f"{i}. {title}")

        while True:
            try:
                choice = int(input("\nEnter the number of your choice: "))
                if 1 <= choice <= len(titles):
                    return titles[choice - 1]
                print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")

    def collect_answers(self, prompts):
        """Ask for one word per placeholder. Blank answers are not accepted."""
        self.clear_screen()
        print("\n=== ENTER YOUR WORDS ===\n")
        answers = {}

        for position, (key, prompt) in enumerate(prompts.items(), 1):
            print(f"\n{position}/{len(prompts)}: {prompt}")
            while True:
                word = input("> ").strip()
                if not word:
                    print("Please type something, a blank would leave a hole in the story.")
                elif key.startswith("number") and not word.isdigit():
                    print("Please enter a number using digits, for example 42.")
                else:
                    break
            answers[key] = word

        return answers

    def create_story(self, story_name, answers):
        """Fill the story template with the answers."""
        return self.stories[story_name]["template"].format(**answers)

    def play_again(self):
        """Ask if the user wants to play again."""
        return input("\nWould you like to play again? (yes/no): ").lower().startswith("y")

    def play(self):
        """Main game loop."""
        while True:
            self.clear_screen()
            self.print_slowly("Welcome to MADLIBS!", 0.05)
            self.print_slowly("Let's create a funny story together!", 0.05)

            story_name = self.get_story_choice()
            answers = self.collect_answers(self.stories[story_name]["prompts"])

            self.clear_screen()
            print("\n=== YOUR MADLIBS STORY ===\n")
            self.print_slowly(self.create_story(story_name, answers))

            if not self.play_again():
                self.clear_screen()
                self.print_slowly("Thanks for playing MADLIBS!", 0.05)
                break


if __name__ == "__main__":
    MadLibs().play()
