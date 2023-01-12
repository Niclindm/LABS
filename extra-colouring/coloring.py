import json
import matplotlib
import graphviz
import sys
sys.path.append('LAB2')
import graphs as gr

def simplify(graph, n=4):
    stack = list()
    while graph.vertices():
        for v in graph.vertices():
            neighbors = graph.neighbors(v)
            if len(neighbors) < n:
                stack.append((v, neighbors))
                graph.remove_vertex(v)
                for neighb in neighbors:
                    graph.remove_edge(v,neighb)
    return reversed(stack)


def rebuild(graph, stack, colors):
    colormap = dict()
    for v, neighbors in stack:
        print(v)
        print(neighbors)
        n = len(colors) - 1
        graph.add_vertex(str(v))

        for nb in neighbors:
            graph.add_edge(str(v), str(nb))

        color = colors[n]
        neighbor_color = []

        for neighbor in graph.neighbors(str(v)):
            if neighbor in colormap:
                neighbor_color.append(colormap[neighbor])
        while color in neighbor_color:
            n -= 1
            color = colors[n]
        colormap[str(v)] = color

    return colormap

def viz_color_graph(source, colors):
    n = len(colors)
    stack = simplify(source, n)
    print(stack)
    colormap = rebuild(source, stack, colors)
    gr.visualize(source, colors=colormap)


def demo():
    G = gr.Graph([(1,2),(1,3),(1,4),(3,4),(3,5),(3,6), (3,7), (6,7)])
    viz_color_graph(G,['red', 'green', 'blue'])

if __name__ == '__main__':
    demo()
