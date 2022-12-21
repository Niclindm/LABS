# visualization of shortest path in Lab 3, modified to work with Django

from .trams import readTramNetwork
from .graphs import dijkstra
from .color_tram_svg import color_svg_network
import os
from django.conf import settings

def show_shortest(dep, dest):
    # TODO: uncomment this when it works with your own code
    network = readTramNetwork()
    # print(network)
    # network = specialize_stops_to_lines(network)
    # print(network)

    # TODO: replace this mock-up with actual computation using dijkstra.
    # First you need to calculate the shortest and quickest paths, by using appropriate
    # cost functions in dijkstra().
    # Then you just need to use the lists of stops returned by dijkstra()
    #
    # If you do Bonus 1, you could also tell which tram lines you use and where changes
    # happen. But since this was not mentioned in lab3.md, it is not compulsory.
    quickest = dijkstra(network, dep, cost=lambda u,v: network.get_weight(u,v))
    time = quickest[dest]['dist']

    shortest = dijkstra(network, dep, cost=lambda u,v: network.geo_distance(u,v))
    dist=shortest[dest]['dist']


    
    timepath = 'Quickest: ' + ', '.join(quickest[dest]['path']) + f', {time} minutes'
    geopath = 'Shortest: ' + ', '.join(shortest[dest]['path']) + f', {dist} km'

    def colors(v):
        if v in shortest[dest]['path'] and v in quickest[dest]['path']: 
            return 'cyan'
        elif v in quickest[dest]['path']: 
            return 'orange'
        elif v in shortest[dest]['path']:
            return 'lightgreen'
        else:
            return 'white'
            

    # this part should be left as it is:
    # change the SVG image with your shortest path colors
    color_svg_network(colormap=colors)
    # return the path texts to be shown in the web page
    return timepath, geopath