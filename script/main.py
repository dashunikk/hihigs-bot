from script.classes import VMConnect

def main():
    try:
        # Создаём подключение к VM (адрес нужно заменить на реальный)
        vm = VMConnect(address="130.193.40.163")

        # Проверяем подключение (используется __bool__)
        if not vm:
            print("Ошибка: Не удалось подключиться к VM!")
            return

        # Пример выполнения команды ls (сохраняется в БД через метод ls())
        print("Результат 'ls':", vm.ls())

        # Пример вызова команды через __call__ (сохраняется в БД)
        print("Результат 'pwd':", vm("pwd"))

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
    finally:
        # Закрываем соединение с VM (используется __exit__)
        if 'vm' in locals():
            vm.client.close()
            vm.db_conn.close()

if __name__ == "__main__":
    main()