import paramiko

LOGS_DIR = '/var/logs/techops'

class AuthData():
    
    def __init__(self, server):
        print('Request authentication for: {0}'.format(server))
        if server == '192.168.1.5':
            self.user = 'havok'
            self.password = 'bb5506451955'
        else:
            raise Exception('No auth data for server: {0}'.format(server))

def print_200_lines_of(server, log_file_mask, line_id):
    ''' Метод для поиска в логе на удаленном сервере строки с заданным числовым идентификатором. Возвращает массив строк -100 + 100 от идентификатора
        server - имя или IP сервера где лежит лог
        log_file_mask - маска пути к лог файлу. Допустимо содержания wildcards. (* - любое количество символов)
        line-id - уникальный ID для строки в файле, по которому будет производится поиск
    '''
    # все в одном методе, чтобы точнее понять пути обобщения
    print('Request authentication for: {0}'.format(server))
    auth_data = AuthData(server)
    ssh = paramiko.client.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, 2222, auth_data.user, auth_data.password)
    sftp = ssh.open_sftp()
    # logfile = [ log for log in sftp.listdir(LOGS_DIR) if log.contains('data')][0]
    for line in sftp.listdir('/var/log/techops'):
        print(line)
    log_file = sftp.open('/var/log/techops/data_01.log')
    try:
        for line in log_file:
            print(line)
    finally:
        log_file.close()

    sftp.close()
    ssh.close


if __name__ == '__main__':
    print_200_lines_of('192.168.1.5', 'data*.log', 4)

