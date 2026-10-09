"""Тесты обработки путей VFS."""

import unittest

from src.path_utils import format_path
from src.path_utils import normalize_path


class TestPaths(unittest.TestCase):
    """Проверить нормализацию путей VFS."""

    def test_absolute_path(self):
        """Проверить абсолютный путь с точками."""
        result = normalize_path(
            "/projects/student/files/../../archive/././docs",
            []
        )
        self.assertEqual(
            result,
            ["projects", "archive", "docs"]
        )

    def test_relative_path(self):
        """Проверить относительный путь."""
        result = normalize_path(
            "../shared/docs",
            ["home", "user"]
        )
        self.assertEqual(
            result,
            ["home", "shared", "docs"]
        )

    def test_current_directory(self):
        """Проверить использование точки."""
        result = normalize_path(
            "./docs/./file",
            ["home"]
        )
        self.assertEqual(
            result,
            ["home", "docs", "file"]
        )

    def test_parent_from_root(self):
        """Проверить невозможность выйти выше корня."""
        result = normalize_path(
            "/../../../home",
            []
        )
        self.assertEqual(result, ["home"])

    def test_repeated_slashes(self):
        """Проверить повторяющиеся разделители."""
        result = normalize_path(
            "/home///user//docs",
            []
        )
        self.assertEqual(
            result,
            ["home", "user", "docs"]
        )

    def test_windows_slashes(self):
        """Проверить обратные слеши."""
        result = normalize_path(
            r"\home\user\..\buddy",
            []
        )
        self.assertEqual(
            result,
            ["home", "buddy"]
        )

    def test_format_root(self):
        """Проверить отображение корня."""
        self.assertEqual(format_path([]), "/")

    def test_format_path(self):
        """Проверить отображение обычного пути."""
        result = format_path(["home", "shared", "docs"])
        self.assertEqual(result, "/home/shared/docs")


if __name__ == "__main__":
    unittest.main()