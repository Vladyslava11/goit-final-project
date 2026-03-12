"""
Тести для address_book.py

Покривають:
    1. Валідацію Phone (укр формат, 10 цифр, починається з 0)
    2. Валідацію Birthday (DD.MM.YYYY)
    3. Record.edit_field() — зміна name / phone / birthday
    4. AddressBook.search() — пошук за іменем та телефоном
    5. AddressBook.get_birthdays_in_range() — ДН у проміжку
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import date, timedelta
import pytest

from address_book import Phone, Birthday, Name, Record, AddressBook


# ============================================
# Phone validation
# ============================================

class TestPhone:
    def test_valid_phone(self):
        p = Phone("0671234567")
        assert p.value == "0671234567"

    def test_valid_phone_with_spaces(self):
        p = Phone("067 123 4567")
        assert p.value == "0671234567"

    def test_invalid_starts_with_non_zero(self):
        with pytest.raises(ValueError, match="invalid"):
            Phone("1671234567")

    def test_invalid_too_short(self):
        with pytest.raises(ValueError):
            Phone("067123456")   # 9 цифр

    def test_invalid_too_long(self):
        with pytest.raises(ValueError):
            Phone("06712345678")  # 11 цифр

    def test_invalid_letters(self):
        with pytest.raises(ValueError):
            Phone("067abc4567")


# ============================================
# Birthday validation
# ============================================

class TestBirthday:
    def test_valid_birthday(self):
        b = Birthday("25.08.1995")
        assert b.date == date(1995, 8, 25)

    def test_invalid_format(self):
        with pytest.raises(ValueError, match="invalid"):
            Birthday("1995-08-25")

    def test_invalid_date(self):
        with pytest.raises(ValueError):
            Birthday("32.01.2000")


# ============================================
# Record.edit_field()
# ============================================

class TestEditField:
    def setup_method(self):
        self.record = Record("Anna")
        self.record.add_phone("0671234567")
        self.record.add_birthday("01.01.1990")

    def test_edit_name(self):
        result = self.record.edit_field("name", "Maria")
        assert self.record.name.value == "Maria"
        assert "Maria" in result

    def test_edit_phone(self):
        result = self.record.edit_field("phone", "0671234567", "0991112233")
        assert self.record.phones[0].value == "0991112233"
        assert "0991112233" in result

    def test_edit_phone_not_found(self):
        with pytest.raises(ValueError, match="not found"):
            self.record.edit_field("phone", "0000000000", "0991112233")

    def test_edit_birthday(self):
        result = self.record.edit_field("birthday", "15.06.1985")
        assert self.record.birthday.value == "15.06.1985"
        assert "15.06.1985" in result

    def test_edit_invalid_field(self):
        with pytest.raises(ValueError, match="Unknown field"):
            self.record.edit_field("email", "test@test.com")

    def test_edit_phone_invalid_format(self):
        with pytest.raises(ValueError, match="invalid"):
            self.record.edit_field("phone", "0671234567", "1234567890")

    def test_edit_name_missing_arg(self):
        with pytest.raises(ValueError, match="new name"):
            self.record.edit_field("name")


# ============================================
# AddressBook.search()
# ============================================

class TestSearch:
    def setup_method(self):
        self.book = AddressBook()

        anna = Record("Anna")
        anna.add_phone("0671234567")
        self.book.add_record(anna)

        johanna = Record("Johanna")
        johanna.add_phone("0991112233")
        self.book.add_record(johanna)

        boris = Record("Boris")
        boris.add_phone("0503330067")
        self.book.add_record(boris)

    def test_search_by_name_partial(self):
        results = self.book.search("ann")
        names = [r.name.value for r in results]
        assert "Anna" in names
        assert "Johanna" in names

    def test_search_by_name_case_insensitive(self):
        results = self.book.search("ANNA")
        assert any(r.name.value == "Anna" for r in results)

    def test_search_by_phone_partial(self):
        results = self.book.search("067")
        names = [r.name.value for r in results]
        # Anna (0671234567) та Boris (0503330067) обидва містять "067"
        assert "Anna" in names
        assert "Boris" in names

    def test_search_by_full_phone(self):
        results = self.book.search("0991112233")
        assert len(results) == 1
        assert results[0].name.value == "Johanna"

    def test_search_no_results(self):
        assert self.book.search("xyz") == []

    def test_search_empty_query(self):
        assert self.book.search("") == []


# ============================================
# AddressBook.get_birthdays_in_range()
# ============================================

class TestGetBirthdaysInRange:
    def _make_book_with_bday(self, name: str, delta_days: int) -> AddressBook:
        """Помічник: створює книгу з контактом, у якого ДН через delta_days."""
        book = AddressBook()
        record = Record(name)
        bday = date.today() + timedelta(days=delta_days)
        record.add_birthday(bday.strftime("%d.%m.%Y"))
        book.add_record(record)
        return book

    def test_birthday_within_range(self):
        book = self._make_book_with_bday("Alice", 3)
        result = book.get_birthdays_in_range(7)
        assert any(r["name"] == "Alice" for r in result)

    def test_birthday_today_included(self):
        book = self._make_book_with_bday("Bob", 0)
        result = book.get_birthdays_in_range(7)
        assert any(r["name"] == "Bob" for r in result)

    def test_birthday_outside_range(self):
        book = self._make_book_with_bday("Charlie", 10)
        result = book.get_birthdays_in_range(7)
        assert not any(r["name"] == "Charlie" for r in result)

    def test_no_birthday_set(self):
        book = AddressBook()
        record = Record("Dave")  # без ДН
        book.add_record(record)
        assert book.get_birthdays_in_range(7) == []

    def test_sorted_by_date(self):
        book = AddressBook()
        for name, delta in [("Third", 5), ("First", 1), ("Second", 3)]:
            r = Record(name)
            bday = date.today() + timedelta(days=delta)
            r.add_birthday(bday.strftime("%d.%m.%Y"))
            book.add_record(r)
        result = book.get_birthdays_in_range(7)
        names = [r["name"] for r in result]
        assert names == ["First", "Second", "Third"]

    def test_custom_range(self):
        book = self._make_book_with_bday("Eve", 20)
        assert book.get_birthdays_in_range(7) == []
        result = book.get_birthdays_in_range(30)
        assert any(r["name"] == "Eve" for r in result)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])