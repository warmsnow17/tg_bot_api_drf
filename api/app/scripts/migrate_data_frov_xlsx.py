import pandas as pd
from bot_api.models import Road, City
from loguru import logger
import math

# загрузка данных из таблицы Excel
data = pd.read_excel('data.xlsx', sheet_name='Лист1')

# обработка данных
for index, row in data.iterrows():
    city_name = row['address'].split(',')[0]
    # получение или создание объекта City по имени города
    if city_name != '':
        city, created = City.objects.get_or_create(name=city_name)
    else:
        city, created = City.objects.get_or_create(name='Республиканские дороги')

    coordinates = row['wkt_geom'].split(',')[1].replace(' ', ',')
    if coordinates.startswith(','):
        coordinates = coordinates.lstrip(',')
    map_url = f'https://yandex.ru/maps/?ll={coordinates}&z=19&l=map'
    if not isinstance(row['_Планируемый год ремонта (кап. ремонт)'], float):
        road = Road(
            geolocation=map_url,
            status='WT',
            name=row['name'],
            repair_date=row['_Планируемый год ремонта (кап. ремонт)'],
            city=city,
        )
    else:
        road = Road(
            geolocation=map_url,
            status='BR',
            name=row['name'],
            city=city,
        )
    road.save()