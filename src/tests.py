# -*- coding: utf-8 -*-
# import parser
import loggetter
import unittest
import os

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
TESTDATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'testdata'))

class TestSuite(unittest.TestCase):

    def test_sft_search_file_only_last_file_mask(self):
        search_mask = os.path.join(TESTDATA_DIR, 'logs_1', '*.log')
        files = loggetter.sftp_search(os, search_mask)
        self.assertEqual(len(files), 3, 'поиск не нашел все файлы логов')

if __name__ == '__main__':
    TestSuite().test_sft_search_file_only_last_file_mask()