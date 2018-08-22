# -*- coding: utf-8 -*-

import os
import unittest
from sftp import Sftp, AuthData

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
TESTDATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'testdata'))
REMOTE_TESTDATA_DIR = '/var/log/techops'

def connect_test_sftp():
    server = '192.168.1.5'
    port = 2222
    return Sftp(server, port, AuthData.get_auth_data(server))

sftp = connect_test_sftp()

class TestSftp(unittest.TestCase):

    def test_walk_found_all_dirs_and_files(self):
        ''' Тест проверяет, что sftp.walk итерируется по всем папкам внутир указанной папки '''
        found_files = []
        found_folders = []
        for root, folders, files in sftp.walk(REMOTE_TESTDATA_DIR):
            found_folders += folders
            found_files += files
        self.assertEqual(len(found_files), 12, 'Не все файлы найдены')
        self.assertEqual(len(found_folders), 2, 'Не все папки найдены')       

    def test_walk_return_full_pathes(self):
        ''' метод должен возвращать полные пути ко всем сущностям '''

        for root, folders, files in sftp.walk(REMOTE_TESTDATA_DIR):
            self.assertTrue(
                all([root in folder for folder in folders ]), 'не все пути папок полные: {0}'.format(folders)
                )
            self.assertTrue(
                all([root in file for file in files]), 'Не все пути файлов полные: {0}'.format(files)
            )
            
    def test_search_find_all_logs(self):
        ''' найти все файлы логов по маске *.log '''
        logs = sftp.search(REMOTE_TESTDATA_DIR, '*.log')
        self.assertEqual(len(logs), 12, 'не все логи найдены {0}'.format(logs))

    def test_search_find_all_logs_in_logs_folders_with_3_in_name(self):
        ''' найти все логи в папках logs_n, которые содержат в имени цифру 3 '''
        logs = sftp.search(REMOTE_TESTDATA_DIR, '*/logs_*/*3*')
        self.assertEqual(len(logs), 3, 'не все логи в папках logs_n найдены {0}'.format(logs))

if __name__ == '__main__':
    # TestSftp().test_walk_found_all_dirs_and_files()
    # TestSftp().test_walk_return_full_pathes()
    TestSftp().test_search_find_all_logs()
    TestSftp().test_search_find_all_logs_in_logs_folders_with_3_in_name()
    # unittest.main()
