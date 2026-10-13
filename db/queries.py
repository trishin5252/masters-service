"""Загрузка именованных SQL-запросов из sql/queries.sql."""

from functools import lru_cache

from .database import PROJECT_ROOT


@lru_cache(maxsize=1)
def all_queries():
    """Разделить SQL-файл по комментариям ``-- name:``."""
    result = {}
    name = None
    lines = []
    path = PROJECT_ROOT / 'sql' / 'queries.sql'
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('-- name: '):
            if name is not None:
                result[name] = '\n'.join(lines).strip()
            name = line.partition(':')[2].strip()
            lines = []
        elif name and line.strip() and not line.lstrip().startswith('--'):
            lines.append(line)
    if name is not None:
        result[name] = '\n'.join(lines).strip()
    return result


def sql(name):
    """Получить один проверенный запрос по имени."""
    return all_queries()[name]
