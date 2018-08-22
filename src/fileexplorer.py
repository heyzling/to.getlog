
class FileExplorer():
    ''' Расширение чтения файлов. '''

    # TODO: собственный file-like object который может оборачиваться вокруг существующего и 
    # и предоставлять расширенный функционал, вроде кеширвоания оффсетов строк, чтения строки по номер и т.д.
    # доп. преимущество - использование with в клиентском коде

    def __init__(self, file_object_open_method, file_path, open_mode, encoding):
        ''' 
        file_object_open_method - метод, который создает file-like объект
        file_path - путь к файлу
        open_mode - метод открытия (r, w, rb, a и так далее)
        encoding - кодировка файла '''
        self._file_open_method = file_object_open_method
        self._open_mode = open_mode
        self.file_path = file_path
        self.encoding = encoding
        self._file = self._file_open_method(self.file_path, self._open_mode)
        self._line_offsets = []
        self._current_offset = 0

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self._file.close()

    @property
    def current_line(self):
        ''' номер строки на которой стоит курсор '''
        return len(self._line_offsets)

    @property
    def current_offset(self):
        ''' текущий оффсет курсора, на котором проихсодит чтение '''
        return self._current_offset

    def seek(self, string):
        ''' Поиск вхождения указанной строки в файле и остановка курсора на линии с ней.
        returns boolean - найдено ли вхождение или нет  '''
        bstring = string.encode(self.encoding)
        for l in self.read():
            if bstring in l:
                return True
        return False

    def read(self):
        ''' построчно читает файл, возвращает содержание строки '''
        for i, line in enumerate(self._file, self.current_line):
            self._line_offsets.append(self._current_offset)
            self._current_offset += len(line)
            yield line

# import os
# import sftp
# import tools

# SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
# TESTDATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'testdata'))
# DATA_01_LOG = os.path.join(TESTDATA_DIR, 'data_01.log')
# REMOTE_TESTDATA_DIR = '/var/log/techops'
# REMOTE_DATA_01_LOG = tools.join_unix(REMOTE_TESTDATA_DIR, 'data_01.log')

# def connect_test_sftp():
#     server = '192.168.1.5'
#     port = 2222
#     return sftp.Sftp(server, port, sftp.AuthData.get_auth_data(server))

# sftp = connect_test_sftp()

# # file = open(DATA_01_LOG, 'rb')
# # with open(DATA_01_LOG, 'rb') as file:
# # with FileExplorer(sftp.open, REMOTE_DATA_01_LOG, 'rb', 'utf-8') as f:
# with FileExplorer(open, DATA_01_LOG, 'rb', 'utf-8') as f:
#     # fe = FileExplorer(file, 'utf-8')
#     for l in f.read():
#         print('{0} -> {1}'.format(f.current_line, l))

#     print(' ----------------- end RREAD -------')
#     for l in f.read():
#         print('{0} -> {1}'.format(f.current_line, l))