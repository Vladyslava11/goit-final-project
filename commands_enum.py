"""Перелік команд бота-асистента."""

from enum import Enum


class Command(Enum):
    """Перелік доступних команд бота."""
    HELLO = "hello"
    ADD = "add"
    CHANGE = "change"
    PHONE = "phone"
    ALL = "all"
    ADD_BIRTHDAY = "add-birthday"
    SHOW_BIRTHDAY = "show-birthday"
    BIRTHDAYS = "birthdays"
    CLOSE = "close"
    EXIT = "exit"
