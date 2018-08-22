# -*- coding: utf-8 -*-

import os
import fnmatch
import atexit
import paramiko
from stat import S_ISDIR

class AuthData():
    ''' Содержит параметры аутентификации '''

    def __init__(self, user, password):
        self.user = user
        self.password = password

    @classmethod
    def get_auth_data(cls, server):
        ''' Получить данные аутентификации для конкретного сервера '''

        print('Request authentication for: {0}'.format(server))
        if server == '192.168.1.5':
            user = 'havok'
            password = 'bb5506451955'
            return cls(user, password)
        else:
            raise Exception('No auth data for server: {0}'.format(server))


class Sftp(paramiko.sftp_client.SFTPClient):
    ''' кастомный класс-расширение класса paramiko.sftp_client.SFTPClient. 
    Инкапсулирует ssh соединение для удобства клиентского кода.
    Имеет несколько дополнительных методов для работы с удаленной файловой системой. '''

    def __init__(self, server, port, auth):

        self._server = server
        self._port = port

        # коннект по ssh
        self._ssh = paramiko.client.SSHClient()
        self._ssh = paramiko.client.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh.connect(self._server, self._port, auth.user, auth.password)

        # коннект по sftp - инициализация родительского класса
        # то как инициализируется SFTPClient найдено в исходниках Paramiko
        # https://github.com/paramiko/paramiko/blob/master/paramiko/sftp_client.py#L141
        chan = self._ssh._transport.open_session()
        if chan is None:
            raise Exception('failed instantiating sftp connection to {0}'.format(server))
        chan.invoke_subsystem("sftp")
        super().__init__(chan)

        atexit.register(self.close)

    def walk(self, root):
        ''' Упрощенный аналог os.walk. 
        Для каждой итерации возвращает кортеж - (root, folders, files)
        Для всех folders, files возвращает полные пути на базе root '''

        files=[]
        folders=[]

        for f in self.listdir_attr(root):
            if S_ISDIR(f.st_mode):
                folders.append(os.path.join(root, f.filename))
            else:
                files.append(os.path.join(root, f.filename))

        yield root,folders,files
        for folder in folders:
            new_root=os.path.join(root,folder).replace('\\', '/')
            for x in self.walk(new_root):
                yield x

    def search(self, base_dir, log_file_mask):
        ''' Поиск файлов по принятым в Unix системах wildcard 
        basedir - директория, в которой нужно произвести поиск файлов по маске
        log_file_mask - маска для поиска файлов в виде Unix wildcards'''

        # files_dir = os.path.dirname(log_file_mask)
        # file_mask = os.path.split(log_file_mask)[-1]
        # files = sftp.listdir(files_dir)
        # # replace - из-за того, что разработка ведется на windows машине, и join вставляет обратные слеши, которые Unix не любит
        # log_files = [ os.path.join(files_dir, file).replace('\\', '/') for file in fnmatch.filter(files, file_mask)]

        found_files = []
        for root, folders, files in self.walk(base_dir):
            found_files += fnmatch.filter(files, log_file_mask)

        return found_files

    def close(self):
        ''' Закрыть соединение '''
        print('Closing SFTP connection to {0}'.format(self._server))
        super().close()
        self._ssh.close()