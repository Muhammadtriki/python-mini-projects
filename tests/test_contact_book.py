import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from loader import load_module

contact_book = load_module("tools/contact-book/contact_book.py")


class ContactBookTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        patcher = patch.object(contact_book, "CONTACTS_FILE", Path(self.tmp.name) / "contacts.json")
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_missing_file_gives_empty_book(self):
        self.assertEqual(contact_book.load_contacts(), {})

    def test_add_contact_saves_and_reloads(self):
        contacts = {}
        with patch("builtins.input", side_effect=["sara khan", "0300", "sara@example.com"]):
            message = contact_book.add_contact(contacts)
        self.assertIn("added successfully", message)
        self.assertEqual(contact_book.load_contacts()["Sara Khan"]["phone"], "0300")

    def test_empty_name_is_rejected(self):
        contacts = {}
        with patch("builtins.input", side_effect=["   "]):
            message = contact_book.add_contact(contacts)
        self.assertIn("cannot be empty", message)
        self.assertEqual(contacts, {})

    def test_duplicate_is_rejected_before_asking_for_details(self):
        contacts = {"Sara Khan": {"phone": "1", "email": "a"}}
        with patch("builtins.input", side_effect=["Sara Khan"]) as fake_input:
            message = contact_book.add_contact(contacts)
        self.assertIn("already exists", message)
        self.assertEqual(fake_input.call_count, 1)

    def test_damaged_file_is_kept_as_backup(self):
        contact_book.CONTACTS_FILE.write_text("{not valid json", encoding="utf-8")
        self.assertEqual(contact_book.load_contacts(), {})
        backup = contact_book.CONTACTS_FILE.with_name("contacts.json.bak")
        self.assertTrue(backup.exists())
        self.assertFalse(contact_book.CONTACTS_FILE.exists())

    def test_non_latin_names_are_stored_readably(self):
        contacts = {"محمد": {"phone": "1", "email": "a"}}
        contact_book.save_contacts(contacts)
        raw = contact_book.CONTACTS_FILE.read_text(encoding="utf-8")
        self.assertIn("محمد", raw)
        self.assertEqual(contact_book.load_contacts(), contacts)

    def test_edit_renames_contact(self):
        contacts = {"Sara Khan": {"phone": "1", "email": "a"}}
        with patch("builtins.input", side_effect=["Sara Khan", "Sara Ali", "", ""]):
            contact_book.edit_contact(contacts)
        self.assertIn("Sara Ali", contacts)
        self.assertNotIn("Sara Khan", contacts)

    def test_delete_contact(self):
        contacts = {"Sara Khan": {"phone": "1", "email": "a"}}
        with patch("builtins.input", side_effect=["sara khan"]):
            contact_book.delete_contact(contacts)
        self.assertEqual(contacts, {})


if __name__ == "__main__":
    unittest.main()
