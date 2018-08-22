# -*- coding: utf-8 -*-
from sftp import Sftp, AuthData

def print_200_lines_of(server, port, logs_dir, log_file_mask, line_id):
    ''' Метод для поиска в логе на удаленном сервере строки с заданным числовым идентификатором. Возвращает массив строк -100 + 100 от идентификатора
        server - имя или IP сервера где лежит лог
        logs_dir - папка, где лежат логи
        log_file_mask - маска путей к лог файлу на основе Unix-wildcards.
        line-id - уникальный ID для строки в файле, по которому будет производится поиск
    '''
    sftp = Sftp(server, port, AuthData.get_auth_data(server))
    for log in sftp.search(logs_dir, log_file_mask):
        print('open: {0}'.format(log))
        with sftp.open(log, 'r') as f:
            for line in f:
                print(line)

if __name__ == '__main__':
    print_200_lines_of('192.168.1.5', 2222, '/var/log/techops/', '*data_34.log', 4)
    pass
