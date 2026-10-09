"""Консольный эмулятор командной оболочки."""

import argparse
from pathlib import Path

from src.commands import command_cd
from src.commands import command_ls
from src.commands import command_clear
from src.commands import command_date
from src.path_utils import format_path
from src.vfs import load_vfs


VFS_NAME = "my_vfs"


def parse_args():
    """Получить параметры командной строки."""
    parser = argparse.ArgumentParser(
        description="Shell emulator"
    )
    parser.add_argument(
        "--vfs",
        help="Path to VFS"
    )
    parser.add_argument(
        "--script",
        help="Path to startup script"
    )
    return parser.parse_args()


def parse_command(user_input):
    """Разделить ввод на команду и аргументы."""
    parts = user_input.split()

    if not parts:
        return "", []

    command = parts[0]
    arguments = parts[1:]
    return command, arguments


def execute_cd(arguments, state):
    """Выполнить cd с учётом режима работы."""
    if state is not None:
        return command_cd(
            state["vfs"],
            state["cwd"],
            arguments
        )

    if len(arguments) != 1:
        print("Ошибка: команда cd ожидает один аргумент")
        return False

    print("cd", arguments)
    return True

def execute_ls(arguments, state):
    """Выполнить ls с учётом режима работы."""
    if state is not None:
        return command_ls(
            state["vfs"],
            state["cwd"],
            arguments
        )

    print("ls", arguments)
    return True

def execute_command(command, arguments, state=None):
    """Выполнить команду эмулятора."""
    if command == "ls":
        return execute_ls(arguments, state)

    if command == "cd":
        return execute_cd(arguments, state)

    if command == "date":
        return command_date(arguments)

    if command == "clear":
        return command_clear(arguments)

    if command == "exit":
        if arguments:
            print(
                "Ошибка: команда exit "
                "не принимает аргументы"
            )
            return False

        return None

    print(f"Ошибка: неизвестная команда: {command}")
    return False


def make_prompt(state):
    """Сформировать приглашение командной строки."""
    path = format_path(state["cwd"])
    return f"{VFS_NAME}:{path}$"


def run_script(path, state):
    """Выполнить команды из стартового скрипта."""
    try:
        with open(path, encoding="utf-8") as script:
            for line_number, raw_line in enumerate(script, 1):
                line = raw_line.strip()

                if not line or line.startswith("#"):
                    continue

                print(f"{make_prompt(state)} {line}")

                command, arguments = parse_command(line)
                result = execute_command(
                    command,
                    arguments,
                    state
                )

                if result is False:
                    print(
                        "Ошибка в скрипте, "
                        f"строка {line_number}"
                    )
                    return False

                if result is None:
                    return None

    except (OSError, UnicodeError) as error:
        print(f"Ошибка чтения скрипта: {error}")
        return False

    return True


def prepare_vfs(vfs_path):
    """Подготовить виртуальную файловую систему."""
    if vfs_path is None:
        vfs = {
            "type": "dir",
            "owner": "root",
            "children": {}
        }
        print("Используется пустая VFS")
    else:
        try:
            vfs = load_vfs(vfs_path)
        except (OSError, ValueError) as error:
            print(f"Ошибка загрузки VFS: {error}")
            return None

        print("VFS успешно загружена")

    count = len(vfs["children"])
    print(f"Элементов в корне VFS: {count}")
    return vfs


def handle_startup_script(script_path, state):
    """Проверить и выполнить стартовый скрипт."""
    if script_path is None:
        return None

    if not Path(script_path).is_file():
        print(
            "Ошибка: скрипт не найден: "
            f"{script_path}"
        )
        return 1

    result = run_script(script_path, state)

    if result is False:
        return 1

    if result is None:
        return 0

    return None


def run_repl(state):
    """Запустить интерактивный режим."""
    while True:
        user_input = input(f"{make_prompt(state)} ")

        command, arguments = parse_command(user_input)

        if not command:
            continue

        result = execute_command(
            command,
            arguments,
            state
        )

        if result is None:
            break


def main():
    """Запустить эмулятор."""
    args = parse_args()

    print(f"VFS: {args.vfs or '(не указан)'}")
    print(f"Скрипт: {args.script or '(не указан)'}")

    vfs = prepare_vfs(args.vfs)

    if vfs is None:
        return 1

    state = {
        "vfs": vfs,
        "cwd": []
    }

    script_result = handle_startup_script(
        args.script,
        state
    )

    if script_result is not None:
        return script_result

    run_repl(state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())