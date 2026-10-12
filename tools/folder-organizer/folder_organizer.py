"""Folder organizer: sorts the files in a folder into subfolders by file type.

It shows a preview first and only moves files after you confirm. Files are
never overwritten: if a name is already taken, the moved file gets a number,
like photo (1).jpg.
"""

import shutil
from pathlib import Path

CATEGORIES = {
    "PDFs": {".pdf"},
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"},
    "Documents": {".doc", ".docx", ".txt", ".rtf", ".odt"},
    "Spreadsheets": {".xls", ".xlsx", ".csv"},
    "Presentations": {".ppt", ".pptx"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Audio": {".mp3", ".wav", ".m4a"},
    "Video": {".mp4", ".mkv", ".avi", ".mov"},
    "Code": {".py", ".js", ".html", ".css", ".cpp", ".java"},
}
OTHER_FOLDER = "Other"

EXTENSION_TO_FOLDER = {
    extension: folder for folder, extensions in CATEGORIES.items() for extension in extensions
}


def folder_for(file_path):
    """Return the name of the subfolder a file belongs in."""
    return EXTENSION_TO_FOLDER.get(Path(file_path).suffix.lower(), OTHER_FOLDER)


def plan_moves(target_dir):
    """List (source, destination) pairs for the files directly inside target_dir.

    Folders, hidden files and this script itself are skipped, so running the
    organizer twice in a row never tries to sort its own output.
    """
    this_script = Path(__file__).resolve()
    plan = []
    for item in sorted(target_dir.iterdir()):
        if not item.is_file() or item.name.startswith(".") or item.resolve() == this_script:
            continue
        plan.append((item, target_dir / folder_for(item) / item.name))
    return plan


def unique_destination(path):
    """Return path, or path with ' (1)', ' (2)'... added if the name is taken."""
    if not path.exists():
        return path
    number = 1
    while True:
        candidate = path.with_name(f"{path.stem} ({number}){path.suffix}")
        if not candidate.exists():
            return candidate
        number += 1


def organize_files_by_extension(folder_path, ask_confirmation=True):
    """Sort a folder's files into subfolders. Returns how many files were moved."""
    target_dir = Path(folder_path).expanduser()

    if not target_dir.is_dir():
        print("That path doesn't exist or isn't a folder.")
        return 0

    plan = plan_moves(target_dir)
    if not plan:
        print("Nothing to organize.")
        return 0

    print(f"\nThese {len(plan)} files will be moved:")
    for source, destination in plan:
        print(f"  {source.name}  ->  {destination.parent.name}/")

    if ask_confirmation:
        answer = input("\nMove them now? (y/n): ").strip().lower()
        if answer not in ("y", "yes"):
            print("Cancelled, nothing was moved.")
            return 0

    moved = 0
    for source, destination in plan:
        try:
            destination.parent.mkdir(exist_ok=True)
            shutil.move(str(source), str(unique_destination(destination)))
            moved += 1
        except OSError as error:
            print(f"Could not move {source.name}: {error}")

    print(f"Done. Moved {moved} of {len(plan)} files.")
    return moved


if __name__ == "__main__":
    path_input = input("Enter the path of the folder you want to organize: ").strip()
    organize_files_by_extension(path_input)
