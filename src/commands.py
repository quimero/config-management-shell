"""Команды эмулятора командной оболочки."""

from src.path_utils import get_node
from src.path_utils import resolve_path
from datetime import datetime

LS_OPTIONS = {"l", "h", "a"}
CHOWN_ARGUMENTS = 2

def command_cd(vfs, current_path, arguments):
    """Изменить текущий каталог VFS."""
    if len(arguments) != 1:
        print("Ошибка: команда cd ожидает один аргумент")
        return False

    try:
        path_parts, node = resolve_path(
            vfs,
            arguments[0],
            current_path
        )
    except FileNotFoundError:
        print("Ошибка: каталог не найден")
        return False
    except NotADirectoryError:
        print("Ошибка: часть пути не является каталогом")
        return False

    if node["type"] != "dir":
        print("Ошибка: указанный путь не является каталогом")
        return False

    current_path[:] = path_parts
    return True


def parse_ls_arguments(arguments):
    """Разобрать ключи и путь команды ls."""
    options = set()
    paths = []

    for argument in arguments:
        if argument.startswith("-") and argument != "-":
            for option in argument[1:]:
                if option not in LS_OPTIONS:
                    raise ValueError(
                        f"неизвестный ключ: -{option}"
                    )
                options.add(option)
        else:
            paths.append(argument)

    if len(paths) > 1:
        raise ValueError(
            "команда ls принимает не более одного пути"
        )

    path = paths[0] if paths else "."
    return options, path


def human_size(size):
    """Преобразовать размер файла в удобный вид."""
    units = ("B", "K", "M", "G")
    value = float(size)
    index = 0

    while value >= 1024 and index < len(units) - 1:
        value /= 1024
        index += 1

    if index == 0:
        return f"{int(value)}B"

    return f"{value:.1f}{units[index]}"


def node_size(node):
    """Получить размер объекта VFS."""
    if node["type"] == "file":
        return len(node["content"])

    return 0


def format_long_entry(name, node, human):
    """Сформировать строку для ls -l."""
    object_type = "d" if node["type"] == "dir" else "-"
    owner = node.get("owner", "root")
    size = node_size(node)

    if human:
        size_text = human_size(size)
    else:
        size_text = str(size)

    return f"{object_type} {owner} {size_text:>6} {name}"


def directory_entries(vfs, node, path_parts, show_all):
    """Получить элементы каталога для вывода."""
    entries = list(node["children"].items())

    if not show_all:
        return [
            item for item in entries
            if not item[0].startswith(".")
        ]

    parent = get_node(vfs, path_parts[:-1])
    special = [
        (".", node),
        ("..", parent)
    ]
    return special + entries


def print_entry(name, node, options):
    """Вывести один элемент VFS."""
    if "l" in options:
        text = format_long_entry(
            name,
            node,
            "h" in options
        )
        print(text)
        return

    print(name)


def command_ls(vfs, current_path, arguments):
    """Вывести содержимое каталога VFS."""
    try:
        options, path = parse_ls_arguments(arguments)
    except ValueError as error:
        print(f"Ошибка: {error}")
        return False

    try:
        path_parts, node = resolve_path(
            vfs,
            path,
            current_path
        )
    except FileNotFoundError:
        print("Ошибка: путь не найден")
        return False
    except NotADirectoryError:
        print("Ошибка: часть пути не является каталогом")
        return False

    if node["type"] == "file":
        name = path_parts[-1]
        print_entry(name, node, options)
        return True

    entries = directory_entries(
        vfs,
        node,
        path_parts,
        "a" in options
    )

    for name, child in entries:
        print_entry(name, child, options)

    return True

def command_date(arguments):
    """Вывести текущие дату и время."""
    if arguments:
        print("Ошибка: команда date не принимает аргументы")
        return False

    now = datetime.now().astimezone()
    print(now.strftime("%Y-%m-%d %H:%M:%S %Z"))
    return True


def command_clear(arguments):
    """Очистить экран терминала."""
    if arguments:
        print("Ошибка: команда clear не принимает аргументы")
        return False

    print("\033[2J\033[H", end="")
    return True

def command_chown(vfs, current_path, arguments):
    """Изменить владельца объекта VFS."""
    if len(arguments) != CHOWN_ARGUMENTS:
        print(
            "Ошибка: команда chown ожидает "
            "владельца и путь"
        )
        return False

    owner = arguments[0]
    path = arguments[1]

    try:
        _, node = resolve_path(
            vfs,
            path,
            current_path
        )
    except FileNotFoundError:
        print("Ошибка: путь не найден")
        return False
    except NotADirectoryError:
        print("Ошибка: часть пути не является каталогом")
        return False

    node["owner"] = owner
    return True