import tempfile
import unittest
from pathlib import Path

from time_validator import find_in_file, find_times, is_valid_time


class TimeValidationTests(unittest.TestCase):
    def test_valid_times(self):
        for value in ("00:00:00", "09:05:07", "19:59:59", "20:00:00",
                      "23:59:59"):
            with self.subTest(value=value):
                self.assertTrue(is_valid_time(value))

    def test_invalid_times(self):
        values = (
            "", "24:00:00", "29:00:00", "12:60:00", "12:00:60",
            "9:00:00", "09:0:00", "09:00:0", "009:00:00",
            "-1:00:00", "12-30-00", "12:30", "12:30:00.123",
            " 12:30:00", "12:30:00 ", "12:30:00\n", "abc12:30:00",
            "１２:３０:００", "١٢:٣٠:٠٠",
        )
        for value in values:
            with self.subTest(value=value):
                self.assertFalse(is_valid_time(value))

    def test_all_hours(self):
        for hour in range(100):
            with self.subTest(hour=hour):
                self.assertEqual(is_valid_time(f"{hour:02}:00:00"), hour < 24)

    def test_all_minutes_and_seconds(self):
        for number in range(100):
            with self.subTest(number=number):
                self.assertEqual(is_valid_time(f"12:{number:02}:00"), number < 60)
                self.assertEqual(is_valid_time(f"12:00:{number:02}"), number < 60)


class TimeSearchTests(unittest.TestCase):
    def test_search_with_punctuation(self):
        text = "Начало (09:00:00), конец - 23:59:59.\n[00:00:00]"
        self.assertEqual(find_times(text), ["09:00:00", "23:59:59", "00:00:00"])

    def test_search_preserves_duplicates(self):
        self.assertEqual(find_times("09:00:00; 09:00:00"),
                         ["09:00:00", "09:00:00"])

    def test_search_skips_invalid_times(self):
        self.assertEqual(find_times("24:00:00 12:60:00 12:00:60 9:00:00"), [])

    def test_search_does_not_extract_parts(self):
        values = (
            "109:00:00", "09:00:001", "12:30:00:10", "1:12:30:00",
            "abc09:00:00", "09:00:00abc", "текст09:00:00",
            "_09:00:00", "09:00:00_", "١09:00:00",
        )
        for value in values:
            with self.subTest(value=value):
                self.assertEqual(find_times(value), [])

    def test_empty_text_and_no_matches(self):
        self.assertEqual(find_times(""), [])
        self.assertEqual(find_times("Время не указано"), [])


class FileSearchTests(unittest.TestCase):
    def test_utf8_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "schedule.txt"
            path.write_text("Начало: 09:00:00\nКонец: 12:30:00", encoding="utf-8")
            self.assertEqual(find_in_file(path), ["09:00:00", "12:30:00"])

    def test_file_with_bom(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "schedule.txt"
            path.write_text("09:00:00", encoding="utf-8-sig")
            self.assertEqual(find_in_file(path), ["09:00:00"])

    def test_empty_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "empty.txt"
            path.write_text("", encoding="utf-8")
            self.assertEqual(find_in_file(path), [])

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(FileNotFoundError):
                find_in_file(Path(folder) / "missing.txt")

    def test_wrong_encoding(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "wrong.txt"
            path.write_bytes(b"\xff\xfe\xff")
            with self.assertRaises(UnicodeError):
                find_in_file(path)


if __name__ == "__main__":
    unittest.main()
