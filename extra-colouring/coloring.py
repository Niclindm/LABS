import json
import graphviz
import matplotlib
import sys
sys.path.append('/LABS/LAB2/')
import graphs as gr

def simpify(graph, n=4):
    pass

def rebuild(graph, stack, colors):
    pass

def viz_color_graph(source, colors):
    pass


def demo():
    G = gr.Graph([(1,2),(1,3),(1,4),(3,4),(3,5),(3,6), (3,7), (6,7)])
    print(G)
    viz_color_graph(G,['red', 'green', 'blue'])

if __name__ == '__main__':
    demo()