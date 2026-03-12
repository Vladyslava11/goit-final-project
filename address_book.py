"""
Бізнес-логіка адресної книги.

Модуль містить класи для зберігання та обробки контактів:
    - Phone     — поле телефону з валідацією (0XXXXXXXXX, 10 цифр, укр формат)
    - Birthday  — поле дня народження з валідацією (DD.MM.YYYY)
    - Record    — запис контакту (ім'я, список телефонів, день народження)
    - AddressBook — колекція контактів із методами пошуку та вибірки

Основний функціонал (завдання):
    - Record.edit_field()      — змінити конкретне поле існуючого контакту
    - AddressBook.search()     — гнучкий пошук за іменем або номером телефону
    - AddressBook.get_birthdays_in_range() — контакти з ДН у заданому проміжку
"""

import re
from datetime import date, datetime, timedelta
from collections import UserDict


# ============================================
# Поля (Fields)
# ============================================

class Field:
    """Базовий клас для полів запису."""

    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return self.value


class Name(Field):
    """Ім'я контакту. Обов'язкове поле."""

    def __init__(self, value: str):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty.")
        super().__init__(value.strip())


class Phone(Field):
    """
    Телефон контакту.

    Формат: починається з 0, рівно 10 цифр (український формат).
    Приклад: 0671234567
    """

    PHONE_PATTERN = re.compile(r"^0\d{9}$")

    def __init__(self, value: str):
        cleaned = re.sub(r"\s+", "", value)  # прибираємо пробіли, якщо є
        if not self.PHONE_PATTERN.match(cleaned):
            raise ValueError(
                f"Phone '{value}' is invalid. "
                "Must start with 0 and contain exactly 10 digits (e.g. 0671234567)."
            )
        super().__init__(cleaned)


class Birthday(Field):
    """
    День народження контакту.

    Формат: DD.MM.YYYY
    Приклад: 25.08.1995
    """

    DATE_FORMAT = "%d.%m.%Y"

    def __init__(self, value: str):
        try:
            self.date: date = datetime.strptime(value, self.DATE_FORMAT).date()
        except ValueError:
            raise ValueError(
                f"Birthday '{value}' is invalid. Use format DD.MM.YYYY (e.g. 25.08.1995)."
            )
        super().__init__(value)


# ============================================
# Запис контакту (Record)
# ============================================

class Record:
    """
    Запис контакту: ім'я, список телефонів, необов'язковий день народження.

    Attributes:
        name     (Name)           — ім'я контакту
        phones   (list[Phone])    — список телефонів
        birthday (Birthday|None)  — день народження
    """

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

    # ------ телефони ------

    def add_phone(self, phone: str) -> None:
        """Додати телефон до контакту."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """Видалити телефон із контакту."""
        target = self._find_phone_obj(phone)
        if target is None:
            raise ValueError(f"Phone '{phone}' not found in contact '{self.name}'.")
        self.phones.remove(target)

    def _find_phone_obj(self, phone: str) -> Phone | None:
        """Повернути об'єкт Phone або None."""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    # ------ день народження ------

    def add_birthday(self, birthday: str) -> None:
        """Встановити день народження контакту."""
        self.birthday = Birthday(birthday)

    # ------ ✅ ЗАВДАННЯ: змінити конкретне поле ------

    def edit_field(self, field: str, *values: str) -> str:
        """
        Змінити конкретне поле існуючого контакту.

        Args:
            field:  назва поля ('name', 'phone', 'birthday')
            values: аргументи залежно від поля:
                    - 'name'     → (new_name,)
                    - 'phone'    → (old_phone, new_phone)
                    - 'birthday' → (new_birthday,)

        Returns:
            Рядок із підтвердженням зміни.

        Raises:
            ValueError: якщо поле невідоме, аргументів недостатньо або дані невалідні.
        """
        field = field.lower().strip()

        if field == "name":
            if not values:
                raise ValueError("Provide a new name.")
            old_name = self.name.value
            self.name = Name(values[0])
            return f"Name changed: '{old_name}' → '{self.name}'."

        elif field == "phone":
            if len(values) < 2:
                raise ValueError("Provide old phone and new phone: edit-field phone <old> <new>.")
            old_phone, new_phone = values[0], values[1]
            target = self._find_phone_obj(old_phone)
            if target is None:
                raise ValueError(f"Phone '{old_phone}' not found in contact '{self.name}'.")
            idx = self.phones.index(target)
            self.phones[idx] = Phone(new_phone)
            return f"Phone changed: '{old_phone}' → '{new_phone}'."

        elif field == "birthday":
            if not values:
                raise ValueError("Provide a new birthday in format DD.MM.YYYY.")
            old = self.birthday.value if self.birthday else "—"
            self.birthday = Birthday(values[0])
            return f"Birthday changed: '{old}' → '{self.birthday}'."

        else:
            raise ValueError(
                f"Unknown field '{field}'. Available fields: name, phone, birthday."
            )

    # ------ представлення ------

    def __str__(self):
        phones_str = ", ".join(p.value for p in self.phones) if self.phones else "—"
        birthday_str = self.birthday.value if self.birthday else "—"
        return (
            f"Contact: {self.name} | "
            f"Phones: {phones_str} | "
            f"Birthday: {birthday_str}"
        )


