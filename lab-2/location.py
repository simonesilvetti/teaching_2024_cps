import math

import matplotlib.pyplot as plt

import geopy.distance


class Location:
    def __init__(self, index, name, coordinates, trace):
        self.index = index
        self.name = name
        self.coordinates = coordinates
        self.trace = trace

    def distance(self, other):
        left = self.coordinates
        right = other.coordinates
        return geopy.distance.distance(left, right).m

    def get_trace_values(self):
        return [[value[1]] for value in self.trace]

    def get_trace_time(self):
        return [value[0] for value in self.trace]

    def __str__(self):
        return f"[{self.index},{self.coordinates}]"


class LocationDatabase:
    def __init__(self):
        self.db = list()

    @staticmethod
    def get_location_full(df, name, index):
        location = df[df['NAME'] == name]
        row = location.iloc[0]
        coordinates = row['LAT'], row['LONG']
        traces = location.apply(lambda row: (
            row['ABS_TIME'], row['NBBIKES']), axis=1)
        values = list(traces.values)
        values.sort(key=lambda x: x[0])
        return Location(index, name, coordinates, values)

    def generate_from_df(self, df):
        location_names = df['NAME'].unique()
        n = 0
        for name in location_names:
            self.db.append(self.get_location_full(df, name, n))
            n = n+1

    def get_graph(self):
        graph = []
        for l_idx in range(len(self.db)):
            for r_idx in range(len(self.db)):
                left_location = self.db[l_idx]
                right_location = self.db[r_idx]
                graph.append([left_location.index, right_location.index,
                             left_location.distance(right_location)])
        return [graph]

    def get_traces(self):
        return [location.get_trace_values() for location in self.db]

    def get_time(self):
        return self.db[0].get_trace_time()

    def show_locations_map(self):
        coordinates = [location.coordinates for location in self.db]
        lat = [x[0] for x in coordinates]
        long = [x[1] for x in coordinates]
        print("lat", min(lat), max(lat))
        print("long", min(long), max(long))
        plt.scatter(lat, long)
        plt.show()

    def __str__(self):
        return str([str(location) for location in self.db])
