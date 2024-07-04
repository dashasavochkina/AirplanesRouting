import datetime
import math
import pandas as pd
from pandas import DataFrame
from AirportsGraph import AirportsGraph

def hours_to_time(hours: float):
    if math.isnan(hours) or hours is None:
        return None
    seconds = round(hours * 3600)
    return datetime.time(seconds // 3600 % 24, seconds % 3600 // 60, seconds % 60)

# считать csv файл с аэропортами и самолетами
airports = pd.read_csv('data/airports.csv', sep=';')
planes = pd.read_csv('data/planes.csv', sep=';')

# считываем параметры перелета
departure_airport_name = input('Введите аэропорт отправления: ')
arrival_airport_name = input('Введите аэропорт прибытия: ')
plane_name = input('Введите модель самолета: ')

# cобираем граф и находим путь перелета
airportsGraph = AirportsGraph(airports, planes[planes['name'] == plane_name].to_dict(orient='records')[0])
route = DataFrame(airportsGraph.find_path(departure_airport_name, arrival_airport_name))

# если в итоговом маршруте нет ни одного аэропорта, то путь не найден
if len(route) == 0:
    print('На данном самоелете невозможно совершить такой перелет')
else:
    # иначе переводим часы в читабельный формат
    route['arrival_time_formatted'] = route['arrival_time'].apply(hours_to_time)
    route['departure_time_formatted'] = route['departure_time'].apply(hours_to_time)
    route.drop('departure_time', axis=1, inplace=True)
    route.drop('arrival_time', axis=1, inplace=True)
    print(route)
