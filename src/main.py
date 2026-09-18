VFS_NAME = "my_vfs"


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


def main():
    while True:
        user_input = input(f"{VFS_NAME}:~$ ")

        command, arguments = parse_command(user_input)

        if not command:
            continue

        result = execute_command(command, arguments)

        if result is None:
            break


if __name__ == "__main__":
    main()