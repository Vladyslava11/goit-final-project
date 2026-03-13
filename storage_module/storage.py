"""Модуль серіалізації даних для персонального помічника."""

import pickle
from pathlib import Path

DATA_DIR = Path.home() / ".personal_assistant"
DATA_DIR.mkdir(exist_ok=True)


def save_data(data, filename):
    """Зберегти дані у файл."""
    filepath = DATA_DIR / filename
    with open(filepath, "wb") as f:
        pickle.dump(data, f)


def load_data(filename, default_factory=None):
    """Завантажити дані з файлу."""
    filepath = DATA_DIR / filename
    try:
        with open(filepath, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return default_factory() if default_factory else None
