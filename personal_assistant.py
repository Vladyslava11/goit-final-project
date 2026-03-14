"""Головний файл бота-асистента."""

from datetime import datetime
from notebook_module import Notebook
from storage_module import save_data, load_data
from address_book_module.address_book import AddressBook
from address_book_module.record import Record


def input_error(func):
    """Декоратор для обробки помилок введення."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return f"Контакт '{e.args[0]}' не знайдено."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Недостатньо аргументів."
    return wrapper


def parse_input(user_input):
    """Розділити введення на команду та аргументи."""
    parts = user_input.strip().split()
    cmd = parts[0].lower() if parts else ""
    args = parts[1:]
    return cmd, args


def suggest_command(user_input: str) -> str | None:
    """Запропонувати найближчу команду на основі введення."""
    from difflib import get_close_matches
    
    commands = [
        "hello", "help", "add", "change", "phone", "all", "delete",
        "add-birthday", "show-birthday", "birthdays",
        "add-note", "edit-note", "delete-note", "find-note", "show-all-notes",
        "add-tag", "search-by-tag", "sort-notes-by-tag",
        "close", "exit"
    ]
    
    user_input_lower = user_input.lower().strip()
    
    # Точний збіг
    if user_input_lower in commands:
        return None
    
    # Спроба знайти близькі збіги
    matches = get_close_matches(user_input_lower, commands, n=1, cutoff=0.6)
    if matches:
        return matches[0]
    
    # Перевірка чи користувач намагається додати контакт
    add_patterns = ["додати", "додаю", "новий контакт", "new contact", "add contact"]
    if any(p in user_input_lower for p in add_patterns):
        return "add"
    
    # Перевірка чи користувач шукає контакт
    find_patterns = ["знайти", "пошук", "шукаю", "find", "search"]
    if any(p in user_input_lower for p in find_patterns):
        return "phone"
    
    # Перевірка чи користувач хоче побачити всі контакти
    all_patterns = ["всі", "усі", "показати всіх", "all contacts", "show all"]
    if any(p in user_input_lower for p in all_patterns):
        return "all"
    
    # Перевірка чи користувач хоче додати нотатку
    note_patterns = ["нотатку", "нотатка", "замітка", "note"]
    if any(p in user_input_lower for p in note_patterns):
        return "add-note"
    
    return None


def main():
    """Головна функція бота-асистента."""
    book = load_data("addressbook.pkl", AddressBook)
    notebook = load_data("notebook.pkl", Notebook)

    print("Ласкаво просимо до персонального помічника!")
    print("Введіть 'help' для списку команд.")

    while True:
        user_input = input("\nВведіть команду: ")

        if not user_input.strip():
            print("Будь ласка, введіть команду.")
            print("Введіть 'help' для списку доступних команд.")
            continue

        command, args = parse_input(user_input)

        if command in ("close", "exit"):
            save_data(book, "addressbook.pkl")
            save_data(notebook, "notebook.pkl")
            print("До побачення!")
            break

        elif command == "hello":
            print("Чим можу допомогти?")

        elif command == "help":
            print("""
📋 Доступні команди:

👤 Робота з контактами:
   add - додати новий контакт
         Приклад: add Олександр 0991234567
         Приклад: add Олександр 0991234567 alex@email.com
         Приклад: add Олександр 0991234567 alex@email.com Київ
         Приклад: add Олександр 0991234567 alex@email.com Київ 15.05.1990
         Обов'язкові: ім'я, телефон
         Необов'язкові: email, адреса, день народження

   change - змінити дані контакту
         Приклад: change Олександр phone 0999999999
         Приклад: change Олександр address Київ вул. Садова 5
         Приклад: change Олександр birthday 20.12.1985
         Поля для зміни: phone, email, address, birthday

   phone - показати номер телефону контакту
         Приклад: phone Олександр

   all - показати всі контакти

   delete - видалити контакт
         Приклад: delete Олександр

   add-birthday - додати день народження
         Приклад: add-birthday Олександр 15.05.1990

   show-birthday - показати день народження контакту
         Приклад: show-birthday Олександр

   birthdays - показати дні народження найближчим часом
         Приклад: birthdays (покаже на 7 днів)
         Приклад: birthdays 30 (покаже на 30 днів)

📝 Робота з нотатками:
   add-note - додати нотатку
         Приклад: add-note Покупки Купити молоко та хліб

   edit-note - редагувати нотатку
         Приклад: edit-note 1 Новий заголовок Новий текст

   delete-note - видалити нотатку
         Приклад: delete-note 1

   find-note - шукати нотатку
         Приклад: find-note Покупки

   show-all-notes - показати всі нотатки

