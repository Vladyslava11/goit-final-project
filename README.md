# Personal Assistant

This project is a Personal Assistant - a system for storing and interacting with address book entries and notes.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd goit-final-project
```

2. No external dependencies required - uses only Python standard library.

3. Run the assistant:
```bash
python3 main.py
```

## Functionality

The assistant supports the following operations:

### Contact Management
- **Add contacts** - store contacts with names, phone numbers, emails, addresses, and birthdays
- **Search contacts** - find contacts by name
- **Edit contacts** - change phone, email, address, or birthday
- **Delete contacts** - remove contact records
- **Birthday reminders** - display list of contacts with birthdays within a specified number of days
- **Validation** - validate phone numbers and emails during contact creation/editing

### Notes Management
- **Add notes** - store text-based notes with titles
- **Search notes** - find notes by content
- **Edit notes** - modify note title and body
- **Delete notes** - remove notes
- **Tags** - add keywords/tags to describe note topics
- **Search by tags** - find notes by tag
- **Sort by tags** - sort notes by keywords (tags)

### Data Persistence
- All data (contacts, notes) is stored on the user's hard drive in `~/.personal_assistant/`
- Data persists between application restarts

### Intelligent Analysis
- The assistant can guess what command you mean based on your input
- Example: if you type "додати контакт" (add contact), it will suggest the `add` command

## Available Commands

### Contact Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add` | Add new contact (name, phone required; email, address, birthday optional) | `add John 0991234567` |
| `change` | Change contact field (phone, email, address, birthday) | `change John address Kyiv` |
| `phone` | Show phone numbers for contact | `phone John` |
| `all` | Show all contacts | `all` |
| `delete` | Delete contact | `delete John` |
| `add-birthday` | Add birthday to contact | `add-birthday John 15.05.1990` |
| `show-birthday` | Show birthday for contact | `show-birthday John` |
| `birthdays` | Show upcoming birthdays (default 7 days) | `birthdays 30` |

### Note Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add-note` | Add new note | `add-note Shopping Buy milk and bread` |
| `edit-note` | Edit note | `edit-note 1 Shopping Buy milk, bread and eggs` |
| `delete-note` | Delete note | `delete-note 1` |
| `find-note` | Search notes by content | `find-note Shopping` |
| `show-all-notes` | Show all notes | `show-all-notes` |

### Tag Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add-tag` | Add tag to note | `add-tag 1 Shopping` |
| `search-by-tag` | Search notes by tag | `search-by-tag Shopping` |
| `sort-notes-by-tag` | Sort notes by tags | `sort-notes-by-tag` |

### Other Commands

| Command | Description |
|---------|-------------|
| `hello` | Get greeting |
| `help` | Show all commands |
| `close` or `exit` | Exit and save data |

## Project Structure

```
goit-final-project/
├── main.py                     # Main entry point with command loop
├── commands_enum.py            # Command enumeration
├── address_book_module/        # Address book module
│   ├── __init__.py
│   ├── address_book.py        # AddressBook class
│   ├── fields.py              # Field classes (Name, Phone, Email, Address, Birthday)
│   └── record.py              # Record class
├── notebook_module/           # Notes module
│   ├── __init__.py
│   ├── notebook.py            # Notebook class
│   └── models.py             # Note and Tag classes
├── storage_module/            # Data persistence module
│   ├── __init__.py
│   └── storage.py            # save_data and load_data functions
└── README.md                  # This file
```

## Running the Project

To start the assistant, run:

```bash
python3 main.py
```

## Architecture

The project is built according to OOP principles:

- **Enum** for bot commands ([`commands_enum.py`](commands_enum.py))
- **Decorator** for error handling `input_error` ([`main.py`](main.py:10))
- **Parser** for parsing user input ([`main.py`](main.py:24))
- **`while True` loop** for continuous input waiting ([`main.py`](main.py:86))
- **Intelligent command suggestion** ([`main.py`](main.py:32))

## Requirements

The project implements all core requirements:
- ✅ Contact storage with names, phone numbers, emails, addresses, birthdays
- ✅ Contact search by name
- ✅ Contact editing and deletion
- ✅ Birthday reminders with configurable days
- ✅ Phone and email validation
- ✅ Notes with text information
- ✅ Note search, editing, and deletion
- ✅ Data persistence on disk
- ✅ Tags for notes (additional feature)
- ✅ Sort notes by tags (additional feature)
- ✅ Intelligent command suggestion (additional feature)

## Author

Project created as the final task of GoIT Python course.
