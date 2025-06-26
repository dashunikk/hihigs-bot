__all__ = ['VMConnect']

from paramiko import SSHClient, AutoAddPolicy

class VMConnect:
    def __init__(self, address=None, username=None, password=None):
        self.address = address
        self.username = username
        self.password = password
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.connected = False

    def connect(self):
        """Подключается к VM"""
        try:
            self.client.connect(
                hostname=self.address,
                username=self.username,
                password=self.password,
                timeout=5
            )
            self.connected = True
            return True
        except Exception as e:
            return False

    def check_connection(self):
        """Проверяет подключение"""
        return self.connected

    def list_files(self):
        """Список файлов в домашней директории"""
        if not self.connected:
            return "Нет подключения"
        stdin, stdout, stderr = self.client.exec_command('ls ~')
        return stdout.read().decode()

    def read_file(self, filename):
        """Читает содержимое файла"""
        if not self.connected:
            return "Нет подключения"
        stdin, stdout, stderr = self.client.exec_command(f'cat ~/{filename}')
        return stdout.read().decode()

    def __str__(self):
        return f"Подключение к {self.address} как {self.username}"

    def __bool__(self):
        return self.connected

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()