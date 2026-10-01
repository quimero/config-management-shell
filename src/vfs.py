"""Загрузка виртуальной файловой системы в память."""

from pathlib import Path


def read_folder(folder):
    """Прочитать папку и её содержимое."""
    node = {"type": "dir", "owner": "root", "children": {}}

    for item in sorted(folder.iterdir()):
        if item.is_symlink():
            raise ValueError(f"Ссылки не поддерживаются: {item}")

        if item.is_dir():
            node["children"][item.name] = read_folder(item)
        elif item.is_file():
            node["children"][item.name] = {
                "type": "file",
                "owner": "root",
                "content": item.read_bytes(),
            }
        else:
            raise ValueError(f"Неизвестный тип объекта: {item}")

    return node


def load_vfs(path):
    """Загрузить VFS из указанной папки."""
    folder = Path(path)

    if not folder.exists():
        raise FileNotFoundError(
            f"Папка VFS не найдена: {folder}"
        )

    if not folder.is_dir():
        raise ValueError(f"VFS должна быть папкой: {folder}")

    return read_folder(folder)
