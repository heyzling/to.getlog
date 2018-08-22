# -*- coding: utf-8 -*-
from sftp import Sftp, AuthData

def print_200_lines_of(server, port, log_file_mask, line_id):
    ''' Метод для поиска в логе на удаленном сервере строки с заданным числовым идентификатором. Возвращает массив строк -100 + 100 от идентификатора
        server - имя или IP сервера где лежит лог
        log_file_mask - маска пути к лог файлу. Допустимо содержания wildcards. (* - любое количество символов)
        line-id - уникальный ID для строки в файле, по которому будет производится поиск
    '''
    # все в одном методе, чтобы точнее понять пути обобщения
    # ssh = None
    # sftp = None
    # try:
    #     ssh = ssh_connect(server, port)
    #     sftp = ssh.open_sftp()
    #     files = sftp_search(sftp, log_file_mask)
    #     for file in files:
    #         print('open: {0}'.format(file))
    #         with sftp.open(file, 'r') as f:
    #             for line in f:
    #                 print(line)
    # finally:
    #     sftp.close()
    #     ssh.close()
    pass


if __name__ == '__main__':
    # print_200_lines_of('192.168.1.5', 2222, '/var/log/techops/data*.log', 4)
    pass
