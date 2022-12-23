import sys
sys.path.append('/Users/nick/LABS/DATA')
import json
import math

TRAMSTOPS = 'DATA/tramstops.json'
TRAMLINES = 'DATA/tramlines.txt'
TRAMNETWORK = 'DATA/tramnetwork.json'


def build_tram_stops(jsonobject):
    with open(jsonobject, 'r') as f:
        d = json.load(f)

    dict_stops = {}

    for key in d.keys():
        lat, lon = d[key]['position']
        dict_stops[key] = {'lat': lat, 'lon': lon}

    return dict_stops


def get_stop_and_time (line):
    ## Extract data
    time = line[-6:] # extracts time
    stop = line[:-6].strip() # extracts stop by removing spaces
    return stop, time

def parse_time(time_string):
    mins = time_string.split(':')[-1]
    if mins[0] == '0':
        return int(mins[1:])
    else:
        return int(mins)

def build_tram_lines(lines):

    with open(lines, 'r') as f:
        d = f.read()
    
    lines = d.split('\n\n')[:-1]

    line_dict = {}
    time_dict = {}

    for line in lines:

        current_line_iter = line.split('\n')
        current_line = current_line_iter[0]
        line_dict[current_line] = []

        stop_lines = current_line_iter[1:]

        for index, line in enumerate(stop_lines):
            stop, time = get_stop_and_time(line)

            line_dict[current_line].append(stop)

            ## get next stop
            if index != len(stop_lines) - 1:
                next_stop, next_time = get_stop_and_time(stop_lines[index+1])
                time_diff = parse_time(next_time) - parse_time(time)

                if stop not in time_dict:
                    time_dict[stop] = {}

                time_dict[stop][next_stop] = time_diff
    line_dict = {key.strip()[:-1]: value for key, value in line_dict.items()}
    return time_dict, line_dict

def build_tram_network():
    dict_stops = build_tram_stops(TRAMSTOPS)
    time_dict, line_dict = build_tram_lines(TRAMLINES)
    tramnetwork_dict =  {
    "stops": dict_stops,
    "lines": line_dict,
    "times": time_dict
    } 
    with open(TRAMNETWORK, 'w') as jsonfile:
        json.dump(tramnetwork_dict, jsonfile, indent=6)
    jsonfile.close()

    return tramnetwork_dict

def lines_via_stop(somedicts, stops):

    with open(somedicts,'r') as f:
        d = json.load(f)

    if stops not in d['stops']:
        return None
    
    keys = [key for key, value in d['lines'].items() if stops in value]
    return keys

def lines_between_stops(somedicts, stop1, stop2):
    with open(somedicts, 'r') as f:
        d = json.load(f)
    if (stop1 and stop2) not in d['stops']:
        return None
    list_of_lines = []

    keys = [key for key, value in d['lines'].items() if stop1 in value and stop2 in value]
    for key in keys:
        if key not in list_of_lines:
            list_of_lines.append(key)
    return list_of_lines
    

def time_between_stops(somedicts, line, stop1, stop2):
    with open(somedicts, 'r') as f:
        d = json.load(f)

    if str(line) not in d["lines"]:
        return None
    
    linestops = d["lines"][str(line)]
    stopslist = []

    if (stop1 and stop2) in linestops:
        for entries in linestops:
            if stop1 in stopslist and stop2 in stopslist:
                break
            if entries == stop1 or entries == stop2:
                stopslist.append(entries)
            elif len(stopslist) != 0:
                stopslist.append(entries)
    else:
        return None


    time = 0

    for i in stopslist[:-1]:
        keys = d["times"][i].keys()
        for key in keys:
            if key in stopslist[stopslist.index(i)+1]:
                time += (d["times"][i][key])

    return time 

      
    

def distance_between_stops(somedicts, stop1, stop2):
    with open(somedicts, "r") as f:
        d = json.load(f)
    if (stop1 and stop2) not in d['stops']:
        return None
    R = 6371 #radius of earth in kilometers
    lat1 = math.radians(float(d["stops"][stop1]["lat"]))
    lon1 = math.radians(float(d["stops"][stop1]["lon"]))
    lat2 = math.radians(float(d["stops"][stop2]["lat"]))
    lon2 = math.radians(float(d["stops"][stop2]["lon"]))
    mean_lat = (lat1 + lat2)/2
    c = math.sqrt(math.pow((lat2-lat1),2)+math.pow((math.cos(mean_lat)*(lon2-lon1)),2))
    return c*R




def answer_query(input_str):

    build_tram_network()
    answer = None
    string1 = ""
    string2 = ""
    stop1 = None
    stop2 = None 
    line = None


    if input_str[0:3] == "via":

        string1 = input_str.strip()
        answer = lines_via_stop(TRAMNETWORK, string1[4:])

    
    if input_str[0:8] == "between ":

        stop1 = input_str.index(" and ")
        string1 = input_str[8:stop1]
        string2 = input_str[stop1+5:]
        answer = lines_between_stops(TRAMNETWORK, string1, string2)
    
    if input_str[0:10] == 'time with ':

        stop1 = input_str.index(" from ")
        stop2 = input_str.index(" to ")
        line = input_str[10:stop1]
        string1 = input_str[stop1+6:stop2]
        string2 = input_str[stop2+4:]

        answer = time_between_stops(TRAMNETWORK, line, string1, string2)

    if input_str[0:14] == "distance from ":
                
        stop1 = input_str.index(" to ")
        string1 = input_str[14:stop1]
        string2 = input_str[stop1+4:]


        answer = distance_between_stops(TRAMNETWORK, string1, string2)


    
    if answer == None or answer == []:
        return "Bad Argument"

    else:
        return answer

def dialogue():
    while True:
        try:
            input_str = input("> ").strip()
            if input_str == "exit":
                break
            else:
                answer = answer_query(input_str)
                print(answer)
        except ValueError: 
            "sorry, try again"

    quit()



if __name__ == '__main__':
    if sys.argv[1:] == ['init']:
        build_tram_network()
    else:
        dialogue()	
