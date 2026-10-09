import argparse
from pathlib import Path
from src.vfs import load_vfs


VFS_NAME = "my_vfs"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Shell emulator"
    )
    parser.add_argument("--vfs", help="Path to VFS")
    parser.add_argument("--script", help="Path to startup script")
    return parser.parse_args()


def parse_command(user_input):
    parts = user_input.split()

    if not parts:
        return "", []

    command = parts[0]
    arguments = parts[1:]
    return command, arguments


def execute_command(command, arguments):
    if command == "ls":
        print("ls", arguments)
        return True

    if command == "cd":
        if len(arguments) != 1:
            print("Ошибка: команда cd ожидает один аргумент")
            return False

        print("cd", arguments)
        return True

    if command == "exit":
        if arguments:
            print("Ошибка: команда exit не принимает аргументы")
            return False

        return None

    print(f"Ошибка: неизвестная команда: {command}")
    return False


def run_script(path):
    """Выполнить команды из стартового скрипта."""
    try:
        with open(path, encoding="utf-8") as script:
            for line_number, raw_line in enumerate(script, 1):
                line = raw_line.strip()

                if not line or line.startswith("#"):
                    continue

                print(f"{VFS_NAME}:~$ {line}")

                command, arguments = parse_command(line)
                result = execute_command(command, arguments)

                if result is False:
                    print(f"Ошибка в скрипте, строка {line_number}")
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

    print(f"Элементов в корне VFS: {len(vfs['children'])}")
    return vfs


def handle_startup_script(script_path):
    """Проверить и выполнить стартовый скрипт."""
    if script_path is None:
        return None

    if not Path(script_path).is_file():
        print(f"Ошибка: скрипт не найден: {script_path}")
        return 1

    result = run_script(script_path)

    if result is False:
        return 1

    if result is None:
        return 0

    return None


def run_repl():
    """Запустить интерактивный режим."""
    while True:
        user_input = input(f"{VFS_NAME}:~$ ")
        command, arguments = parse_command(user_input)

        if not command:
            continue

        result = execute_command(command, arguments)

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

    script_result = handle_startup_script(args.script)

    if script_result is not None:
        return script_result

    run_repl()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
