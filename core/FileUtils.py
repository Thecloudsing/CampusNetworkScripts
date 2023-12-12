from os import mkdir
from os.path import isdir, isfile
import typing


class BinFile(object):
    def __init__(self, file, supplement=False):
        self.supplement = supplement
        self.writefile: typing.BinaryIO
        self.readfile: typing.BinaryIO

        if supplement:
            self.writefile = open(file, mode='+ab')
            self.readfile = open(file, mode='rb')
        else:
            if not isfile(file):
                with open(file, mode='wb'):
                    pass
            file = open(file, mode='r+b')
            self.file = file
            self.writefile = file
            self.readfile = file

    def close(self):
        if self.supplement:
            self.readfile.close()
            self.writefile.close()
        else:
            self.file.close()

    def flush(self):
        self.writefile.flush()

    def writer(self, s: typing.Union[bytes, bytearray]):
        return self.writefile.write(s)

    def read_all(self):
        return self.readfile.read().decode()

    def last_line(self):
        file = self.readfile
        offset = -1
        oneline = file.readline()
        count = 10
        while count > 0:
            count -= 1
            line = file.readline()
            if not line:
                return oneline.decode()
            oneline = line

        while True:
            file.seek(offset, 2)
            lines = file.readlines()
            if len(lines) > 2:
                return lines[-1].decode()
            offset *= 2


def exists_dir(path):
    isdir(path) or mkdir(path)


def batch_exists_dir(paths: list[str]):
    for path in paths:
        exists_dir(path)
