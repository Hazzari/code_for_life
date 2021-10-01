#!/usr/bin/env python

import argparse
import datetime
import logging
import os
import time
from pathlib import Path


def set_settings() -> dict:
    """
    Настраивает логи и парсит аргументы командной строки
    :return: возвращает Namespace аргументов командной строки
    """

    app_params = {}
    parser = argparse.ArgumentParser(description='Поиск подозрительных файлов')
    parser.add_argument('--path', '-p',
                        action='store',
                        help='Папка для поиска',
                        default='data')

    parser.add_argument('--date', '-d',
                        action='store',
                        type=datetime.datetime.fromisoformat,
                        help='Контрольное время в формате: '
                             '"YYYY-MM-DD HH:MM:SS" '
                             'example: "2011-11-04T00:05:23+04:00"',
                        )

    parser.add_argument('--debug',
                        action='store',
                        choices=[20, 10],
                        help=f'Debug режим',
                        default=10)

    args_app = parser.parse_args()
    app_log_level = args_app.debug

    file_log = logging.FileHandler('find_virus.log')
    console_out = logging.StreamHandler()

    logging.basicConfig(handlers=(file_log, console_out),
                        format='%(asctime)s | %(levelname)s : %(message)s',
                        datefmt='%m.%d.%Y-%H:%M:%S:%Z',
                        level=app_log_level)
    print(app_log_level)

    app_params['path'] = args_app.path
    app_params['date'] = args_app.date
    return app_params


def get_absolute_path(path: Path) -> Path:
    """
    Создаем абсолютный путь если он относительный
    :param path: Path путь
    :return: экземпляр Path пути
    """
    if not path.is_absolute():
        path = Path(path).resolve()
    return path


def defines_a_file_or_folder_or_none(current_path: Path) -> list[Path]:
    """
    Создаем список файлов если передан путь к директории
    или один файл если передан путь к файлу
    :param current_path: Path путь к файлу или директории
    :return: список файлов в формате Path
    """
    result = []
    if current_path.is_file():
        result.append(current_path)
    if current_path.is_dir():
        file = ([Path(root_dir, file)
                 for root_dir, d, file_list in os.walk(current_path)
                 for file in file_list])
        if file:
            result += file
    return result


def find_virus(*, file_list, date_time):
    for str_file in file_list:
        logging.info(f'WARNING файл {str_file} '
                     f'был изменен с {date_time}')


def check(file: Path) -> tuple:
    def get_change_time(check_file: Path) -> float:
        m_time = os.stat(check_file).st_mtime
        a_time = os.stat(check_file).st_atime
        c_time = os.stat(check_file).st_ctime
        return max(m_time, a_time, c_time)

    current_ts = time.time()
    change_time = get_change_time(file)

    return current_ts - change_time, file


def main(*, settings: dict) -> None:
    # Создаем Path путь
    args_path = Path(settings.get('path'))

    # Проверяем на относительность пути
    path = get_absolute_path(args_path)

    # Формирует список файлов для проверки
    files = defines_a_file_or_folder_or_none(path)
    if not files:
        logging.info(f'Файлов по пути: "{path}" не найдено.')
        logging.info(f'------>>>>>> Остановка проверки')
        exit(code=0)
    checked_file_parameters = [check(file) for file in files]
    current_time = datetime.datetime.now()

    # Время отсчета
    time_border = (current_time - settings.get('date')).total_seconds()

    # Валидация файлов на изменение с даты
    not_valid_file = [p
                      for x, p in checked_file_parameters
                      if x < time_border]
    if not_valid_file:
        find_virus(file_list=not_valid_file, date_time=settings.get('date'))


if __name__ == '__main__':
    args = set_settings()
    logging.info(f'------>>>>>> Запуск проверки')

    # Запуск программы
    main(settings=args)

    # Выход из программы
    logging.info(f'------>>>>>> Остановка проверки')
    exit(0)