🏷️ Робота з тегами:
   add-tag - додати тег до нотатки
         Приклад: add-tag 1 Покупки

   search-by-tag - шукати нотатки за тегом
         Приклад: search-by-tag Покупки

   sort-notes-by-tag - сортувати нотатки за тегами

🚪 Вихід:
   close або exit - вийти та зберегти дані
""")

        elif command == "add":
            # add [name] [phone] [email] [address] [birthday]
            if len(args) < 2:
                print("Використання: add <ім'я> <телефон> [email] [адреса] [день_народження]")
                print("Обов'язкові поля: ім'я, телефон")
            else:
                name = args[0]
                phone = args[1]
                
                # Email, адреса та день народження - все що після телефону
                email = None
                address = None
                birthday = None
                if len(args) > 2:
                    remaining = args[2:]
                    bday_idx = None
                    for i, arg in enumerate(remaining):
                        if len(arg) == 10 and arg[2] == '.' and arg[5] == '.':
                            bday_idx = i
                            break
                    
                    if bday_idx is not None:
                        # Email - перше слово перед датою
                        if bday_idx > 0:
                            email = remaining[0]
                            address = " ".join(remaining[1:bday_idx]) if bday_idx > 1 else None
                        birthday = remaining[bday_idx]
                    else:
                        # Немає дня народження - все інше це email + адреса
                        if len(remaining) >= 1:
                            email = remaining[0]
                        if len(remaining) > 1:
                            address = " ".join(remaining[1:])
                
                # Перевірка обов'язкових полів
                if not name or not name.strip():
                    print("❌ Ім'я є обов'язковим.")
                elif not phone or not phone.strip():
                    print("❌ Телефон є обов'язковим.")
                else:
                    try:
                        record = Record(name)
                        record.add_phone(phone)
                        if email:
                            record.set_email(email)
                        if address:
                            record.set_address(address)
                        if birthday:
                            record.add_birthday(birthday)
                        book.add_record(record)
                        print(f"✅ Контакт '{name}' додано.")
                    except ValueError as e:
                        print(e)

        elif command == "change":
            # change [name] [поле] [значення]
            if len(args) < 3:
                print("Використання: change <ім'я> <поле> <значення>")
                print("Поля: phone, email, address, birthday")
            else:
                name = args[0].lower()
                field = args[1].lower()
                value = " ".join(args[2:])  # Об'єднуємо все після поля
                if name in book.data:
                    try:
                        record = book.data[name]
                        if field == "phone":
                            record.phones.clear()
                            record.add_phone(value)
                            print(f"✅ Телефон для '{args[0]}' оновлено.")
                        elif field == "email":
                            record.set_email(value)
                            print(f"✅ Email для '{args[0]}' оновлено.")
                        elif field == "address":
                            record.set_address(value)
                            print(f"✅ Адреса для '{args[0]}' оновлено/додано.")
                        elif field == "birthday":
                            record.add_birthday(value)
                            print(f"✅ День народження для '{args[0]}' оновлено/додано.")
                        else:
                            print(f"❌ Невідоме поле: {field}")
                            print("Доступні поля: phone, email, address, birthday")
                    except ValueError as e:
                        print(e)
                else:
                    print(f"❌ Контакт '{args[0]}' не знайдено.")

        elif command == "phone":
            # phone [name]
            if len(args) < 1:
                print("Використання: phone <ім'я>")
            else:
                name = args[0].lower()
                if name in book.data:
                    record = book.data[name]
                    phones = "; ".join(p.value for p in record.phones)
                    print(f"📞 {args[0]}: {phones}")
                else:
                    print(f"❌ Контакт '{args[0]}' не знайдено.")

        elif command == "all":
            # all
            print(book.get_all_records())

        elif command == "delete":
            # delete [name]
            if len(args) < 1:
                print("Використання: delete <ім'я>")
            else:
                name = args[0].lower()
                if book.delete(name):
                    print(f"✅ Контакт '{args[0]}' видалено.")
                else:
                    print(f"❌ Контакт '{args[0]}' не знайдено.")

        elif command == "add-birthday":
            # add-birthday [name] [DD.MM.YYYY]
            if len(args) < 2:
                print("Використання: add-birthday <ім'я> <DD.MM.YYYY>")
            else:
                name = args[0].lower()
                if name in book.data:
                    try:
                        book.data[name].add_birthday(args[1])
                        print(f"✅ День народження для '{args[0]}' додано.")
                    except ValueError as e:
                        print(e)
                else:
                    print(f"❌ Контакт '{args[0]}' не знайдено.")

        elif command == "show-birthday":
            # show-birthday [name]
            if len(args) < 1:
                print("Використання: show-birthday <ім'я>")
            else:
                name = args[0].lower()
                if name in book.data:
                    record = book.data[name]
                    if record.birthday:
                        print(f"🎂 {args[0]}: {record.birthday}")
                    else:
                        print(f"День народження для '{args[0]}' не вказано.")
                else:
                    print(f"❌ Контакт '{args[0]}' не знайдено.")

        elif command == "birthdays":
            # birthdays [кількість_днів]
            days = 7  # за замовчуванням
            if len(args) >= 1:
                try:
                    days = int(args[0])
                except ValueError:
                    print("❌ Кількість днів має бути числом.")
                    pass
            
            today = datetime.now().date()
            upcoming = []
            for record in book.data.values():
                if record.birthday:
                    bday = record.birthday.value
                    this_year_bday = bday.replace(year=today.year)
                    if this_year_bday < today:
                        this_year_bday = bday.replace(year=today.year + 1)
                    days_until = (this_year_bday - today).days
                    if 0 <= days_until <= days:
                        upcoming.append((record.name.value, this_year_bday.strftime("%d.%m.%Y"), days_until))
            if upcoming:
                upcoming.sort(key=lambda x: x[2])
                print(f"🎂 Дні народження протягом {days} днів:")
                for name, bday, days_left in upcoming:
                    print(f"  {name}: {bday} (через {days_left} днів)")
            else:
                print(f"Немає днів народження протягом {days} днів.")

        elif command == "add-note":
            # add-note [title] [body]
            if len(args) < 2:
                print("Використання: add-note <заголовок> <текст>")
            else:
                title = args[0]
                body = " ".join(args[1:])
                try:
                    notebook.add_note(title, body)
                    print(f"✅ Нотатку '{title}' додано.")
                except ValueError as e:
                    print(e)

        elif command == "edit-note":
            # edit-note [id] [title] [body]
            if len(args) < 3:
                print("Використання: edit-note <id> <заголовок> <текст>")
            else:
                try:
                    note_id = int(args[0])
                    title = args[1]
                    body = " ".join(args[2:])
                    notebook.edit_note(note_id, title, body)
                    print(f"✅ Нотатку {note_id} оновлено.")
                except ValueError as e:
                    print(e)
                except IndexError:
                    print("❌ Нотатку не знайдено.")

        elif command == "delete-note":
            # delete-note [id]
            if len(args) < 1:
                print("Використання: delete-note <id>")
            else:
                try:
                    note_id = int(args[0])
                    notebook.delete_note(note_id)
                    print(f"✅ Нотатку {note_id} видалено.")
                except ValueError as e:
                    print(e)

        elif command == "find-note":
            # find-note [query]
            if len(args) < 1:
                print("Використання: find-note <запит>")
            else:
                query = " ".join(args)
                results = notebook.find_note(query)
                if results:
                    print("🔍 Результати пошуку:")
                    for note in results:
                        print(note)
                else:
                    print("Нотаток не знайдено.")

        elif command == "show-all-notes":
            # show-all-notes
            notes = notebook.get_all_notes()
            if notes:
                for note in notes:
                    print(note)
            else:
                print("Нотаток немає.")

        elif command == "add-tag":
            # add-tag [note_id] [tag]
            if len(args) < 2:
                print("Використання: add-tag <id> <тег>")
            else:
                try:
                    note_id = int(args[0])
                    tag = args[1]
                    note = notebook.get_note_by_id(note_id)
                    if note:
                        note.add_tag(tag)
                        print(f"✅ Тег '{tag}' додано до нотатки {note_id}.")
                    else:
                        print(f"❌ Нотатку {note_id} не знайдено.")
                except ValueError as e:
                    print(e)

        elif command == "search-by-tag":
            # search-by-tag [tag]
            if len(args) < 1:
                print("Використання: search-by-tag <тег>")
            else:
                tag = args[0]
                results = notebook.search_by_tag(tag)
                if results:
                    print("🔍 Нотатки з тегом:")
                    for note in results:
                        print(note)
                else:
                    print("Нотаток з таким тегом не знайдено.")

        elif command == "sort-notes-by-tag":
            # sort-notes-by-tag
            sorted_notes = notebook.sort_by_tags()
            if sorted_notes:
                print("📋 Нотатки відсортовані за тегами:")
                for note in sorted_notes:
                    print(note)
            else:
                print("Немає нотаток для сортування.")

        else:
            suggestion = suggest_command(user_input)
            if suggestion:
                print(f"❌ Невідома команда. Можливо, ви мали на увазі '{suggestion}'?")
            else:
                print("Невідома команда.")
            print("Введіть 'help' для списку доступних команд.")


if __name__ == "__main__":
    main()
