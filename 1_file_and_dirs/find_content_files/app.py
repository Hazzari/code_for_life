import os
from pathlib import Path

from utils import get_directory, get_find_string


def find(*, find_str, find_dir):
    for root, dirs, files in os.walk(find_dir):
        for name in files:
            find_string_in_file(Path(root, name), find_str)


def find_string_in_file(file, find_str):
    with open(file, 'r', encoding='utf-8') as f:
        gen_words = ((w, i) for w, i in enumerate(f.readlines(), start=1))
        for word in gen_words:
            if find_str in word[1]:
                custom_str = word[1].split()
                print(f'В файле {Path(file).name} '
                      f'было найдено слово "{find_str}" '
                      f'на строке: {word[0]}, '
                      f'в {custom_str.index(find_str) + 1} слове')


def main():
    search_dir: str = get_directory()
    find_str: str = get_find_string()
    find(find_str=find_str, find_dir=search_dir)


if __name__ == '__main__':
    print('--- Начало поиска ---')
    main()
    print('--- Конец поиска ---')
