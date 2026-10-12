"""Multi-tool hub: a calculator, a Caesar cipher, a palindrome and anagram
checker, and a to-do list in one command-line program."""

MENU = """
Choose:
        1. Calculator
        2. Caesar Cipher
        3. Palindrome and Anagram Checker
        4. To-Do List
        5. Quit
        > """


# ----------------------------------------------------------------------------
# Calculator
# ----------------------------------------------------------------------------
def calculate(number_1, number_2, operator):
    """Return number_1 <operator> number_2.

    Raises ValueError for an unknown operator and ZeroDivisionError for x / 0.
    """
    if operator == "+":
        return number_1 + number_2
    if operator == "-":
        return number_1 - number_2
    if operator in ("*", "x", "X"):
        return number_1 * number_2
    if operator == "/":
        return number_1 / number_2
    raise ValueError("Incorrect operator")


def calculator():
    try:
        number_1 = float(input("Input your first number: "))
        number_2 = float(input("Input your second number: "))
    except ValueError:
        return "Error: Inputs must be numbers"

    operator = input("Input the operator (e.g +, -, *, /): ").strip()
    try:
        result = calculate(number_1, number_2, operator)
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed"
    except ValueError:
        return "Error: Incorrect operator"

    if result.is_integer():
        result = int(result)
    return f"The result for the calculation is {result}"


# ----------------------------------------------------------------------------
# Caesar cipher
# ----------------------------------------------------------------------------
def caesar_shift(text, shift):
    """Shift the English letters in text by shift places.

    Only a-z and A-Z are shifted. Every other character (digits, punctuation,
    Arabic, Urdu or accented letters) is passed through unchanged.
    """
    result = []
    for char in text:
        if "a" <= char <= "z":
            base = ord("a")
        elif "A" <= char <= "Z":
            base = ord("A")
        else:
            result.append(char)
            continue
        result.append(chr((ord(char) - base + shift) % 26 + base))
    return "".join(result)


def caesar_cipher():
    sentence = input("Enter your sentence: ")

    try:
        mode = int(input("""
        1. Encrypt
        2. Decrypt
        > """))
        shift = int(input("By how many numbers do you wanna shift: "))
    except ValueError:
        return "Error: Mode and shift must be valid integers!"

    if mode not in (1, 2):
        return "Error: Invalid mode selected (choose 1 or 2)."

    if mode == 2:
        shift = -shift

    if shift % 26 == 0:
        return "Error: A shift of 26 (or multiples of 26) leaves the text unchanged!"

    new_sentence = caesar_shift(sentence, shift)

    if shift < 0:
        return f"Your decrypted sentence is '{new_sentence}' (shifted back by {abs(shift)})"
    return f"Your encrypted sentence is '{new_sentence}' (shifted forward by {shift})"


# ----------------------------------------------------------------------------
# Palindrome and anagram checker
# ----------------------------------------------------------------------------
def normalize(text):
    """Keep only letters and digits, lowercased, so spaces and punctuation are ignored."""
    return "".join(char.lower() for char in text if char.isalnum())


def is_palindrome(text):
    cleaned = normalize(text)
    return bool(cleaned) and cleaned == cleaned[::-1]


def is_anagram(first_text, second_text):
    first, second = normalize(first_text), normalize(second_text)
    return bool(first) and sorted(first) == sorted(second)


def palindrome_and_anagram_checker():
    try:
        choice = int(input("""
        1. Palindrome
        2. Anagram
        > """))
    except ValueError:
        return "Error: You must type a number (1 or 2)."

    if choice == 1:
        text = input("What do you wanna check?\n> ")
        if not normalize(text):
            return "Error: Type at least one letter or digit."
        if is_palindrome(text):
            return f"'{text}' is a palindrome!"
        return f"'{text}' is not a palindrome."

    if choice == 2:
        first_text = input("Input your first word/sentence: ")
        second_text = input("Input your second word/sentence: ")
        if not normalize(first_text) or not normalize(second_text):
            return "Error: Type at least one letter or digit in both."
        if is_anagram(first_text, second_text):
            return f"'{first_text}' and '{second_text}' are anagrams!"
        return f"'{first_text}' and '{second_text}' are not anagrams."

    return "Error: Invalid choice (must be 1 or 2)."


# ----------------------------------------------------------------------------
# To-do list
# ----------------------------------------------------------------------------
def to_do_list():
    tasks = []

    while True:
        choice = input("""
        1. Add task
        2. Delete a task
        3. Show tasks
        4. Quit
        > """)

        if choice == "1":
            add = input("What is the new task you want to add? ")
            tasks.append(add)
            print(f"Added: '{add}'")

        elif choice == "2":
            if not tasks:
                print("Your list is empty!")
                continue
            try:
                remove = int(input("Which task number do you wanna delete? "))
            except ValueError:
                print("Please enter a valid number.")
                continue

            if 1 <= remove <= len(tasks):
                removed_task = tasks.pop(remove - 1)
                print(f"Removed: '{removed_task}'")
            else:
                print("That task number does not exist.")

        elif choice == "3":
            if not tasks:
                print("Your list is empty!")
            else:
                for index, task in enumerate(tasks, start=1):
                    print(f"{index}. {task}")

        elif choice == "4":
            return "Exiting To-Do List."

        else:
            print("Invalid choice, please select 1-4.")


# ----------------------------------------------------------------------------
# Main menu
# ----------------------------------------------------------------------------
def main():
    print("=== Welcome to the Multi-Tool Hub ===")
    actions = {
        "1": calculator,
        "2": caesar_cipher,
        "3": palindrome_and_anagram_checker,
        "4": to_do_list,
    }

    while True:
        choice = input(MENU).strip()
        if choice == "5":
            print("Goodbye.")
            break
        action = actions.get(choice)
        if action is None:
            print("Enter a valid choice (1-5).")
            continue
        print(action())


if __name__ == "__main__":
    main()
