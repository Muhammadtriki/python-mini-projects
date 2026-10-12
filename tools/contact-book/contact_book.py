"""Contact book: a command-line app that keeps contacts in a JSON file."""

import json
from pathlib import Path

CONTACTS_FILE = Path(__file__).with_name("contacts.json")

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


def load_contacts():
    """Read contacts from disk. A missing or damaged file gives an empty book."""
    try:
        with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
        raise ValueError("contacts file does not hold a dictionary")
    except FileNotFoundError:
        print(f"{YELLOW}No existing contacts found. Starting a new contact book.{RESET}")
    except ValueError:  # json.JSONDecodeError is a subclass of ValueError
        backup = CONTACTS_FILE.with_name(CONTACTS_FILE.name + ".bak")
        CONTACTS_FILE.replace(backup)
        print(
            f"{RED}The contacts file was damaged. It was kept as {backup.name} "
            f"and a new contact book was started.{RESET}"
        )
    return {}


def save_contacts(contacts):
    with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=4, ensure_ascii=False)


def add_contact(contacts):
    name = input("Enter contact name: ").strip().title()
    if not name:
        return f"{RED}Name cannot be empty.{RESET}"
    if name in contacts:
        return f"{RED}Contact already exists.{RESET}"

    phone = input("Enter contact phone number: ").strip()
    email = input("Enter contact email: ").strip()
    contacts[name] = {"phone": phone, "email": email}
    save_contacts(contacts)
    return f"\n{GREEN}Contact {name} added successfully.{RESET}"


def view_all_contacts(contacts):
    if not contacts:
        yield f"{RED}No contacts found.{RESET}"
    else:
        yield f"\n{YELLOW}These are the contacts in your contact book:{RESET}"
        for name, info in contacts.items():
            yield f"\n{GREEN}Name: {name} | Phone: {info['phone']} | Email: {info['email']}{RESET}"


def search_contact(contacts):
    name = input("Enter contact name to search: ").strip().title()
    if name in contacts:
        info = contacts[name]
        return f"\n{GREEN}Name: {name}, Phone: {info['phone']}, Email: {info['email']}{RESET}"
    return f"{RED}Contact not found.{RESET}"


def delete_contact(contacts):
    name = input("Enter contact name to delete: ").strip().title()
    if name in contacts:
        del contacts[name]
        save_contacts(contacts)
        return f"\n{GREEN}Contact {name} deleted successfully.{RESET}"
    return f"{RED}Contact not found.{RESET}"


def edit_contact(contacts):
    name = input("Enter contact name to edit: ").strip().title()

    if name not in contacts:
        return f"{RED}Contact not found.{RESET}"

    print("\n" + "=" * 50)
    print(f" EDITING: {name}")
    print(" Leave blank and press Enter to keep current info.")
    print("=" * 50)

    new_name = input(f"New name ({name}): ").strip().title()
    if new_name != "" and new_name != name:
        if new_name in contacts:
            confirm = input(
                f"{YELLOW}A contact named {new_name} already exists. Overwrite it? (y/n): {RESET}"
            ).strip().lower()
            if confirm != "y":
                print(f"{YELLOW}Rename cancelled, keeping other edits under the original name.{RESET}")
            else:
                contacts[new_name] = contacts.pop(name)
                name = new_name
        else:
            contacts[new_name] = contacts.pop(name)
            name = new_name

    new_phone = input(f"New phone ({contacts[name]['phone']}): ").strip()
    if new_phone != "":
        contacts[name]["phone"] = new_phone

    new_email = input(f"New email ({contacts[name]['email']}): ").strip()
    if new_email != "":
        contacts[name]["email"] = new_email

    save_contacts(contacts)
    return f"\n{GREEN}Success! Contact {name} updated.{RESET}"


def print_menu():
    print("\n" + "╔" + "═" * 47 + "╗")
    print("║               CONTACT BOOK MENU               ║")
    print("╠" + "═" * 47 + "╣")
    print("║  1. Add Contact                               ║")
    print("║  2. View All Contacts                         ║")
    print("║  3. Search Contact                            ║")
    print("║  4. Delete Contact                            ║")
    print("║  5. Edit Contact                              ║")
    print("║  6. Exit                                      ║")
    print("╚" + "═" * 47 + "╝")


def contact_book():
    contacts = load_contacts()

    while True:
        print_menu()
        choice = input("\nChoose an option (1-6): ").strip()

        if choice == "1":
            print(add_contact(contacts))
        elif choice == "2":
            for item in view_all_contacts(contacts):
                print(item)
        elif choice == "3":
            print(search_contact(contacts))
        elif choice == "4":
            print(delete_contact(contacts))
        elif choice == "5":
            print(edit_contact(contacts))
        elif choice == "6":
            save_contacts(contacts)
            print(f"\n{CYAN}Exiting Contact Book. Goodbye!{RESET}")
            break
        else:
            print(f"{RED}Invalid option. Please choose a number between 1 and 6.{RESET}")


if __name__ == "__main__":
    contact_book()
