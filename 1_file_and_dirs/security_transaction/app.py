# Запись в файл только если не было ошибок, реализуется через временный файл
# двумя вариантами
# с помощью класса
import os
import tempfile


class AtomicWrite:
    def __init__(self, path, mode='w', encoding='utf-8'):
        self.path = path
        self.mode = mode if mode == 'wb' else 'w'
        self.encoding = encoding

    def __enter__(self, ):
        self.temp_file = tempfile.NamedTemporaryFile(
            self.mode,
            encoding=self.encoding,
            delete=False,
        )
        return self.temp_file

    def __exit__(self, exc_type, exc_message, traceback):
        self.temp_file.close()
        if exc_type is None:
            os.rename(self.temp_file.name, self.path)
        else:
            os.unlink(self.temp_file.name)


# и с помощью contextmanager
from contextlib import contextmanager


@contextmanager
def atomic_writes(path, mode='w', encoding='utf-8'):
    mode = mode if mode == 'wb' else 'w'
    temp_file = tempfile.NamedTemporaryFile(mode,
                                            encoding=encoding,
                                            delete=False)
    try:
        yield temp_file
    except Exception as e:
        temp_file.close()
        os.unlink(temp_file.name)
        print(f'Ошибка {e}!')
    else:
        temp_file.close()
        try:
            os.rename(temp_file.name, path)
        except OSError as e:
            os.unlink(temp_file.name)
            print(f'Ошибка {e}!')


if __name__ == '__main__':
    items = ['Это', 'просто', 'праздник', 'какой-то', ]

    with atomic_writes('text.txt') as f:
        for coun, item in enumerate(items):
            f.write(f'{item}\n')
