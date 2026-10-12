# Python Mini Projects

Small command-line programs I built while learning Python. Each project has its own folder and README, uses only the standard library, and is covered by automated tests.

| Project | What it does |
| --- | --- |
| [Contact Book](tools/contact-book) | Add, search, edit and delete contacts, saved to a JSON file |
| [Folder Organizer](tools/folder-organizer) | Sorts the files in a folder into subfolders by type, with a preview first |
| [Multi-Tool Hub](tools/multi-tool-hub) | Calculator, Caesar cipher, palindrome and anagram checker, and a to-do list |
| [XOR Cipher](tools/xor-cipher) | Educational repeating-key XOR encryption that works with any language |
| [Tic-Tac-Toe](games/tic-tac-toe) | Two-player game with a running scoreboard |
| [Mad Libs](games/mad-libs) | Pick a story, fill in the blanks, read the result. Stories live in a JSON file |

## Run a project

Python 3 is all you need. From the repo folder:

```
python tools/contact-book/contact_book.py
python games/tic-tac-toe/tic_tac_toe.py
```

Every project follows the same pattern: `python <folder>/<file>.py`.

## Run the tests

```
python -m unittest discover -s tests
```

## What these projects practice

- Splitting a program into small functions that each do one job
- Validating user input and handling errors without crashing
- Reading and writing files (JSON) and handling a missing or damaged file
- Writing tests for command-line programs
- Working with text in any language through UTF-8
