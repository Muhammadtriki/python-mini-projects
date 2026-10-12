# Folder Organizer

Sorts the files in a folder into subfolders by type: PDFs, Images, Documents, Spreadsheets, Presentations, Archives, Audio, Video, Code, and Other.

```
python folder_organizer.py
```

Enter the path of the folder when asked.

## How it keeps your files safe

- It shows a preview of every move and waits for you to confirm before touching anything
- It never overwrites: if `photo.jpg` already exists in the destination, the moved file becomes `photo (1).jpg`
- It skips folders, hidden files and the script itself
- Running it twice in a row does nothing the second time

## Tip

Try it on a copy of a folder first, or on a folder like Downloads, until you are comfortable with how it sorts.
