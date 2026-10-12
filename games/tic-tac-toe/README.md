# Tic-Tac-Toe

A two-player game for the command line. Player 1 picks X or O, then the players take turns choosing a numbered position (1 to 9). A scoreboard tracks wins and draws across rounds.

```
python tic_tac_toe.py
```

## Details

- Checks rows, columns and both diagonals after every move
- A winning last move counts as a win, not a draw
- Invalid input (letters, numbers out of range, taken squares) is rejected with a message instead of crashing
- "Play again?" keeps asking until you answer yes or no
