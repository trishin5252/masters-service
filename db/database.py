"""Подключение к отдельной базе предметной области."""

import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / 'data' / 'masters_service.sqlite'
SCHEMA_PATH = PROJECT_ROOT / 'sql' / 'schema.sql'


def get_connection():
    """Открыть SQLite с именованными строками и проверкой внешних ключей."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute('PRAGMA foreign_keys = ON')
    return connection


def create_schema(connection):
    """Создать таблицы и индексы из отдельного SQL-файла."""
    connection.executescript(SCHEMA_PATH.read_text(encoding='utf-8'))
