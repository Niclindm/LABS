import graphs as graphs
import json
import sys
import graphviz
sys.path.append('/Users/nick/Desktop/LABS/LAB1')
import tramdata as td

TRAM_FILE = 'DATA/tramnetwork.json'

class TramNetwork(graphs.WeightedGraph):


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

    def all_lines(self):
        return list(self._linedict.keys())

    def all_stops(self):
        return list(self._stopdict.keys())

    def extreme_positions(self):
        temp_min_lat = 100000
        temp_max_lat = 0
        temp_min_lon = 100000
        temp_max_lon = 0
        for stop in self._stopdict.keys():
            if self._stopdict[stop]['lat'] > temp_max_lat:
                temp_max_lat = self._stopdict[stop]['lat']
            if self._stopdict[stop]['lat'] < temp_min_lat:
                temp_min_lat = self._stopdict[stop]['lat']
            if self._stopdict[stop]['lon'] > temp_max_lon:
                temp_max_lon = self._stopdict[stop]['lon']
            if self._stopdict[stop]['lon'] < temp_min_lon:
                temp_min_lon = self._stopdict[stop]['lon']
        extreme_pos = {
        'max_lon': temp_max_lon, 
        'max_lat': temp_max_lat, 
        'min_lon': temp_min_lon, 
        'min_lat': temp_min_lat
        }
        return extreme_pos
    
    def geo_distance(self, a, b):
        D = td.distance_between_stops(str(a),str(b))
        if D:
            return round(D)
        else:
            print("bad argument")

    def lines_stops(self, line):
        if str(line) in list(self._linedict.keys()):
            return self._linedict[str(line)].get_stops()

    
    def stop_lines(self, a):
        if a in self.all_stops():
            return a.get_lines()


    def stop_position(self, a):
        if a in self.all_stops():
            return a.get_position()


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


def demo():
    G = readTramNetwork(TRAM_FILE)
    a, b = input('from,to ').split(',')
    graphs.view_shortest(G, a, b)

if __name__ == '__main__':
    demo()
