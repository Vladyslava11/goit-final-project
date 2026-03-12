"""Головний файл бота-асистента."""

from notebook_module import Notebook
from storage_module import save_data, load_data


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


def main():
    """Головна функція бота-асистента."""
    # from address_book_module import AddressBook
    # book = load_data("addressbook.pkl", AddressBook)
    notebook = load_data("notebook.pkl", Notebook)

    print("Ласкаво просимо до персонального помічника!")

    while True:
        user_input = input("Введіть команду: ")

        if not user_input.strip():
            print("Будь ласка, введіть команду.")
            continue

        command, args = parse_input(user_input)

        if command in ("close", "exit"):
            # save_data(book, "addressbook.pkl")
            save_data(notebook, "notebook.pkl")
            print("До побачення!")
            break

        elif command == "hello":
            print("Чим можу допомогти?")

        elif command == "add":
            # TODO: додавання контакту
            print("Команда add - буде реалізовано")

        elif command == "change":
            # TODO: зміна контакту
            print("Команда change - буде реалізовано")

        elif command == "phone":
            # TODO: пошук телефону
            print("Команда phone - буде реалізовано")

        elif command == "all":
            # TODO: показ усіх контактів
            print("Команда all - буде реалізовано")

        elif command == "add-birthday":
            # TODO: додавання дня народження
            print("Команда add-birthday - буде реалізовано")

        elif command == "show-birthday":
            # TODO: показ дня народження
            print("Команда show-birthday - буде реалізовано")

        elif command == "birthdays":
            # TODO: показ днів народжень
            print("Команда birthdays - буде реалізовано")

        elif command == "add-note":
            # TODO: додавання нотатки
            print("Команда add-note - буде реалізовано")

        elif command == "edit-note":
            # TODO: редагування нотатки
            print("Команда edit-note - буде реалізовано")

        elif command == "delete-note":
            # TODO: видалення нотатки
            print("Команда delete-note - буде реалізовано")

        elif command == "find-note":
            # TODO: пошук нотатки
            print("Команда find-note - буде реалізовано")

        elif command == "show-all-notes":
            # TODO: показ усіх нотаток
            print("Команда show-all-notes - буде реалізовано")

        elif command == "add-tag":
            # TODO: додавання тегу
            print("Команда add-tag - буде реалізовано")

        elif command == "search-by-tag":
            # TODO: пошук за тегом
            print("Команда search-by-tag - буде реалізовано")

        elif command == "sort-notes-by-tag":
            # TODO: сортування нотаток за тегами
            print("Команда sort-notes-by-tag - буде реалізовано")

        else:
            print("Невідома команда.")


if __name__ == "__main__":
    main()
