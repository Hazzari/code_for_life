import re
from statistics import mean

import pandas as pd
import requests
from bs4 import BeautifulSoup


def parsing_site(start_page):
    """ПАРСИТ САЙТ ПОСТРАНИЧНО"""
    pages = get_all_pages(get_html(start_page), start_page)
    result = {}
    for page in pages:
        prices = get_prices(get_html(page))
        result = result | prices
    writing_to_file(result)


def writing_to_file(data: dict):
    """Запись словаря в excel файл"""
    file = pd.DataFrame.from_dict(data,
                                  orient="index",
                                  columns=["min price", "max price",
                                           "Средняя цена"], )
    file.to_excel("data/e-catalog.xlsx", sheet_name='e-catalog', index=False)


def get_prices(html):
    """Получение цены товара

        :return (min, max, mean) price
    """
    bs = BeautifulSoup(html, 'html.parser')
    elements = bs.select('div.model-price-range')
    result = {}

    for elem in elements:
        span = elem.select('span')
        name_elem = elem.find('div', class_='jcontent')
        name = re.sub(r'\s+', ' ',
                      name_elem.getText()).lstrip('Сравнить цены и купить ')
        range_price = [int(re.sub(r'\W+', '', price.getText()))
                       for price in span
                       if price.getText()]
        price_1 = f'{range_price[0]}'
        if len(range_price) > 1:
            price_2 = f'{range_price[1]}'
        else:
            price_2 = f'-'
        result[name] = (price_1, price_2, f'{mean(range_price)}')
    return result


def get_html(url):
    """Запрос url страницы"""
    response = requests.get(url)
    return response.text


def get_all_pages(html, start_pages):
    """Получение всех страниц каталога"""
    bs = BeautifulSoup(html, 'html.parser')
    elements = bs.find('div', class_='ib page-num').find_all('a')
    count_pages = 0
    for elem in elements:
        try:
            page = int(elem.getText())
            if page > count_pages:
                count_pages = page
        except ValueError:
            pass
    pages = [start_pages]

    for i in range(1, count_pages):
        pages.append(start_pages + str(i) + '/')
    return pages


if __name__ == '__main__':
    PAGE = 'https://www.e-katalog.ru/list/206/'
    parsing_site(PAGE)
