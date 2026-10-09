"""Тесты команд date и clear."""

import io
import unittest
from contextlib import redirect_stdout

from src.commands import command_clear
from src.commands import command_date


class TestBasicCommands(unittest.TestCase):
    """Проверить команды date и clear."""

    def capture(self, function, arguments):
        """Получить результат и текст команды."""
        output = io.StringIO()

        with redirect_stdout(output):
            result = function(arguments)

        return result, output.getvalue()

    def test_date(self):
        """Проверить вывод даты."""
        result, output = self.capture(
            command_date,
            []
        )

        self.assertTrue(result)
        self.assertRegex(
            output,
            r"\d{4}-\d{2}-\d{2} "
            r"\d{2}:\d{2}:\d{2}"
        )

    def test_date_arguments(self):
        """Проверить лишние аргументы date."""
        result, output = self.capture(
            command_date,
            ["test"]
        )

        self.assertFalse(result)
        self.assertIn(
            "не принимает аргументы",
            output
        )

    def test_clear(self):
        """Проверить очистку экрана."""
        result, output = self.capture(
            command_clear,
            []
        )

        self.assertTrue(result)
        self.assertEqual(
            output,
            "\033[2J\033[H"
        )

    def test_clear_arguments(self):
        """Проверить лишние аргументы clear."""
        result, output = self.capture(
            command_clear,
            ["test"]
        )

        self.assertFalse(result)
        self.assertIn(
            "не принимает аргументы",
            output
        )


if __name__ == "__main__":
    unittest.main()