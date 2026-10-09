"""Тесты команды cd."""

import unittest
from pathlib import Path

from src.commands import command_cd
from src.vfs import load_vfs


VFS_DIR = Path(__file__).resolve().parent / "vfs"


class TestCd(unittest.TestCase):
    """Проверить переходы между каталогами."""

    def setUp(self):
        """Подготовить VFS перед тестом."""
        self.vfs = load_vfs(VFS_DIR / "nested")
        self.current_path = []

    def test_relative_path(self):
        """Проверить относительный путь."""
        result = command_cd(
            self.vfs,
            self.current_path,
            ["level1"]
        )

        self.assertTrue(result)
        self.assertEqual(
            self.current_path,
            ["level1"]
        )

    def test_nested_path(self):
        """Проверить переход сразу через несколько каталогов."""
        result = command_cd(
            self.vfs,
            self.current_path,
            ["level1/level2/level3"]
        )

        self.assertTrue(result)
        self.assertEqual(
            self.current_path,
            ["level1", "level2", "level3"]
        )

    def test_absolute_path(self):
        """Проверить абсолютный путь."""
        self.current_path[:] = ["level1"]

        result = command_cd(
            self.vfs,
            self.current_path,
            ["/level1/level2"]
        )

        self.assertTrue(result)
        self.assertEqual(
            self.current_path,
            ["level1", "level2"]
        )

    def test_parent_directory(self):
        """Проверить переход через две точки."""
        self.current_path[:] = [
            "level1",
            "level2",
            "level3"
        ]

        result = command_cd(
            self.vfs,
            self.current_path,
            ["../.."]
        )

        self.assertTrue(result)
        self.assertEqual(
            self.current_path,
            ["level1"]
        )

    def test_complex_path(self):
        """Проверить сложную конструкцию пути."""
        result = command_cd(
            self.vfs,
            self.current_path,
            [
                "/level1/level2/"
                "../level2/./level3"
            ]
        )

        self.assertTrue(result)
        self.assertEqual(
            self.current_path,
            ["level1", "level2", "level3"]
        )

    def test_root(self):
        """Проверить переход в корень."""
        self.current_path[:] = ["level1", "level2"]

        result = command_cd(
            self.vfs,
            self.current_path,
            ["/"]
        )

        self.assertTrue(result)
        self.assertEqual(self.current_path, [])

    def test_missing_directory(self):
        """Проверить отсутствующий каталог."""
        result = command_cd(
            self.vfs,
            self.current_path,
            ["missing"]
        )

        self.assertFalse(result)
        self.assertEqual(self.current_path, [])

    def test_file_instead_of_directory(self):
        """Проверить попытку перейти в файл."""
        result = command_cd(
            self.vfs,
            self.current_path,
            ["root.txt"]
        )

        self.assertFalse(result)
        self.assertEqual(self.current_path, [])


if __name__ == "__main__":
    unittest.main()