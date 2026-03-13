import re
from datetime import datetime


# Базовий клас для полів запису
class Field:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


# Клас для імені, успадковує Field без додаткової логіки
class Name(Field):
    pass


# Клас для телефону, перевіряє формат номера при ініціалізації
class Phone(Field):
    def __init__(self, value: str) -> None:
        # Перевіряємо, чи немає в номері заборонених символів (наприклад, букв)
        # дужки, дефіси та пробіли дозволені
        if not re.fullmatch(r"[0-9()\-\s]+", value):
            raise ValueError(
                f"❌ Номер '{value}' некоректний. "
                f"Використовуйте лише цифри. Приклад: 0936657545"
            )

        clean_value = re.sub(r"\D", "", value)
        # Перевіряємо, чи номер складається з 10 цифр і починається з '0'
        if not re.fullmatch(r"0\d{9}", clean_value):
            raise ValueError(
                f"❌ Номер '{value}' некоректний. "
                f"Має бути 10 цифр і починатися з '0'. Приклад: 0936657545"
            )

        super().__init__(clean_value)


# Клас для email, перевіряє формат адреси при ініціалізації
class Email(Field):
    def __init__(self, value: str) -> None:
        if not value.isascii():
            raise ValueError(
                "❌ Email має містити лише латинські літери та символи."
            )

        pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        if not re.fullmatch(pattern, value):
            raise ValueError(
                "❌ Некоректний формат адреси. "
                "Приклад: user@example.com"
            )
        super().__init__(value)


# Клас для дня народження, перевіряє формат дати при ініціалізації
class Birthday(Field):
    def __init__(self, value: str) -> None:
        try:
            date_obj = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(date_obj)
        except ValueError as e:
            raise ValueError("❌ Формат дати має бути ДД.ММ.РРРР") from e

    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y")
