"""
Головний файл бота-асистента для керування контактами.

Цей модуль надає інтерфейс командного рядка для керування контактами.
Підтримує додавання, зміну, перегляд та видалення контактів,
а також роботу з днями народження.

Основні можливості:
    - Додавання та зміна контактів з іменами та телефонами
    - Пошук телефонних номерів за іменем
    - Перегляд усіх контактів
    - Додавання та перегляд днів народження
    - Отримання списку днів народжень на наступний тиждень

Команди бота:
    add [ім'я] [телефон] - додати новий контакт або телефон до існуючого
    change [ім'я] [новий телефон] - змінити телефон існуючого контакту
    phone [ім'я] - показати телефони вказаного контакту
    all - показати всі контакти
    add-birthday [ім'я] [DD.MM.YYYY] - додати день народження
    show-birthday [ім'я] - показати день народження контакту
    birthdays - показати дні народження на наступному тижні
    hello - отримати вітання від бота
    close або exit - вийти з програми
"""

from functools import wraps

from commands_enum import Command


# ============================================
# Декоратор обробки помилок
# ============================================


def input_error(func):
    """
    Декоратор для обробки помилок у функціях команд.
    
    Перехоплює поширені виключення та повертає зрозумілі повідомлення про помилки.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return f"Contact '{e.args[0]}' not found."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Not enough arguments. Check your input."
    return wrapper


# ============================================
# Парсер команд
# ============================================


def parse_input(user_input: str) -> tuple[str, list[str]]:
    """
    Парсить ввід користувача та розділяє на команду та аргументи.
    
    Рядок розділяється по пробілах. Перше слово - команда,
    решта - аргументи.
    
    Args:
        user_input: Рядок введений користувачем
        
    Returns:
        Кортеж з двох елементів: (команда, список аргументів)
    """
    parts = user_input.strip().split()
    cmd = parts[0].lower() if parts else ""
    args = parts[1:]
    return cmd, args


# ============================================
# Головна функція
# ============================================


def main():
    """
    Головна функція бота-асистента.
    
    Запускає інтерактивний цикл обробки команд користувача.
    Підтримує команди: hello, add, change, phone, all, add-birthday, show-birthday, birthdays, close, exit
    """
    print("Welcome to the assistant bot!")
    print("Commands: hello, add, change, phone, all, add-birthday, show-birthday, birthdays, close, exit")

    while True:
        user_input = input("Enter a command: ")
        
        # Handle empty input
        if not user_input.strip():
            print("Please enter a command.")
            continue
            
        command, args = parse_input(user_input)

        if command in ("close", "exit"):
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            # TODO: Реалізувати додавання контакту
            print("Add command - to be implemented")

        elif command == "change":
            # TODO: Реалізувати зміну контакту
            print("Change command - to be implemented")

        elif command == "phone":
            # TODO: Реалізувати пошук телефону
            print("Phone command - to be implemented")

        elif command == "all":
            # TODO: Реалізувати показ усіх контактів
            print("All command - to be implemented")

        elif command == "add-birthday":
            # TODO: Реалізувати додавання дня народження
            print("Add birthday command - to be implemented")

        elif command == "show-birthday":
            # TODO: Реалізувати показ дня народження
            print("Show birthday command - to be implemented")

        elif command == "birthdays":
            # TODO: Реалізувати показ днів народжень
            print("Birthdays command - to be implemented")

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
