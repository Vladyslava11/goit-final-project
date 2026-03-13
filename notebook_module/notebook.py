"""Модуль управління нотатками."""

from .models import Note, Tag


class Notebook:
    """Колекція нотаток."""

    def __init__(self):
        self._notes = []
        self._next_id = 1

    def add_note(self, title, body):
        """Додати нову нотатку."""
        note = Note(self._next_id, title, body)
        self._notes.append(note)
        self._next_id += 1
        return note

    def find_note(self, query):
        """Знайти нотатки за ключовим словом."""
        q = query.lower()
        return [
            note for note in self._notes
            if q in note.title.lower() or q in note.body.lower()
        ]

    def get_note_by_id(self, note_id):
        """Знайти нотатку за ID."""
        for note in self._notes:
            if note.note_id == note_id:
                return note
        return None

    def edit_note(self, note_id, title=None, body=None):
        """Відредагувати нотатку."""
        note = self.get_note_by_id(note_id)
        if note is None:
            raise ValueError(f"Нотатку з ID {note_id} не знайдено.")
        if title is not None:
            note.edit_title(title)
        if body is not None:
            note.edit_body(body)

    def delete_note(self, note_id):
        """Видалити нотатку за ID."""
        note = self.get_note_by_id(note_id)
        if note is None:
            raise ValueError(f"Нотатку з ID {note_id} не знайдено.")
        self._notes.remove(note)

    def search_by_tag(self, tag):
        """Знайти нотатки за тегом."""
        target = Tag(tag)
        return [note for note in self._notes if target in note.tags]

    def sort_by_tags(self):
        """Повернути нотатки, відсортовані за першим тегом."""
        return sorted(
            self._notes,
            key=lambda n: (not n.tags, str(n.tags[0]) if n.tags else ""),
        )

    def get_all_notes(self):
        """Повернути всі нотатки."""
        return list(self._notes)
