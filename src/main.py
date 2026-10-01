
import argparse
from pathlib import Path

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


def main():
    args = parse_args()
    print(f"VFS: {args.vfs or '(не указан)'}")
    print(f"Скрипт: {args.script or '(не указан)'}")


    if args.script is not None:
        if not Path(args.script).is_file():
            print(f"Ошибка: скрипт не найден: {args.script}")
            return 1

        result = run_script(args.script)

        if result is False:
            return 1

        if result is None:
            return 0


    while True:
        user_input = input(f"{VFS_NAME}:~$ ")
        command, arguments = parse_command(user_input)

        if not command:
            continue

        result = execute_command(command, arguments)

        if result is None:
            break

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
