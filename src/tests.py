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

class TestSuite(unittest.TestCase):

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
            

if __name__ == '__main__':
    TestSuite().test_walk_found_all_dirs_and_files()
    TestSuite().test_walk_return_full_pathes()
    # unittest.main()
