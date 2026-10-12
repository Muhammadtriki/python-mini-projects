import unittest
from unittest.mock import patch

from loader import load_module

xor = load_module("tools/xor-cipher/xor_cipher.py")


class XorCipherTests(unittest.TestCase):
    def test_known_value_for_english_text(self):
        self.assertEqual(xor.xor_cipher_encrypt("hello", "key"), "030015070a")

    def test_round_trip_english(self):
        encrypted = xor.xor_cipher_encrypt("Attack at dawn", "secret")
        self.assertEqual(xor.xor_cipher_decrypt(encrypted, "secret"), "Attack at dawn")

    def test_round_trip_arabic_and_urdu(self):
        for text in ["مرحبا بالعالم", "آپ کیسے ہیں"]:
            encrypted = xor.xor_cipher_encrypt(text, "key")
            self.assertEqual(xor.xor_cipher_decrypt(encrypted, "key"), text)

    def test_key_can_be_non_english_too(self):
        encrypted = xor.xor_cipher_encrypt("hello", "مفتاح")
        self.assertEqual(xor.xor_cipher_decrypt(encrypted, "مفتاح"), "hello")

    def test_empty_key_is_rejected(self):
        with self.assertRaises(ValueError):
            xor.xor_cipher_encrypt("hello", "")
        with self.assertRaises(ValueError):
            xor.xor_cipher_decrypt("00", "")

    def test_invalid_hex_is_a_value_error(self):
        with self.assertRaises(ValueError):
            xor.xor_cipher_decrypt("zz", "key")

    def test_wrong_key_that_breaks_utf8_is_a_decode_error(self):
        # 0xff XOR 0x61 ("a") is 0x9e, a lone continuation byte: never valid UTF-8
        with self.assertRaises(UnicodeDecodeError):
            xor.xor_cipher_decrypt("ff", "a")

    def test_menu_rows_line_up_with_the_border(self):
        with patch("builtins.print") as fake_print:
            xor.print_menu()
        lines = [call.args[0].strip("\n") for call in fake_print.call_args_list]
        self.assertEqual({len(line) for line in lines}, {xor.MENU_WIDTH + 2})


if __name__ == "__main__":
    unittest.main()
