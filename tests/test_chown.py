"""Тесты команды chown."""

import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from src.commands import command_chown
from src.path_utils import resolve_path
from src.vfs import load_vfs


VFS_DIR = Path(__file__).resolve().parent / "vfs"


class TestChown(unittest.TestCase):
    """Проверить команду chown."""

    def setUp(self):
        """Загрузить VFS перед каждым тестом."""
        self.vfs = load_vfs(VFS_DIR / "multiple")
        self.current_path = []

    def get_owner(self, path):
        """Получить владельца объекта VFS."""
        _, node = resolve_path(
            self.vfs,
            path,
            self.current_path
        )
        return node["owner"]

    def run_chown(self, arguments):
        """Запустить chown и получить вывод."""
        output = io.StringIO()

        with redirect_stdout(output):
            result = command_chown(
                self.vfs,
                self.current_path,
                arguments
            )

        return result, output.getvalue()

    def test_file_owner(self):
        """Изменить владельца файла."""
        result, _ = self.run_chown(
            ["sergey", "readme.txt"]
        )

        self.assertTrue(result)
        self.assertEqual(
            self.get_owner("readme.txt"),
            "sergey"
        )

    def test_directory_owner(self):
        """Изменить владельца каталога."""
        result, _ = self.run_chown(
            ["admin", "docs"]
        )

        self.assertTrue(result)
        self.assertEqual(
            self.get_owner("docs"),
            "admin"
        )

    def test_absolute_path(self):
        """Проверить абсолютный путь."""
        result, _ = self.run_chown(
            ["student", "/docs/info.txt"]
        )

        self.assertTrue(result)
        self.assertEqual(
            self.get_owner("/docs/info.txt"),
            "student"
        )

    def test_complex_path(self):
        """Проверить сложный путь."""
        result, _ = self.run_chown(
            ["user", "/docs/.././readme.txt"]
        )

        self.assertTrue(result)
        self.assertEqual(
            self.get_owner("readme.txt"),
            "user"
        )

    def test_relative_path(self):
        """Проверить путь от текущего каталога."""
        self.current_path[:] = ["docs"]

        result, _ = self.run_chown(
            ["student", "info.txt"]
        )

        self.assertTrue(result)
        self.assertEqual(
            self.get_owner("info.txt"),
            "student"
        )

    def test_no_arguments(self):
        """Проверить отсутствие аргументов."""
        result, output = self.run_chown([])

        self.assertFalse(result)
        self.assertIn(
            "ожидает владельца и путь",
            output
        )

    def test_one_argument(self):
        """Проверить один аргумент."""
        result, output = self.run_chown(
            ["sergey"]
        )

        self.assertFalse(result)
        self.assertIn(
            "ожидает владельца и путь",
            output
        )

    def test_too_many_arguments(self):
        """Проверить лишние аргументы."""
        result, output = self.run_chown(
            ["sergey", "readme.txt", "extra"]
        )

        self.assertFalse(result)
        self.assertIn(
            "ожидает владельца и путь",
            output
        )

    def test_missing_path(self):
        """Проверить отсутствующий объект."""
        result, output = self.run_chown(
            ["sergey", "missing.txt"]
        )

        self.assertFalse(result)
        self.assertIn(
            "путь не найден",
            output
        )

    def test_changes_only_in_memory(self):
        """Проверить изменение только в памяти."""
        self.run_chown(
            ["sergey", "readme.txt"]
        )

        new_vfs = load_vfs(VFS_DIR / "multiple")
        _, node = resolve_path(
            new_vfs,
            "readme.txt",
            []
        )

        self.assertEqual(node["owner"], "root")


if __name__ == "__main__":
    unittest.main()