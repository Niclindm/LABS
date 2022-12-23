import json

# imports added in Lab3 version
import math
import os
from .graphs import WeightedGraph
from django.conf import settings

TRAM_FILE = os.path.join(settings.BASE_DIR, 'static/tramnetwork.json')
#TRAM_FILE = 'static/tramnetwork.json'

import sys
sys.path.append('/Users/nick/LABS/LAB1')
import tramdata as td

class TramNetwork(WeightedGraph):

    def __init__(self, lines, stops, times):
        super().__init__()
        self._linedict = {}
        self._stopdict = {}
        self._timedict = {}
        if lines: 
            for line in lines:
                self._linedict[line] = TramLine(line, lines[line])
        if stops:
            for stop in stops:
                lines_via_stop = td.lines_via_stop(TRAM_FILE, stop)
                self._stopdict[stop] = TramStop(stop, lines=lines_via_stop, lat=stops[stop]['lat'], lon=stops[stop]['lon'])
        if times:
            self._timedict = times
        for stops in self.all_stops():
            self.add_vertex(stop)

        for stop in self._timedict:
            for connected_stop in self._timedict[stop]:
                self.add_edge(stop, connected_stop)
                self.set_weight(stop, connected_stop, self.transition_time(stop, connected_stop))
                if not self.transition_time(stop,connected_stop):
                    self.set_weight(stop, connected_stop, 0)

    def all_lines(self):
        return list(self._linedict.keys())

    def all_stops(self):
        return list(self._stopdict.keys())

    # def extreme_positions(self):
    #     temp_min_lat = 100000
    #     temp_max_lat = 0
    #     temp_min_lon = 100000
    #     temp_max_lon = 0
    #     for stop in self._stopdict.keys():
    #         if self._stopdict[stop]['lat'] > temp_max_lat:
    #             temp_max_lat = self._stopdict[stop]['lat']
    #         if self._stopdict[stop]['lat'] < temp_min_lat:
    #             temp_min_lat = self._stopdict[stop]['lat']
    #         if self._stopdict[stop]['lon'] > temp_max_lon:
    #             temp_max_lon = self._stopdict[stop]['lon']
    #         if self._stopdict[stop]['lon'] < temp_min_lon:
    #             temp_min_lon = self._stopdict[stop]['lon']
    #     extreme_pos = {
    #     'max_lon': temp_max_lon, 
    #     'max_lat': temp_max_lat, 
    #     'min_lon': temp_min_lon, 
    #     'min_lat': temp_min_lat
    #     }
    #     return extreme_pos

    def extreme_positions(self):
        stops = self._stopdict.keys()
        minlat = float(min([self.stop_position(s)[0] for s in stops]))
        minlon = float(min([self.stop_position(s)[1] for s in stops]))
        maxlat = float(max([self.stop_position(s)[0] for s in stops]))
        maxlon = float(max([self.stop_position(s)[1] for s in stops]))
        return minlon, minlat, maxlon, maxlat
    
    def geo_distance(self, a, b):
        D = td.distance_between_stops(TRAM_FILE, str(a), str(b))
        if D:
            return round(D,3)
        else:
            print("bad argument")

    def line_stops(self, line):
        if str(line) in list(self._linedict.keys()):
            return list(self._linedict[str(line)].get_stops())

    
    def stop_lines(self, a):
        if a in self.all_stops():
            return self._stopdict[a].get_lines()

    def stop_position(self, a):
        if a in self.all_stops():
            return self._stopdict[a].get_position()


    def transition_time(self, a, b):
        try:
            if self._timedict[a][b]:
                return self._timedict[a][b]
        except:
            print("not adjecent")





    

class TramLine():
    def __init__(self, num, stops):
        if num:
            self._number = str(num)
        else: 
            self._number = str()
        if stops:
            self._stops = stops
        else:
            self._stops = [] 

    def get_stops(self):
        return self._stops

    def get_number(self):
        return self._number


class TramStop():
    def __init__(self, name, lines=[], lat=None, lon=None):
        if name:
            self._name = str(name)

            self._lines = lines

            if (lat and lon) != None:
                self._postition = tuple((lat, lon))
            else:
                self._postition = tuple()

        else: 
            print("requies name argument")

    
    def add_line(self, line):
        if str(line) not in self._lines:
            self._lines.append(str(line))

    def get_lines(self):
        return self._lines

    def get_name(self):
        return self._name

    def get_position(self):
        if self._postition:
            return self._postition

    def set_position(self, lat, lon):
        if (lat and lon) != None:
            self._postition = tuple(lat, lon)

def readTramNetwork(tramfile=TRAM_FILE):
    with open(tramfile, 'r') as f:
        d = json.load(f)
    lines = d['lines']
    stops = d['stops']
    times = d['times']
    return TramNetwork(lines, stops, times)




# Bonus task 1: take changes into account and show used tram lines

# def specialize_stops_to_lines(self, network):
#     for line in network.all_lines():
#         for stop in network.lines_stops(line):
#             WeightedGraph.remove_vertex(stop)
#             WeightedGraph.add_vertex((stop, line))

#     for vtx in WeightedGraph.vertices():
#         for v in WeightedGraph.vertices():
#             for edge in WeightedGraph.edges():
#                 if (vtx[0], v[0]) == edge:
#                     WeightedGraph.add_edge(vtx, v)
#                     if vtx[1] == v[1]:
#                         WeightedGraph.set_weight(vtx,v,WeightedGraph.get_weight(edge[0],edge[1]))
#                     if vtx[1] != v[1]:
#                         WeightedGraph.set_weight(vtx,v,WeightedGraph.get_weight(edge[0],edge[1])+10)


# def specialized_transition_time(spec_network, a, b, changetime=10):
#     # TODO: write this function as specified
#     return changetime


# def specialized_geo_distance(spec_network, a, b, changedistance=0.02):
#     # TODO: write this function as specified
#     return changedistance
