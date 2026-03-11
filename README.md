# Personal Assistant

This project is a Personal Assistant - a system for storing and interacting with address book entries and notes.

## Functionality

The assistant supports the following operations:

### Contact Management
- **Add contacts** - store contacts with names, addresses, phone numbers, emails, and birthdays
- **Search contacts** - find contacts by various criteria (e.g., by name)
- **Edit and delete contacts** - modify or remove contact records
- **Birthday reminders** - display list of contacts with birthdays within a specified number of days
- **Validation** - validate phone numbers and emails during contact creation/editing

### Notes Management
- **Add notes** - store text-based notes
- **Search notes** - find notes by content
- **Edit and delete notes** - modify or remove notes
- **Tags** - add keywords/tags describing the topic and subject of notes
- **Sort by tags** - search and sort notes by keywords (tags)

### Data Persistence
- All data (contacts, notes) is stored on the user's hard drive
- Data persists between application restarts

## Available Commands

| Command | Description |
|---------|-------------|
| `add [name] [phone]` | Add a new contact or phone to existing contact |
| `change [name] [new phone]` | Change phone number of existing contact |
| `phone [name]` | Show phone numbers for specified contact |
| `all` | Show all contacts |
| `add-birthday [name] [DD.MM.YYYY]` | Add birthday |
| `show-birthday [name]` | Show birthday for contact |
| `birthdays` | Show birthdays in the next week |
| `add-note [title]` | Add a new note |
| `show-notes` | Show all notes |
| `search-notes [query]` | Search notes by content |
| `hello` | Get greeting from bot |
| `close` or `exit` | Exit the program |

## Project Structure

```
goit-final-project/
├── main.py       # Main entry point with command loop
├── enums.py      # Command enumeration (Enum)
└── README.md     # This file
```

## Running the Project

To start the assistant, run:

```bash
python main.py
```

## Architecture

The project is built according to OOP principles:

- **Enum** for bot commands ([`enums.py`](enums.py))
- **Decorator** for error handling `input_error` ([`main.py`](main.py:42))
- **Parser** for parsing user input ([`main.py`](main.py:65))
- **`while True` loop** for continuous input waiting ([`main.py`](main.py:98))

## Requirements

The project implements all core requirements:
- ✅ Contact storage with names, addresses, phone numbers, emails, birthdays
- ✅ Contact search
- ✅ Contact editing and deletion
- ✅ Birthday reminders
- ✅ Phone and email validation
- ✅ Notes with text information
- ✅ Note search, editing, and deletion
- ✅ Data persistence on disk
- ✅ Tags for notes (additional feature)
- ✅ Sort notes by tags (additional feature)

## Author

Project created as the final task of GoIT Python course.
