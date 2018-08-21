# -*- coding: utf-8 -*-
import paramiko
import fnmatch
import os
LOGS_DIR = '/var/logs/techops'

class AuthData():
    
    def __init__(self, server):
        print('Request authentication for: {0}'.format(server))
        if server == '192.168.1.5':
            self.user = 'havok'
            self.password = 'bb5506451955'
        else:
            raise Exception('No auth data for server: {0}'.format(server))

def ssh_connect(server, port):
    auth_data = AuthData(server)

    ssh = paramiko.client.SSHClient()
    ssh = paramiko.client.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, 2222, auth_data.user, auth_data.password)

    return ssh

def sftp_search(sftp, log_file_mask):
    ''' Поиск файлов по принятым в Unix системах wildcard '''
    files_dir = os.path.dirname(log_file_mask)
    file_mask = os.path.split(log_file_mask)[-1]
    files = sftp.listdir(files_dir)
    # replace - из-за того, что разработка ведется на windows машине, и join вставляет обратные слеши, которые Unix не любит
    log_files = [ os.path.join(files_dir, file).replace('\\', '/') for file in fnmatch.filter(files, file_mask)]
    return log_files

def print_200_lines_of(server, port, log_file_mask, line_id):
    ''' Метод для поиска в логе на удаленном сервере строки с заданным числовым идентификатором. Возвращает массив строк -100 + 100 от идентификатора
        server - имя или IP сервера где лежит лог
        log_file_mask - маска пути к лог файлу. Допустимо содержания wildcards. (* - любое количество символов)
        line-id - уникальный ID для строки в файле, по которому будет производится поиск
    '''
    # все в одном методе, чтобы точнее понять пути обобщения
    ssh = None
    sftp = None
    try:
        ssh = ssh_connect(server, port)
        sftp = ssh.open_sftp()
        files = sftp_search(sftp, log_file_mask)
        for file in files:
            print('open: {0}'.format(file))
            with sftp.open(file, 'r') as f:
                for line in f:
                    print(line)
    finally:
        sftp.close()
        ssh.close()


if __name__ == '__main__':
    print_200_lines_of('192.168.1.5', 2222, '/var/log/techops/data*.log', 4)

