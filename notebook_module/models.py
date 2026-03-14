"""Моделі даних для модуля нотаток."""

from datetime import datetime


class Tag:
    """Тег для категоризації нотаток."""

    def __init__(self, value):
        stripped = value.strip().lower()
        if not stripped:
            raise ValueError("Тег не може бути порожнім.")
        self.value = stripped

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, Tag):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash(self.value)


class Note:
    """Текстова нотатка з заголовком, тілом та тегами."""

    def __init__(self, note_id, title, body):
        title = title.strip()
        if not title:
            raise ValueError("Заголовок не може бути порожнім.")
        body = body.strip()
        if not body:
            raise ValueError("Текст нотатки не може бути порожнім.")
        self.note_id = note_id
        self.title = title
        self.body = body
        self.tags = []
        self.created_at = datetime.now()

    def add_tag(self, tag):
        """Додати тег до нотатки."""
        new_tag = Tag(tag)
        if new_tag in self.tags:
            raise ValueError("Тег вже існує.")
        self.tags.append(new_tag)

    def remove_tag(self, tag):
        """Видалити тег з нотатки."""
        target = Tag(tag)
        if target not in self.tags:
            raise ValueError("Тег не знайдено.")
        self.tags.remove(target)

    def edit_title(self, new_title):
        """Змінити заголовок нотатки."""
        new_title = new_title.strip()
        if not new_title:
            raise ValueError("Заголовок не може бути порожнім.")
        self.title = new_title

    def edit_body(self, new_body):
        """Змінити текст нотатки."""
        new_body = new_body.strip()
        if not new_body:
            raise ValueError("Текст нотатки не може бути порожнім.")
        self.body = new_body

    def __str__(self):
        tags_str = ", ".join(str(t) for t in self.tags) if self.tags else "без тегів"
        date_str = self.created_at.strftime("%d.%m.%Y")
        return f"[{self.note_id}] {self.title} | Теги: {tags_str} | {date_str}"

    def __repr__(self):
        """Повне представлення нотатки з текстом."""
        tags_str = ", ".join(str(t) for t in self.tags) if self.tags else "без тегів"
        date_str = self.created_at.strftime("%d.%m.%Y")
        return (
            f"─── Нотатка #{self.note_id} ───\n"
            f"📌 Заголовок: {self.title}\n"
            f"📝 Текст: {self.body}\n"
            f"🏷️ Теги: {tags_str}\n"
            f"📅 Дата: {date_str}\n"
            f"────────────────────"
        )
