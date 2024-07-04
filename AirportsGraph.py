import math
import string

from pandas import DataFrame


def get_travel_time(a_latitude, a_longitude, a_park_time, b_latitude, b_longitude, airplane_speed, airplane_range):
    dist = get_dist(a_latitude, a_longitude, b_latitude, b_longitude)
    if dist > airplane_range:
        return -1
    return dist / airplane_speed + a_park_time


def get_dist(lat1, lon1, lat2, lon2):
    R = 6371
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance


class AirportsGraph:

    def __init__(self, airports_df: DataFrame, plane: dict):
        self.airports_df = airports_df
        plane_speed = plane['speed']
        plane_range = plane['range']
        self.graph = []
        for i in range(len(airports_df)):
            a_latitude = airports_df['latitude'].values[i]
            a_longitude = airports_df['longitude'].values[i]
            a_park_time = airports_df['park_time'].values[i]
            dists = []
            for j in range(len(airports_df)):
                if i == j:
                    dists.append(-1)
                    continue
                b_latitude = airports_df['latitude'].values[j]
                b_longitude = airports_df['longitude'].values[j]
                dists.append(get_travel_time(
                    a_latitude,
                    a_longitude,
                    a_park_time,
                    b_latitude,
                    b_longitude,
                    plane_speed,
                    plane_range
                ))

            self.graph.append(dists)

        self.airports_name = dict()
        for i in range(len(airports_df)):
            self.airports_name[airports_df['name'].values[i]] = i

    def find_path(self, a_airport_name: string, b_airport_name: string):
        try:
            a_airport_id = self.airports_name[a_airport_name]
            b_airport_id = self.airports_name[b_airport_name]
        except KeyError:
            return []

        airports_path = [None for i in range(len(self.graph))]
        airports_path[a_airport_id] = [0]
        airports_dist = [math.inf] * len(self.graph)
        airports_dist[a_airport_id] = 0
        is_airports_done = [False] * len(self.graph)
        is_airports_done[a_airport_id] = True
        next_airport = a_airport_id

        while min(is_airports_done) is False:
            for i in range(len(airports_dist)):
                if (
                        is_airports_done[i] is False
                        and self.graph[next_airport][i] != -1
                        and airports_dist[i] > self.graph[next_airport][i] + airports_dist[next_airport]
                ):
                    airports_dist[i] = self.graph[next_airport][i] + airports_dist[next_airport]
                    airports_path[i] = []
                    for x in airports_path[next_airport]:
                        airports_path[i].append(x)
                    airports_path[i].append(i)

            min_id = is_airports_done.index(False)
            min_val = airports_dist[min_id]
            for i in range(len(airports_dist)):
                if is_airports_done[i] is False and airports_dist[i] < min_val:
                    min_val = airports_dist[i]
                    min_id = i
            if min_val == math.inf:
                break
            next_airport = min_id
            is_airports_done[next_airport] = True

        if airports_path[b_airport_id] is None:
            return []

        route_details = [{
            'airport_name': a_airport_name,
            'arrival_time': None,
            'departure_time': 0,
        }]
        arrival_time = -self.airports_df['park_time'].values[a_airport_id]
        for i in range(1, len(airports_path[b_airport_id])):
            airport_name = list(self.airports_name.keys())[airports_path[b_airport_id][i]]
            arrival_time += self.graph[airports_path[b_airport_id][i - 1]][airports_path[b_airport_id][i]]

            if i != len(airports_path[b_airport_id]) - 1:
                park_time = self.airports_df['park_time'].values[airports_path[b_airport_id][i]]
                departure_time = float(arrival_time + park_time)
            else:
                departure_time = None

            route_details.append({
                'airport_name': airport_name,
                'arrival_time': float(arrival_time),
                'departure_time': departure_time,
            })

        return route_details
