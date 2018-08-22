import os
import random
import string
from datetime import datetime

def join_unix(*argv):
    ''' конкатенация пути используя Unix-style сепаратор - / '''
    return os.path.join(*argv).replace('\\', '/')

def log_text_generator(lines_amount):
    ''' генерирует лог по формату <время> <уникальный в рамках файла 9-значный ID> <lorem ipsum>
    lines_amount - количество строк (Допустимо строго менее 10^9 строк) '''
    IDS_LENGTH = 999999999 
    if (lines_amount > IDS_LENGTH):
        raise Exception('Can not generate file with unique id for every line, for lines_amount > {0}'.format(IDS_LENGTH))
    log_lines = []
    ids = random.sample(range(0, IDS_LENGTH), lines_amount)
    for i in range(lines_amount):
        log_lines.append('{time} {id} {message}'.format_map(
            dict(
                time=datetime.now().strftime("%H:%M:%S.%f"), 
                id=str(ids[i]).zfill(9), 
                message=message_generator(30))))
    log_text = '\r\n'.join(log_lines)
    return log_text

def message_generator(text_length):
    ''' генерирует рандомную строку указанной длины из букв и пробелов '''
    return ''.join(random.choice(string.ascii_lowercase + '     ') for _ in range(text_length))
