"""XOR cipher tool: an educational demo of repeating-key XOR.

This is NOT secure encryption. Repeating-key XOR falls to known-plaintext
attacks and key reuse, so never use it to protect real data.
"""

from itertools import cycle

MENU_WIDTH = 47


def _xor_bytes(data, key_bytes):
    """XOR data with key_bytes, repeating the key as many times as needed."""
    return bytes(byte ^ key_byte for byte, key_byte in zip(data, cycle(key_bytes)))


def xor_cipher_encrypt(text, key):
    """Return the hex of text XOR key. Works with any language, via UTF-8 bytes."""
    if not key:
        raise ValueError("Key cannot be empty.")
    return _xor_bytes(text.encode("utf-8"), key.encode("utf-8")).hex()


def xor_cipher_decrypt(encrypted_hex, key):
    """Reverse xor_cipher_encrypt.

    Raises ValueError for an empty key or invalid hex, and UnicodeDecodeError
    (also a ValueError) when the result is not valid text, which usually means
    the key was wrong.
    """
    if not key:
        raise ValueError("Key cannot be empty.")
    data = bytes.fromhex(encrypted_hex)
    return _xor_bytes(data, key.encode("utf-8")).decode("utf-8")


def print_menu():
    print("\n╔" + "═" * MENU_WIDTH + "╗")
    print("║" + "XOR CIPHER TOOL".center(MENU_WIDTH) + "║")
    print("╠" + "═" * MENU_WIDTH + "╣")
    for line in ("1. Encrypt Text", "2. Decrypt Text", "3. Exit"):
        print("║  " + line.ljust(MENU_WIDTH - 2) + "║")
    print("╚" + "═" * MENU_WIDTH + "╝")


def xor_cipher_tool():
    while True:
        print_menu()
        choice = input("\nChoose an option (1-3): ").strip()

        if choice == "1":
            text = input("Enter text to encrypt: ")
            key = input("Enter encryption key: ")

            if not key:
                print("\033[91mError: Key cannot be empty.\033[0m")
                continue

            encrypted_hex = xor_cipher_encrypt(text, key)
            print(f"\n\033[92mEncrypted Text (hex): {encrypted_hex}\033[0m")

        elif choice == "2":
            encrypted_hex = input("Enter hex to decrypt: ").strip()
            key = input("Enter decryption key: ")

            if not key or not encrypted_hex:
                print("\033[91mError: Text and key cannot be empty.\033[0m")
                continue

            try:
                decrypted_text = xor_cipher_decrypt(encrypted_hex, key)
            except UnicodeDecodeError:
                print("\033[91mError: Could not turn the result into text. The key is probably wrong.\033[0m")
                continue
            except ValueError:
                print("\033[91mError: That's not valid hex, check what you pasted.\033[0m")
                continue

            print(f"\n\033[92mDecrypted Text: {decrypted_text}\033[0m")

        elif choice == "3":
            print("\n\033[96mExiting XOR Cipher Tool. Goodbye!\033[0m")
            break
        else:
            print("\033[91mInvalid choice. Please select a valid option (1-3).\033[0m")


if __name__ == "__main__":
    xor_cipher_tool()
