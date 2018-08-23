import os
import unittest
from fileexplorer import FileExplorer


SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
TESTDATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'testdata'))
DATA_01_LOG = os.path.join(TESTDATA_DIR, 'data_01.log')
ENCODING = 'utf-8'

class TestFileExplorer(unittest.TestCase):

    def setUp(self):
        self.fe = FileExplorer(open, DATA_01_LOG, 'rb')

    def tearDown(self):
        self.fe.close()

    def test_cur_line_index_iterates_from_0(self):
        ''' cur_line_index итерируется правильно '''
        index = 0
        for l in self.fe:
            index += 1
            self.assertEqual(self.fe.cur_line_index, index)
    
    def test_read_1_line_return_one_line(self):
        ''' чтение одной строки'''
        line = self.fe.read()
        self.assertEqual(line.rstrip().decode(ENCODING), '20:10:29.085040 185130259 dqhl gzytdvpprvflrivlle h    i')
        self.assertEqual(self.fe.cur_line_index, 1, '')


    def test_read_n_lines(self):
        ''' read возвращает указанное количество строк. ''' 
        lines_to_read = 5
        lines = self.fe.read(lines_to_read)
        self.assertEqual(len(lines), lines_to_read, )
        self.assertEqual(lines[0].rstrip().decode(ENCODING), '20:10:29.085040 185130259 dqhl gzytdvpprvflrivlle h    i', 'Первая прочитанная строка не равна строке из файла')
        self.assertEqual(lines[lines_to_read - 1].rstrip().decode(ENCODING), '20:10:29.085040 258262132 vzkpk ivvdtpsxlcffehbibvgmjkvq', '{0} строка не равна строке из файла'.format(lines_to_read))
        self.assertEqual(self.fe.cur_line_index, lines_to_read, '')

    def test_seek_line_return_correct_line(self):
        ''' seek - должен переходить к указанной строке в файле '''
        line_to_seek = 21
        self.fe.seek(line_to_seek)
        self.assertEqual(self.fe.cur_line_index, 21, 'cur_line_index неправильный')
    
    def test_seek_return_to_previous_line(self):
        ''' возвращение на уже прочитанную линию '''
        lines_to_read = 5
        seak_line = 2
        self.fe.read(lines_to_read)
        self.fe.seek(seak_line)
        self.assertEqual(self.fe.cur_line_index, seak_line, 'курсор не встал на линию {0}'.format(seak_line))
        self.assertEqual(self.fe.read().rstrip().decode(ENCODING), '20:10:29.085040 987719878  p tiwj   puca yhl kt gqqeihc', 'читается неправильная строка')

    def test_read_n_lines_from_start_pos(self):
        ''' чтение указанного количества строк, начиная с указанной позиции '''
        start_pos = 12
        lines_to_read = 5
        lines = self.fe.read(lines_to_read, start_pos)
        self.assertEqual(len(lines), lines_to_read, 'прочитаны не все строки')
        self.assertEqual(lines[0].rstrip().decode(ENCODING), '20:10:29.086017 392548458 hcwxu rr doiu mofiansylomvsfi', 'Первая прочитанная строка не равна строке из файла')
        self.assertEqual(lines[lines_to_read - 1].rstrip().decode(ENCODING), '20:10:29.086017 858173529 r evgcpe cepkzed daz fddjdecmu', '{0} строка не равна строке из файла'.format(start_pos + lines_to_read))
        self.assertEqual(self.fe.cur_line_index, start_pos + lines_to_read, 'после чтения курсор не на той позиции')


if __name__ == '__main__':
    unittest.main()
