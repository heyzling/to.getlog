import os

def join_unix(*argv):
    ''' конкатенация пути используя Unix-style сепаратор - / '''
    return os.path.join(*argv).replace('\\', '/')