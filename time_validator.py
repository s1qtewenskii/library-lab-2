"""Проверка и поиск времени в формате ЧЧ:ММ:СС."""

import re


TIME_PATTERN = r"(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]"
TIME_RE = re.compile(TIME_PATTERN)
# Границы не позволяют извлечь время из слова или более длинной записи.
SEARCH_RE = re.compile(r"(?<![\w:])" + TIME_PATTERN + r"(?![\w:])")


def is_valid_time(value):
    """Проверяет всю строку, включая количество цифр."""
    return TIME_RE.fullmatch(value) is not None


def find_times(text):
    """Возвращает найденное время в порядке появления, с повторами."""
    return SEARCH_RE.findall(text)


def find_in_file(filename):
    """Читает текстовый файл в кодировке UTF-8 и ищет в нем время."""
    with open(filename, encoding="utf-8-sig") as file:
        return find_times(file.read())
