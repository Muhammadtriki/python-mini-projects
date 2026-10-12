import tempfile
import unittest
from pathlib import Path

from loader import load_module

organizer = load_module("tools/folder-organizer/folder_organizer.py")


class FolderOrganizerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def make(self, name, text="x"):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def test_files_go_to_the_right_folders(self):
        for name in ["a.pdf", "b.JPG", "c.docx", "d.xyz", "e.csv", "f.jpeg"]:
            self.make(name)
        moved = organizer.organize_files_by_extension(self.root, ask_confirmation=False)
        self.assertEqual(moved, 6)
        self.assertTrue((self.root / "PDFs" / "a.pdf").exists())
        self.assertTrue((self.root / "Images" / "b.JPG").exists())
        self.assertTrue((self.root / "Images" / "f.jpeg").exists())
        self.assertTrue((self.root / "Documents" / "c.docx").exists())
        self.assertTrue((self.root / "Spreadsheets" / "e.csv").exists())
        self.assertTrue((self.root / "Other" / "d.xyz").exists())

    def test_existing_files_are_never_overwritten(self):
        self.make("Images/photo.jpg", "old")
        self.make("photo.jpg", "new")
        organizer.organize_files_by_extension(self.root, ask_confirmation=False)
        self.assertEqual((self.root / "Images" / "photo.jpg").read_text(), "old")
        self.assertEqual((self.root / "Images" / "photo (1).jpg").read_text(), "new")

    def test_hidden_files_are_skipped(self):
        self.make(".hidden.txt")
        self.make("note.txt")
        organizer.organize_files_by_extension(self.root, ask_confirmation=False)
        self.assertTrue((self.root / ".hidden.txt").exists())
        self.assertTrue((self.root / "Documents" / "note.txt").exists())

    def test_running_twice_does_not_touch_sorted_files(self):
        self.make("a.pdf")
        organizer.organize_files_by_extension(self.root, ask_confirmation=False)
        moved_again = organizer.organize_files_by_extension(self.root, ask_confirmation=False)
        self.assertEqual(moved_again, 0)
        self.assertTrue((self.root / "PDFs" / "a.pdf").exists())

    def test_bad_path_moves_nothing(self):
        self.assertEqual(organizer.organize_files_by_extension(self.root / "missing", ask_confirmation=False), 0)

    def test_declining_the_preview_moves_nothing(self):
        from unittest.mock import patch

        self.make("a.pdf")
        with patch("builtins.input", return_value="n"):
            moved = organizer.organize_files_by_extension(self.root)
        self.assertEqual(moved, 0)
        self.assertTrue((self.root / "a.pdf").exists())


if __name__ == "__main__":
    unittest.main()
