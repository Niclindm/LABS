import unittest
from tramdata import *

TRAM_FILE = 'DATA/tramnetwork.json'
TRAM_LINES = 'DATA/tramlines.txt'

class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            tramdict = json.loads(trams.read())
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']
            self.maxDiff = None

    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg = stop + ' not in stopdict')
            
    def test_lines_equal(self): #check if linedict lines are same as tramlines.txt in order
        with open(TRAM_LINES, 'r') as f:
            d = f.read()
        lines = d.split('\n\n')[:-1]
        expected_lines = []
        for line in lines:
            expected_lines.append(line[0:2].replace(":",""))
        actual_lines = list(self.linedict.keys())
        
        self.assertListEqual(expected_lines, actual_lines)
    
    def test_stops_per_line(self): #check if linedict stops are same as tramlines.txt in order
        with open(TRAM_LINES) as f:
            d = f.read()
    
        lines = d.split('\n\n')[:-1]

        line_list = []

        for line in lines:

            current_line_iter = line.split('\n')

            stop_lines = current_line_iter[1:]

            for temp, line in enumerate(stop_lines):
                stop = line[:-6].strip()
                line_list.append(stop)


        linedict_list = []
        for key in self.linedict.keys():
            for value in self.linedict[key]:
                linedict_list.append(value)

        self.assertListEqual(line_list,linedict_list)


    def test_time(self): #tests if time from a to b is same as b to a of all stops and lines
        for line in self.linedict:
            for stop1 in line:
                for stop2 in line:
                    self.assertEqual(
                        time_between_stops(TRAMNETWORK, line, stop1, stop2), 
                        time_between_stops(TRAMNETWORK, line, stop2, stop1)
                        )
    def test_distance_feasible(self): #test if distance of all stations are less than 20.0km 
        duplicates = []
        for stop1 in self.stopdict:
            for stop2 in self.stopdict:

                if (stop1, stop2) not in duplicates and stop1 != stop2:
                    distance = distance_between_stops(TRAMNETWORK, stop1, stop2)
                    self.assertLess(distance, 20.0)
                    duplicates.append((stop2, stop1))

if __name__ == '__main__':
    unittest.main()


