from .fields import Birthday, Email, Name, Phone


# Клас для запису в адресній книзі, містить ім'я, телефони,
# email та день народження
class Record:
    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: list[Phone] = []
        self.email: Email | None = None
        self.birthday: Birthday | None = None

    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def set_email(self, email: str) -> None:
        self.email = Email(email)

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def __str__(self) -> str:
        phones = (
            "; ".join(phone.value for phone in self.phones)
            if self.phones
            else "немає"
        )
        email_str = str(self.email) if self.email else "відсутній"
        birthday_str = str(self.birthday) if self.birthday else "не вказано"

        return (
            f"👤 {self.name.value:<15} | 📞 {phones:<12} | "
            f"📧 {email_str:<20} | 🎂 {birthday_str}"
        )
