from collections import deque
import unittest
import trams as t
import json
TRAM_FILE = 'DATA/tramnetwork.json'

def BFS(G, node, goal=lambda n: False):
    Q = deque()
    explored = [node]
    Q.append(node)
    while Q:
        v = Q.popleft()
        if goal(v):
            return v
        for w in G.neighbors(v):
            if w not in explored:
                explored.append(w)
                Q.append(w)
    return explored

class TestTrams(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            tramdict = json.loads(trams.read())
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']
        
        self.maxDiff = None

    def test_stops_exist(self):
        G = t.readTramNetwork()
        stopset = {stop for stop in G.vertices()}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg = stop + ' not in stopdict')
            
    def test_lines_equal(self): 
        G = t.readTramNetwork()
        lines = self.linedict
        actual_lines = []
        for line in G.all_lines():
            self.assertListEqual(list(lines[line]), G._linedict[line].get_stops())
            actual_lines.append(line)
        
        self.assertListEqual(list(lines.keys()), actual_lines)
    
    def test_stops_pos(self):
        G = t.readTramNetwork()
        stops = self.stopdict
        for stop in stops:
            (lat,lon) = G._stopdict[stop].get_position()
            self.assertEqual(stops[stop]['lat'], lat)
            self.assertEqual(stops[stop]['lon'], lon)    
    
    def test_connectedness(self):
        G = t.readTramNetwork()

        for target in G.vertices():
            for node in G.vertices():
                all_stops = BFS(G,target,lambda n: n == node)
                self.assertEqual(all_stops, node)
    


if __name__ == '__main__':
    unittest.main()


