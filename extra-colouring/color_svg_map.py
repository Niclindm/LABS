import json
import sys
sys.path.append('../LAB2')
import graphs as gr
import coloring as c
import xml.etree.ElementTree as ET

WHITEMAP_FILE = 'data/whitemap.svg'
COUNTRY_CODES_FILE = 'data/country_codes.json'
NEIGHBOR_FILE = 'data/neighbors.json' 
COLORMAP_FILE = 'colormap.svg'

def get_neighbors(codefile=COUNTRY_CODES_FILE, neighborfile=NEIGHBOR_FILE):
    countries = {}
    adjlist = []


    with open(codefile, 'r') as f:
        codes = json.load(f)
    
    with open(neighborfile, 'r') as f:
        neighbors = json.load(f)
    
    for code in codes:
        for neighb in neighbors:
            if code['Code'] == 'I' or code['Code'] == 'RU-Kaliningrad':
                continue
            else:
                if code['Name'] == neighb['countryLabel']:
                    countries[code['Code']] = {'Name': code['Name'], 'Neighbor' : []}
                    temp = set()
                    for cd in codes:
                        if cd['Code'] == 'I' or cd['Code'] == 'RU-Kaliningrad':
                            continue
                        if cd['Name'] == neighb['neighborLabel']:
                            temp.add(cd['Code'])
                    countries[code['Code']]['Neighbor'] = list(temp)
                    for i in list(temp):
                        if (i,code['Code']) not in adjlist:
                            adjlist.append((code['Code'],i))
    adjlist.append(('RU-KALININGRAD','PL'))
    adjlist.append(('RU-KALININGRAD','LT'))
    countries['RU-KALININGRAD'] = {'Name': "Russia", 'Neighbor' : ["LT", "PL"]}
    adjlist = list(set(adjlist))



    return countries, adjlist

def get_map_colors(neighbordict):
    G = gr.Graph(neighbordict)
    G.add_edge("GB", "IE") # added manualy, problem with not matching names in countrycode file and neighbors file
    colors = ['black', 'red', 'grey', 'orange']
    n = len(colors)
    stack = c.simplify(G, n)
    colormap = c.rebuild(G, stack, colors)
    gr.visualize(G,colors=colormap)
    return colormap

def color_svg_map(colordict, infile=WHITEMAP_FILE, outfile=COLORMAP_FILE):
    tree = ET.parse(infile)
    root = tree.getroot()


    for path in root.iter("{http://www.w3.org/2000/svg}path"):

        country_code = path.get("id").upper()
        if country_code == "RU-MAIN":
            color = colordict.get("RU")
        else:
            color = colordict.get(country_code)
        path.set("style", f"fill:{color}")
    tree.write(outfile)


def main():
    countries, adjlist = get_neighbors()
    country_color = get_map_colors(adjlist)
    color_svg_map(country_color)
if __name__ == "__main__":
    main()
