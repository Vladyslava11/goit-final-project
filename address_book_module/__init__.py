"""Модуль адресної книги."""

from .address_book import AddressBook
from .record import Record
from .fields import Field, Name, Phone, Email, Address, Birthday

__all__ = [
    "AddressBook",
    "Record",
    "Field",
    "Name",
    "Phone",
    "Email",
    "Address",
    "Birthday",
]
