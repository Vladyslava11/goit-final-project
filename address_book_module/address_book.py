from collections import UserDict
from .record import Record



# Додавання контактів, видалення та виведення всіх контактів
class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        key = record.name.value.lower()
        if key in self.data:
            # Якщо контакт з таким ім'ям вже існує, виводимо повідомлення що вже існує
            raise ValueError(f"❌ Контакт з ім'ям '{record.name.value}' вже існує.")
        self.data[key] = record

    def delete(self, name: str) -> bool:
        if name.lower() in self.data:
            del self.data[name.lower()]
            return True
        return False

    def get_all_records(self) -> str:
        if not self.data:
            return "📭 Адресна книга порожня."

        return "\n".join(str(record) for record in self.data.values())
