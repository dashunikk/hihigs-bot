__all__ = ['VMConnect']

from paramiko import SSHClient

class VMConnect:
    def __init__(self, adress):
        self.adress = adress
        self.client = SSHClient()
    def check(self):
        self.client.connect(self.adress)
        #TODO - описать вывод из данного метода (хендлеры паф чек и лс)
    def ls(self):
        stdin, stdout, stderr = self.client.exec_command('ls -l')
        return stdout