# ============================================
# Адресна книга (AddressBook)
# ============================================

class AddressBook(UserDict):
    """
    Колекція контактів (dict: ім'я → Record).

    Додаткові методи:
        search()                 — пошук за іменем або телефоном
        get_birthdays_in_range() — контакти з ДН у заданому діапазоні дат
    """

    def add_record(self, record: Record) -> None:
        """Додати запис до книги."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        """
        Знайти контакт за точним іменем.

        Raises:
            KeyError: якщо контакт не знайдено.
        """
        if name not in self.data:
            raise KeyError(name)
        return self.data[name]

    def delete(self, name: str) -> None:
        """Видалити контакт за іменем."""
        if name not in self.data:
            raise KeyError(name)
        del self.data[name]

    # ------ ✅ ЗАВДАННЯ: гнучкий пошук ------

    def search(self, query: str) -> list[Record]:
        """
        Гнучкий пошук контактів за іменем АБО номером телефону.

        Пошук регістронезалежний та підтримує часткові збіги.
        Наприклад, запит "067" знайде всі номери, що містять "067";
        запит "ann" знайде імена Anna, Johanna тощо.

        Args:
            query: рядок пошуку (частина імені або частина номера)

        Returns:
            Список Record, що відповідають запиту (може бути порожнім).
        """
        query = query.strip().lower()
        if not query:
            return []

        results = []
        for record in self.data.values():
            name_match = query in record.name.value.lower()
            phone_match = any(query in p.value for p in record.phones)
            if name_match or phone_match:
                results.append(record)

        return results

    # ------ ✅ ЗАВДАННЯ: дні народження за проміжок ------

    def get_birthdays_in_range(self, days: int = 7) -> list[dict]:
        """
        Повернути контакти, у яких день народження припадає
        на проміжок від сьогодні до сьогодні + days (включно).

        День народження порівнюється лише за місяцем і числом
        (рік не враховується). Якщо ДН потрапляє на вихідний —
        вітання переноситься на найближчий понеділок.

        Args:
            days: кількість днів вперед (за замовчуванням 7)

        Returns:
            Список словників вигляду:
            [{"name": str, "congratulation_date": "DD.MM.YYYY"}, ...]
            відсортований за датою привітання.
        """
        today = date.today()
        end_date = today + timedelta(days=days)
        upcoming = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            bday = record.birthday.date

            # Підставляємо поточний рік для порівняння
            try:
                bday_this_year = bday.replace(year=today.year)
            except ValueError:
                # 29 лютого у не-високосний рік → 28 лютого
                bday_this_year = bday.replace(year=today.year, day=28)

            # Якщо вже минув — перевіряємо наступний рік
            if bday_this_year < today:
                try:
                    bday_this_year = bday.replace(year=today.year + 1)
                except ValueError:
                    bday_this_year = bday.replace(year=today.year + 1, day=28)

            if today <= bday_this_year <= end_date:
                # Перенесення з вихідних на понеділок
                congratulation_date = bday_this_year
                if congratulation_date.weekday() == 5:   # субота
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:  # неділя
                    congratulation_date += timedelta(days=1)

                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                    "_sort_key": congratulation_date,
                })

        # Сортуємо за датою привітання
        upcoming.sort(key=lambda x: x["_sort_key"])
        # Прибираємо службовий ключ
        for item in upcoming:
            del item["_sort_key"]

        return upcoming

    def __str__(self):
        if not self.data:
            return "Address book is empty."
        return "\n".join(str(record) for record in self.data.values())