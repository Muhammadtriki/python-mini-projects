# Contact Book

A command-line contact book. Contacts are saved in a `contacts.json` file next to the script, so they are still there the next time you run it.

```
python contact_book.py
```

## Features

- Add, view, search, edit and delete contacts
- Names are tidied automatically ("ali khan" becomes "Ali Khan") and cannot be empty
- Renaming a contact to an existing name asks before overwriting
- If `contacts.json` is damaged, it is kept as `contacts.json.bak` and a fresh book starts, so nothing is lost
- Works with names in any language, including Arabic and Urdu
- Colored output (best in Windows Terminal, VS Code or any modern terminal)

## Note

`contacts.json` holds real phone numbers once you use the program, so it is listed in `.gitignore` and never uploaded.
