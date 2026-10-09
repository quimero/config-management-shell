"""Тесты команды ls."""

import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from src.commands import command_ls
from src.vfs import load_vfs


VFS_DIR = Path(__file__).resolve().parent / "vfs"


class TestLs(unittest.TestCase):
    """Проверить режимы команды ls."""

    def setUp(self):
        """Подготовить VFS перед каждым тестом."""
        self.vfs = load_vfs(VFS_DIR / "multiple")
        self.current_path = []

    def run_ls(self, arguments):
        """Запустить ls и получить результат вывода."""
        output = io.StringIO()

        with redirect_stdout(output):
            result = command_ls(
                self.vfs,
                self.current_path,
                arguments
            )

        return result, output.getvalue()

    def test_simple_ls(self):
        """Проверить обычный ls."""
        result, output = self.run_ls([])

        self.assertTrue(result)
        self.assertIn("readme.txt", output)
        self.assertIn("config.ini", output)
        self.assertIn("docs", output)
        self.assertNotIn(".hidden.txt", output)

    def test_all_option(self):
        """Проверить ключ -a."""
        result, output = self.run_ls(["-a"])

        self.assertTrue(result)
        self.assertIn(".hidden.txt", output)
        self.assertIn(".", output)
        self.assertIn("..", output)

    def test_long_option(self):
        """Проверить ключ -l."""
        result, output = self.run_ls(["-l"])

        self.assertTrue(result)
        self.assertIn("root", output)
        self.assertIn("readme.txt", output)
        self.assertIn("docs", output)

    def test_human_option(self):
        """Проверить ключ -h."""
        result, output = self.run_ls(["-h"])

        self.assertTrue(result)
        self.assertIn("readme.txt", output)

    def test_long_human_options(self):
        """Проверить комбинацию -lh."""
        result, output = self.run_ls(["-lh"])

        self.assertTrue(result)
        self.assertIn("root", output)
        self.assertIn("B", output)

    def test_all_combined_options(self):
        """Проверить объединённые ключи -lah."""
        result, output = self.run_ls(["-lah"])

        self.assertTrue(result)
        self.assertIn(".hidden.txt", output)
        self.assertIn("root", output)
        self.assertIn("B", output)

    def test_separate_options(self):
        """Проверить раздельные ключи."""
        result, output = self.run_ls(
            ["-l", "-a", "-h"]
        )

        self.assertTrue(result)
        self.assertIn(".hidden.txt", output)
        self.assertIn("root", output)

    def test_relative_path(self):
        """Проверить относительный путь."""
        result, output = self.run_ls(["docs"])

        self.assertTrue(result)
        self.assertIn("info.txt", output)

    def test_absolute_path(self):
        """Проверить абсолютный путь."""
        result, output = self.run_ls(["/docs"])

        self.assertTrue(result)
        self.assertIn("info.txt", output)

    def test_complex_path(self):
        """Проверить путь с точками."""
        result, output = self.run_ls(
            ["/docs/.././docs"]
        )

        self.assertTrue(result)
        self.assertIn("info.txt", output)

    def test_unknown_option(self):
        """Проверить неизвестный ключ."""
        result, output = self.run_ls(["-x"])

        self.assertFalse(result)
        self.assertIn("неизвестный ключ", output)

    def test_too_many_paths(self):
        """Проверить несколько путей."""
        result, output = self.run_ls(
            ["docs", "/docs"]
        )

        self.assertFalse(result)
        self.assertIn(
            "не более одного пути",
            output
        )


if __name__ == "__main__":
    unittest.main()