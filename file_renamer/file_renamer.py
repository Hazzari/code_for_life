import os
from pathlib import Path
import logging


class Renamer:
    """ Ренеймер файлов, переименовывает по шаблону : File_<000>.*
        по умолчанию файлы берет из папки 'data' рядом с проектом. """

    def __init__(self, *, data_dirs: str = 'data', pattern: str = 'File_', count_zero: int = 5, start_count: int = 1):
        self.__data_dirs = data_dirs
        self.__pattern = pattern
        self.__count_zero = count_zero
        self.__count = start_count
        self.__path_dirs = Path(__file__).resolve().parent / self.__data_dirs

    def __find_all_file_in_dirs(self):
        """Формирует словарь директорий и списков файлов в ней"""
        return {r: f for r, d, f in os.walk(self.__path_dirs)}

    def __format_file_name(self, file: str, pattern):
        """Создает строку вида File_<0001>.*"""
        return f'{pattern}' \
               f'{str(self.__count).zfill(self.__count_zero)}.' \
               f'{file.split(".")[-1]}'

    def __rename_file(self, d, file: str):
        """Переименовывает файлы"""
        try:
            old_file = Path(d, file)
            new_file = Path(d, self.__format_file_name(file, self.__pattern))
            os.rename(old_file, new_file)
        except Exception as e:
            logging.error(e)
        else:
            self.__count += 1

    def run(self):
        for d, file_list in self.__find_all_file_in_dirs().items():
            [self.__rename_file(d, file, ) for file in file_list]


if __name__ == '__main__':
    Renamer(count_zero=3).run()
