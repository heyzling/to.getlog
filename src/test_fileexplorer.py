import os
import unittest
from fileexplorer import FileExplorer


SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
TESTDATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'testdata'))
DATA_01_LOG = os.path.join(TESTDATA_DIR, 'data_01.log')
DATA_43_LOG = os.path.join(TESTDATA_DIR, 'data_43.log')
ENCODING = 'utf-8'

class TestFileExplorer(unittest.TestCase):

    def setUp(self):
        self.fe = FileExplorer(open, DATA_01_LOG)

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
        self.assertEqual(line, '20:10:29.085040 185130259 dqhl gzytdvpprvflrivlle h    i')
        self.assertEqual(self.fe.cur_line_index, 1, '')


    def test_read_n_lines(self):
        ''' read возвращает указанное количество строк. ''' 
        lines_to_read = 5
        lines = self.fe.read(lines_to_read)
        self.assertEqual(len(lines), lines_to_read, )
        self.assertEqual(lines[0], '20:10:29.085040 185130259 dqhl gzytdvpprvflrivlle h    i', 'Первая прочитанная строка не равна строке из файла')
        self.assertEqual(lines[lines_to_read - 1], '20:10:29.085040 258262132 vzkpk ivvdtpsxlcffehbibvgmjkvq', '{0} строка не равна строке из файла'.format(lines_to_read))
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
        self.assertEqual(self.fe.read(), '20:10:29.085040 987719878  p tiwj   puca yhl kt gqqeihc', 'читается неправильная строка')

    def test_read_n_lines_from_start_pos(self):
        ''' чтение указанного количества строк, начиная с указанной позиции '''
        start_pos = 12
        lines_to_read = 5
        lines = self.fe.read(lines_to_read, start_pos)
        self.assertEqual(len(lines), lines_to_read, 'прочитаны не все строки')
        self.assertEqual(lines[0], '20:10:29.086017 392548458 hcwxu rr doiu mofiansylomvsfi', 'Первая прочитанная строка не равна строке из файла')
        self.assertEqual(lines[lines_to_read - 1], '20:10:29.086017 858173529 r evgcpe cepkzed daz fddjdecmu', '{0} строка не равна строке из файла'.format(start_pos + lines_to_read))
        self.assertEqual(self.fe.cur_line_index, start_pos + lines_to_read, 'после чтения курсор не на той позиции')

    def test_search_string_exsistint_string_return_True(self):
        ''' поиск существующеего текста в логе '''
        text_to_search = '291894706'
        self.fe = FileExplorer(open, DATA_43_LOG)
        is_found = self.fe.search_string(text_to_search)
        self.assertTrue(is_found, 'существующий в логе текст не найден')
        self.assertEqual(self.fe.cur_line_index, 35419, 'неправильный индекс у найденной строки')

    def test_read_till_end_of_file(self):
        ''' чтение до конца файла '''
        self.fe.seek(999)
        last_line = self.fe.read()
        self.assertEqual(last_line, '20:10:29.149529 293517476 bmsmbnbbmb pjxvia ghg arvirots', 'Последняя линия прочитана неправильно')
        self.assertEqual(self.fe.cur_line_index, 1000, 'индекс последней строки (EOF) не верен')
        self.assertEqual(self.fe.read(), '', 'При чтении в конце файла не возвращается пустой символ')
        self.assertEqual(self.fe.EOF, True, 'Не проставлен флаг окончания файла')
        self.assertEqual(self.fe.read(), '', 'При чтении в конце файла не возвращается пустой символ')
        self.assertEqual(self.fe.cur_line_index, 1000, 'после чтение в конце файла индекс последней строки изменился. Этого быть не должно')

    def test_read_n_lines_more_than_end_of_file(self):
        ''' чтение строк больше чем есть в файле '''
        end_lines = self.fe.read(50, 990)
        self.assertEqual(len(end_lines), 10, 'Прочитано неверное количество строк')
        self.assertEqual(end_lines[-1], '20:10:29.149529 293517476 bmsmbnbbmb pjxvia ghg arvirots', 'Последняя строка неверная')

    def test_read_till_x_return_to_y_and_then_read_till_z_more_than_x(self):
        ''' Прочитать до Х, затем вернуться до y затем читать до Z > X'''
        x, y, z = 5, 2, 7
        self.fe.read(x)
        self.fe.seek(y)
        self.fe.read(z)
        self.assertEqual(self.fe.cur_line_index, 9)

if __name__ == '__main__':
    unittest.main()
