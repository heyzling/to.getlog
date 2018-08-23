# -*- coding: utf-8 -*-
import sys
from argparse import ArgumentParser
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
    argparser = ArgumentParser(description="Find line in remote log and print 100 lines up and down around it")
    argparser.add_argument('-s', '--server', help='Server to connect', required=True)
    argparser.add_argument('-p', '--port', help='Port for server to connect', default=22, type=int)
    argparser.add_argument('-u', '--user', help='User for server connection')
    argparser.add_argument('--pass', help='Password for server connection')
    argparser.add_argument('-d', '--dir', help='Directory storing logs you wish to explore', required=True)
    argparser.add_argument('-m', '--mask', help="Unix-style wildcards for searching logs. Example = '*.log'", required=True)
    argparser.add_argument('-i', '--id', help='Id-string you wish to search', required=True)

    args = argparser.parse_args()

    if not args.user:
        args.auth = AuthData.get_auth_data(args.server)
        args.user = args.auth.user # только для красоты вывода аргументов
        args.password = args.auth.password
    else:
        args.auth = AuthData(args.user, args.password)

    trace('App started with args: {0}'.format(str(args)))
    print_200_lines_of_log(args.server, args.port, args.auth, args.dir, args.mask, args.id)
