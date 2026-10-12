# XOR Cipher

An educational demo of repeating-key XOR. You type a message and a key, and it gives you the encrypted result as hex. Enter the hex and the same key to get the message back.

```
python xor_cipher.py
```

Example: the text `hello` with the key `key` gives `030015070a`.

## This is not secure encryption

Repeating-key XOR is a classic teaching cipher, not a way to protect real data. It falls to known-plaintext attacks (if someone knows part of the message, they can recover the key) and it is broken completely if a key is reused. For real work, use a tested library and a modern cipher such as AES.

## Details

- The message and the key are turned into UTF-8 bytes first, so it works with English, Arabic, Urdu or any other language
- An empty key is rejected
- A wrong key usually produces bytes that are not valid text, and the program says so instead of crashing
