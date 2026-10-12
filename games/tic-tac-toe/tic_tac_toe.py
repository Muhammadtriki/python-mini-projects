"""Two-player Tic-Tac-Toe for the command line."""

POSITION_NAMES = {
    1: "Top Left", 2: "Top Center", 3: "Top Right",
    4: "Middle Left", 5: "Middle Center", 6: "Middle Right",
    7: "Bottom Left", 8: "Bottom Center", 9: "Bottom Right",
}


def print_board(board):
    for index, row in enumerate(board):
        print(f"{row[0]} | {row[1]} | {row[2]}")
        if index < 2:
            print("---------")


def check_winner(board, symbol):
    # Check rows
    for row in board:
        if all(cell == symbol for cell in row):
            return True

    # Check columns
    for col in range(3):
        if all(board[row][col] == symbol for row in range(3)):
            return True

    # Check diagonals
    if all(board[i][i] == symbol for i in range(3)) or all(board[i][2 - i] == symbol for i in range(3)):
        return True

    return False


def display_available(available, position_name=POSITION_NAMES):
    for choice in available:
        print(f"{choice}: {position_name[choice]}")


def get_coords(choice):
    row = (choice - 1) // 3
    col = (choice - 1) % 3
    return row, col


def check_draw(available):
    return len(available) == 0


def choose_symbol():
    while True:
        symbol = input("Player 1, choose your symbol (X or O): ").strip().upper()
        if symbol in ("X", "O"):
            return symbol
        print("Invalid symbol. Please choose either 'X' or 'O'.")


def play_round():
    """Play one game. Returns the winning symbol, or None for a draw."""
    symbol = choose_symbol()

    board = [[" "] * 3 for _ in range(3)]
    available = list(POSITION_NAMES)
    current_symbol = symbol

    while True:
        print_board(board)
        display_available(available)
        try:
            choice = int(input(f"Player {current_symbol}, choose a position (1-9): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")
            continue

        if choice not in available:
            print("Invalid choice. Please select an available position.")
            continue

        row, col = get_coords(choice)
        board[row][col] = current_symbol
        available.remove(choice)

        if check_winner(board, current_symbol):
            print_board(board)
            print(f"Player {current_symbol} wins!")
            return current_symbol

        if check_draw(available):
            print_board(board)
            print("It's a draw!")
            return None

        current_symbol = "O" if current_symbol == "X" else "X"


def ask_play_again():
    """Keep asking until the answer is yes or no."""
    while True:
        again = input("Play again? (y/n): ").strip().lower()
        if again in ("y", "yes"):
            return True
        if again in ("n", "no"):
            return False
        print("Invalid input. Please enter 'y' or 'n'.")


def print_scoreboard(scores):
    print(f"\nScore  X: {scores['X']}  |  O: {scores['O']}  |  Draws: {scores['Draws']}")


def tic_tac_toe():
    print("Welcome to Tic-Tac-Toe!")
    scores = {"X": 0, "O": 0, "Draws": 0}

    while True:
        winner = play_round()
        scores[winner or "Draws"] += 1
        print_scoreboard(scores)

        if not ask_play_again():
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    tic_tac_toe()
