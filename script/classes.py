__all__ = ['VMConnect']

from paramiko import SSHClient, AutoAddPolicy
from script.db import get_db_connection, save_command, init_db

class VMConnect:
    def __init__(self, address=None, username=None, password=None):
        self.address = address
        self.username = username
        self.password = password
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())  # Автодобавление ключа хоста
        self.db_conn = get_db_connection()
        init_db()

    def connect(self):
        """Подключается к VM с указанными данными."""
        try:
            self.client.connect(
                hostname=self.address,
                username=self.username,
                password=self.password,
                timeout=5
            )
            save_command(self.db_conn, 'connect', f"Успешное подключение к {self.address}")
            return True
        except Exception as e:
            save_command(self.db_conn, 'connect', f"Ошибка подключения: {str(e)}")
            return False

    def check(self):
        """Проверяет, активно ли подключение."""
        try:
            transport = self.client.get_transport()
            return transport and transport.is_active()
        except Exception as e:
            save_command(self.db_conn, 'check', f"Ошибка проверки: {str(e)}")
            return False

    def ls(self):
        """Выводит содержимое домашней директории."""
        try:
            stdin, stdout, stderr = self.client.exec_command('ls -l ~')
            output = stdout.read().decode()
            save_command(self.db_conn, 'ls', output)
            return output
        except Exception as e:
            save_command(self.db_conn, 'ls', f"Ошибка выполнения ls: {str(e)}")
            return f"Ошибка: {str(e)}"

    def __str__(self):
        return f"VMConnect[address={self.address}, user={self.username}]"

    def __bool__(self):
        return self.check()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
        self.db_conn.close()