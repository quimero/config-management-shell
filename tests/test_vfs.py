"""Автоматические тесты виртуальной файловой системы."""

import tempfile
import unittest
from pathlib import Path

from src.vfs import load_vfs


VFS_DIR = Path(__file__).resolve().parent / "vfs"


class TestVFS(unittest.TestCase):

    def test_minimal(self):
        """Проверить минимальную VFS."""
        vfs = load_vfs(VFS_DIR / "minimal")
        file = vfs["children"]["hello.txt"]

        self.assertEqual(file["type"], "file")
        self.assertEqual(
            file["content"].decode("utf-8").strip(),
            "Hello from VFS!"
        )

    def test_multiple(self):
        """Проверить VFS с несколькими файлами."""
        vfs = load_vfs(VFS_DIR / "multiple")
        children = vfs["children"]

        self.assertEqual(
            set(children),
            {"readme.txt", "config.ini", "docs"}
        )
        self.assertEqual(children["docs"]["type"], "dir")
        self.assertIn("info.txt", children["docs"]["children"])

    def test_nested(self):
        """Проверить три уровня вложенности."""
        vfs = load_vfs(VFS_DIR / "nested")
        node = vfs

        for folder in ("level1", "level2", "level3"):
            node = node["children"][folder]

        content = node["children"]["deep.txt"]["content"]
        self.assertEqual(
            content.decode("utf-8").strip(),
            "Level 3 reached!"
        )

    def test_missing_directory(self):
        """Проверить ошибку отсутствующей папки."""
        with tempfile.TemporaryDirectory() as temp:
            missing = Path(temp) / "missing"

            with self.assertRaises(FileNotFoundError):
                load_vfs(missing)

    def test_file_instead_of_directory(self):
        """Проверить передачу файла вместо папки."""
        path = VFS_DIR / "minimal" / "hello.txt"

        with self.assertRaises(ValueError):
            load_vfs(path)

    def test_binary_file(self):
        """Проверить чтение двоичных данных."""
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "image.bin"
            data = bytes([0, 128, 255])
            path.write_bytes(data)

            vfs = load_vfs(temp)
            content = vfs["children"]["image.bin"]["content"]

            self.assertEqual(content, data)

    def test_changes_stay_in_memory(self):
        """Изменения VFS не должны изменять файл на диске."""
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample.txt"
            path.write_bytes(b"before")

            vfs = load_vfs(temp)
            vfs["children"]["sample.txt"]["content"] = b"after"

            self.assertEqual(path.read_bytes(), b"before")

    def test_loaded_data_is_snapshot(self):
        """Загруженные данные не зависят от исходного файла."""
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample.txt"
            path.write_bytes(b"before")

            vfs = load_vfs(temp)
            path.write_bytes(b"after")

            content = vfs["children"]["sample.txt"]["content"]
            self.assertEqual(content, b"before")


if __name__ == "__main__":
    unittest.main()
