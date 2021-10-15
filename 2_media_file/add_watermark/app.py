from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FILE_JPG = Path('1.jpg')
FILE_PNG = Path('2.png')
FONTS = Path('roboto.ttf')
COLOR = (255, 0, 0, 50)
OFFSET = 10


def add_watermark(file: Path, text):
    # Открыть файл
    image = Image.open(file)
    # Запомнить формат
    type_image = 'RGB' if image.format == 'JPEG' else 'RGBA'
    # Конвертировать в слой с прозрачностью
    image = image.convert('RGBA')
    # Создать новое изображение
    image_watermark = Image.new('RGBA', image.size)
    draw = ImageDraw.Draw(image_watermark)
    # Взять размеры оригинального изображения
    width, height = image.size
    # Создать Шрифт Высотой 10% от размера высоты исходного изображения
    font = ImageFont.truetype(f'{FONTS}', int(height / 10))
    # Взять значения высоты и ширины текста и запомнить их значения
    text_width, text_height = draw.textsize(text, font)
    # Расчитать местоположение надписи
    text_x = width - text_width - 10
    text_y = height - text_height - 10
    # Разместить надпись в указанном месте
    draw.text((text_x, text_y), text, COLOR, font)
    # Соединить 2 слоя
    result = Image.alpha_composite(image, image_watermark)
    # Сохранить конвертируемый файл
    result.convert(type_image).save(f'watermark_{file.name}')


if __name__ == '__main__':
    add_watermark(FILE_JPG, 'Тут любой текст ')
    add_watermark(FILE_PNG, 'Тестовый текст')
