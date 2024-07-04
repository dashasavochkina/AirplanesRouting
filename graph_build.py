import pandas as pd
from pandas import DataFrame
from AirportsGraph import AirportsGraph, get_dist

# 1
#построение графа аэропортов
# - считать csv файл с аэропортами
airports = pd.read_csv('data/airports.csv', sep=';')

planes = pd.read_csv('data/planes.csv', sep=';')

#airports_graph = AirportsGraph(airports, dict(planes['airbus']))
planes1 = AirportsGraph(airports, planes[planes['name'] == 'airbus 610'].to_dict(orient='records')[0])
print(DataFrame(planes1.graph))
print(planes1.find_path('AIR0', 'AIR2'))


