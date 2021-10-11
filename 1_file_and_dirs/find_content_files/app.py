import asyncio
import os
from pathlib import Path


def get_directory():
    return '/Users/aleksan/Code/portfolio/code_for_life/1_file_and_dirs/find_content_files/data/'


def get_find_string():
    return 'курс'


async def find(*, find_str, find_dir):
    for root, dirs, files in os.walk(find_dir):
        for name in files:
            await find_string_in_file(Path(root, name), find_str)


async def find_string_in_file(file, find_str):
    pass


async def main():
    search_dir = get_directory()
    find_str = get_find_string()

    await find(find_str=find_str, find_dir=search_dir)


if __name__ == '__main__':
    asyncio.run(main())
