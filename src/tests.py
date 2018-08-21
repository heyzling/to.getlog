# -*- coding: utf-8 -*-
# import parser
import loggetter
import os

class TestSuite():

    def test_sft_search_file(self):
        files = loggetter.sftp_search(os, 'c:/Users/MurMi/git*')
        print(files)

if __name__ == '__main__':
    TestSuite().test_sft_search_file()