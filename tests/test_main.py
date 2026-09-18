import unittest

from src.main import parse_command


class TestParseCommand(unittest.TestCase):

    def test_command_without_arguments(self):
        command, arguments = parse_command("ls")

        self.assertEqual(command, "ls")
        self.assertEqual(arguments, [])

    def test_command_with_argument(self):
        command, arguments = parse_command("cd documents")

        self.assertEqual(command, "cd")
        self.assertEqual(arguments, ["documents"])

    def test_command_with_several_arguments(self):
        command, arguments = parse_command("cd one two")

        self.assertEqual(command, "cd")
        self.assertEqual(arguments, ["one", "two"])

    def test_empty_input(self):
        command, arguments = parse_command("")

        self.assertEqual(command, "")
        self.assertEqual(arguments, [])


if __name__ == "__main__":
    unittest.main()