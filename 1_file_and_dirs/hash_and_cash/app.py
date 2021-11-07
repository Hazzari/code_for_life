# Пример хэшируемого ключа словаря
import csv
from collections import defaultdict

# Выводим все записи по месяцам
from pprint import pprint

employees_int = defaultdict(int)
with open('salary.csv', 'r', encoding='utf-8') as read_f:
    reader = csv.reader(read_f, delimiter=';')

    for row in reader:
        key = tuple(row[:4])
        if employees_int.get(key):
            employees_int[key] = employees_int[key] + int(row[4:][1])
        else:
            employees_int[key] = int(row[4:][1])

pprint(employees_int)

# Выводим общую сумму зп за период
employees_list = defaultdict(list)

with open('salary.csv', 'r', encoding='utf-8') as read_f:
    reader = csv.reader(read_f, delimiter=';')

    for row in reader:
        key = tuple(row[:4])
        employees_list[key].append(row[4:])

pprint(dict(employees_list))
