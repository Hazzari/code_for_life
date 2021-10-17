from pathlib import Path

import eyed3


def walk(*, directory):
    path = Path(directory).absolute()
    for file in path.iterdir():
        set_tags(file,
                 tags={
                     'title': file.name,
                     'year': '2020',
                     'album': 'legal'
                 })


def set_tags(file, *, tags: dict):
    audio_file = eyed3.load(file)
    audio_file.initTag()
    audio_file.tag.title = tags.get('title', None)
    audio_file.tag.year = tags.get('year', '2021')
    audio_file.tag.album = tags.get('album', None)
    audio_file.tag.save()


def main():
    walk(directory='data')


if __name__ == '__main__':
    main()
