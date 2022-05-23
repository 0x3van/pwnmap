import os

from .default import DefaultUtil


class FileUtil:

    @staticmethod
    def get_file_path(*path):
        file_path = os.path.join(*list(map(str, path)))

        if file_path.startswith('/') or file_path.startswith('~'):
            return file_path

        dir_path = os.path.join(DefaultUtil.OUT_PATH, os.path.dirname(file_path))

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        return os.path.join(DefaultUtil.OUT_PATH, file_path)

    @staticmethod
    def exists(path, dir=False, raise_exception=True):
        exists = os.path.exists(path) and (not os.path.isdir(path) if dir is False else os.path.isdir(path))

        if exists is False and raise_exception is True:
            raise IOError('%s not found: %s' % ('Directory' if dir is True else 'File', path))

        return exists

    @staticmethod
    def read_lines(file_path):
        with open(file_path, encoding='utf-8', errors='ignore') as f:
            return [x.strip() for x in f.readlines() if len(x.strip()) > 0]
