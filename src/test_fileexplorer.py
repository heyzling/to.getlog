import os
import unittest
from fileexplorer import FileExplorer


SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
TESTDATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'testdata'))
DATA_01_LOG = os.path.join(TESTDATA_DIR, 'data_01.log')


class TestFileExplorer(unittest.TestCase):

    def setUp(self):
        self.fe = FileExplorer(open, DATA_01_LOG, 'rb', 'utf-8')

    def tearDown(self):
        self.fe.close()

    def test_seek_save_line_index(self):
        ''' seek - находит указанное вхождение в файле '''
        id_to_find = '774038205'
        is_found = self.fe.seek(id_to_find)
        self.assertTrue(is_found, 'строка с ID={0} не найдена'.format(id_to_find))

    def test_current_line_is_correcto_after_succsessfull_seek(self):
        ''' Свойство current_line содержит правильный номер строки, после того, как успешно был выполнен seek '''
        id_to_find = '774038205'
        is_found = self.fe.seek(id_to_find)
        self.assertTrue(is_found, 'строка с ID={0} не найдена'.format(id_to_find))
        self.assertEqual(self.fe.current_line, 77, 'Строка с ID={0} найдено, но свойство current_line содержит неверный номер строки'.format(id_to_find))

if __name__ == '__main__':
    unittest.main()