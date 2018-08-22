# -*- coding: utf-8 -*-
# import parser
from loggetter import AuthData, Sftp
import unittest
import os

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
TESTDATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'testdata'))
REMOTE_TESTDATA_DIR = '/var/log/techops'


def connect_test_sftp():
    server = '192.168.1.5'
    port = 2222
    return Sftp(server, port, AuthData(server))

sftp = connect_test_sftp()

class TestSuite(unittest.TestCase):

    def test_sftp_walk_found_all_dirs_and_files(self):
        found_files = []
        found_folders = []
        for path, folders, files in sftp.walk(REMOTE_TESTDATA_DIR):
            found_folders += folders
            found_files += files
        self.assertEqual(len(found_files), 8, 'Не все файлы найдены')
        self.assertEqual(len(found_folders), 0, 'Не все папки найдены')       

if __name__ == '__main__':
    # TestSuite().test_sft_search_file_only_last_file_mask()
    TestSuite().test_sftp_walk_found_all_dirs_and_files()
