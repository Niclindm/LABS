import json
import sys
sys.path.append('LAB2')
import graphs as gr
import coloring as c
import xml.etree.ElementTree as ET

WHITEMAP_FILE = 'extra-colouring/data/whitemap.svg'
COUNTRY_CODES_FILE = 'extra-colouring/data/country_codes.json'
NEIGHBOR_FILE = 'extra-colouring/data/neighbors.json' 
COLORMAP_FILE = 'extra-colouring/colormap.svg'

def get_neighbors(codefile=COUNTRY_CODES_FILE, neighborfile=NEIGHBOR_FILE):
    countries = {}
    adjlist = []


    with open(codefile, 'r') as f:
        codes = json.load(f)
    
    with open(neighborfile, 'r') as f:
        neighbors = json.load(f)
    
    for code in codes:
        for neighb in neighbors:
            if code['Code'] == 'RU-main' or code['Code'] == 'RU-Kaliningrad':
                continue
            else:
                if code['Name'] == neighb['countryLabel']:
                    countries[code['Code']] = {'Name': code['Name'], 'Neighbor' : []}
                    temp = set()
                    for cd in codes:
                        if cd['Code'] == 'RU-main' or cd['Code'] == 'RU-Kaliningrad':
                            continue
                        if cd['Name'] == neighb['neighborLabel']:
                            temp.add(cd['Code'])
                    countries[code['Code']]['Neighbor'] = list(temp)
                    for i in list(temp):
                        if (i,code['Code']) not in adjlist:
                            adjlist.append((code['Code'],i))
    adjlist = list(set(adjlist))


    return countries, adjlist

def get_map_colors(neighbordict):
    G = gr.Graph(neighbordict)
    colors = ['yellow', 'lightgreen', 'cyan', 'orange']
    n = len(colors)
    stack = c.simplify(G, n)
    colormap = c.rebuild(G, stack, colors)
    colormap['RU-KALININGRAD'] = 'white'
    colormap['RU-MAIN'] = 'white'
    return colormap

def color_svg_map(colordict, infile=WHITEMAP_FILE, outfile=COLORMAP_FILE):
    tree = ET.parse(infile)
    root = tree.getroot()


    for path in root.iter("{http://www.w3.org/2000/svg}path"):

        country_code = path.get("id").upper()
        color = colordict.get(country_code)
        print(country_code, color)
        path.set("style", f"fill:{color}")

    tree.write(outfile)


def main():
    countries, adjlist = get_neighbors()
    country_color = get_map_colors(adjlist)
    color_svg_map(country_color)
if __name__ == "__main__":
    main()
