"""
Программа которая конвертирует изображения в заданный формат и размер
"""
from pathlib import Path

from PIL import Image

DIRECTORY = 'data'
FROM_EXTENSION = 'jpg'
TO_EXTENSION = 'png'
MAX_SIZE = (500, 500)


def walk(*, directory):
    path = Path(directory).absolute()
    for file in path.glob(f'*.{FROM_EXTENSION}'):
        conversion(file)


def conversion(file):
    resize(file)
    new_file = Path(f'{DIRECTORY}/{file.stem}.{TO_EXTENSION}')
    im = Image.open(file)
    im.save(new_file)
    file.unlink()


def resize(file):
    im: Image = Image.open(file)
    im.thumbnail(MAX_SIZE, Image.ANTIALIAS)
    im.save(file)


if __name__ == '__main__':
    walk(directory=DIRECTORY)
