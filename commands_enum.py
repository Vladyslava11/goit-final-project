"""Перелік команд бота-асистента."""

from enum import Enum


class Command(Enum):
    """Перелік доступних команд бота."""
    HELLO = "hello"
    ADD = "add"
    CHANGE = "change"
    PHONE = "phone"
    ALL = "all"
    DELETE = "delete"
    ADD_BIRTHDAY = "add-birthday"
    SHOW_BIRTHDAY = "show-birthday"
    BIRTHDAYS = "birthdays"
    ADD_NOTE = "add-note"
    EDIT_NOTE = "edit-note"
    DELETE_NOTE = "delete-note"
    FIND_NOTE = "find-note"
    SHOW_ALL_NOTES = "show-all-notes"
    ADD_TAG = "add-tag"
    SEARCH_BY_TAG = "search-by-tag"
    SORT_NOTES_BY_TAG = "sort-notes-by-tag"
    CLOSE = "close"
    EXIT = "exit"
