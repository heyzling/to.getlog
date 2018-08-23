# -*- coding: utf-8 -*-
import sys
from tools import trace
from sftp import Sftp, AuthData
from fileexplorer import FileExplorer


def print_200_lines_of_log(server, port, auth, logs_dir, log_file_mask, line_id):
    ''' Подключается по SFTP к указанному серверу, ищет в указанной папке по указанной маске файлы
    Ищет в этих файлах первое вхождение указанного идентификатора и печатает -100 строк от него, саму строку и +100 строк от нее
        server - IP сервера где лежит лог
        port - SSH порт
        auth - user / password
        logs_dir - папка, где лежат файлы
        log_file_mask - маска путей к лог файлу на основе Unix-wildcards.
        line-id - уникальный ID для строки в файле, по которому будет производится поиск
    '''
    line_id = str(line_id)

    trace('Connect to {0}:{1}'.format(server, port))
    with Sftp(server, port, auth) as sftp:

        trace("Search for logs in '{0}' by mask '{1}'".format(logs_dir, log_file_mask))
        logs = sftp.search(logs_dir, log_file_mask)

        if len(logs) == 0:
            trace('No logs has been found.')
            return

        trace('Logs has been found: {0}'.format(len(logs)))
        for log_path in logs:
            trace('Open log: {0}'.format(log_path))
            with FileExplorer(sftp.open, log_path, 'utf-8') as log:

                if log.search_string(line_id):
                    trace("'{0}' string has been found. Print 100 line up and down of it".format(line_id))
                    trace('------- start print -------')
                    for line in log.read(201, log.cur_line_index - 101):
                        print(line)
                    trace('------- end print -------')
                    break

                else:
                    trace("No '{0}' occurrencies has been found.".format(line_id))
                

if __name__ == '__main__':
    trace('Start app')

    server = '192.168.1.5'
    port = 2222
    auth = AuthData.get_auth_data(server)
    logs_base_dir = '/var/log/techops'
    logs_search_mask = 'logs*'
    id_to_search = 411295424

    print_200_lines_of_log(server, port, auth, logs_base_dir, logs_search_mask, id_to_search)
