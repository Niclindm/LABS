from math import inf
import sys

import graphviz


class Graph:
    def __init__(self, edgelist=None): #a edgelist of form (veterx1, vertex2)
        self._adjlist = {}
        self._valuelist = {}
        if edgelist:
            for items in edgelist:
                self.add_vertex(items[0])
                self.add_vertex(items[1])
                if items not in self.edges():
                    self.add_edge(items[0],items[1])




    def __len__(self):
        return len(self._adjlist.keys())



    def add_edge(self, a, b):

        self.add_vertex(a)
        self.add_vertex(b)
        self._adjlist[a][b] = dict()
        self._adjlist[b][a] = dict()


    def add_vertex(self, a):
        if a not in self._adjlist:
            self._adjlist.update({a : {}}) 
            self._valuelist.update({a: {}})

        
    def edges(self):
        eds = []
        for a in self._adjlist.keys():
            for b in self._adjlist[a]:
                if a <= b:
                    eds.append((a, b))
        return eds

    def get_vertex_value(self, v):
        return self._valuelist[v]

    def neighbors(self, v):
        neighbor_list = []
        for value in self._adjlist[v]:
            neighbor_list.append(value)
        return neighbor_list

    def remove_edge(self, a, b):
        for keys in self._adjlist.keys():
            if a == keys or b == keys:
                for item in list(self._adjlist[keys]):
                    if a == item or b == item:
                        self._adjlist[keys].remove(item)


    def remove_vertex(self, v):
        if v in self._adjlist:
            self._adjlist.pop(v, None)
        if v in self._valuelist:
            self._valuelist.pop(v, None)
#        for keys in self._adjlist.keys():
#            for item in list(self._adjlist[keys]):
#                if v == item:
#                    self._adjlist[keys].remove(item)
#                    self._valuelist[keys].remove(item)

        

    def set_vertex_value(self, v, x):
        self._valuelist[v] = {x}

    def vertices(self):
        "Lists all vertices."
        return list(self._adjlist.keys())
        
    def __str__(self):
        return str(self._adjlist)

class WeightedGraph(Graph):

    def __init__(self, start=None):
        super().__init__(start)
        if start:
            self._weightedlist = {(a,b) : None for a,b in start}
        else:
            self._weightedlist = {}

    def get_weight(self, a, b):
        return self._weightedlist[(a,b)]

    def set_weight(self, a, b, w):
        if (a,b) in self._weightedlist.keys():
            self._weightedlist[a,b] = w
        elif (b,a) in self._weightedlist.keys():
            self._weightedlist[b,a] = w
        elif (a, b) in self.edges() or (b,a) in self.edges():
            self._weightedlist[(a,b)] = w


    def __str__(self):
        return str(self._weightedlist)

def costs2attributes(G, cost, attr='weight'):
    for a, b in G.edges():
        G[a][b][attr] = cost(a, b)



def dijkstra(graph, source, cost=lambda u,v: WeightedGraph.get_weight(u,v)):
    q = []
    prev = {}
    dist = {}
    for v in graph.vertices():
        dist[v] = 9999999
        prev[v] = []
        q.append(v)
    dist[source] = 0


    while q:
        temp = 99999999
        for i in q: 
            if dist[i] < temp:
                temp = dist[i]
                u = i
        q.remove(u)

        for neighbor in graph.neighbors(u):
            if neighbor in q:
                alt = dist[u] + cost(u, neighbor)
                if alt < dist[neighbor]:
                    dist[neighbor] = alt
                    prev[neighbor] = u
    
    path = dict()
    for vertex in graph.vertices():
        if vertex != source:
            p = True
            v = vertex
            path_list = list()
            while v != source:
                if v in prev:
                    path_list.append(v)
                    v = prev[v]
                else:
                    p = False
                    break
            if p:
                path_list.append(source)
                path_list.reverse()
                path[vertex] = path_list

    final_dict = {vertex: {'dist': dist[vertex], 'path': path[vertex]} for vertex in graph.vertices() if vertex != source} 
    return final_dict

                




def visualize(graph, view='dot', name='mygraph', colors=None):
    dot = graphviz.Graph(engine='fdp', graph_attr={'size': '12,12'})

    for v in graph.vertices():
        if colors:
            try:
                col = colors(v)
            except TypeError:
                col = colors[v]
        else:
            col = 'white'
        dot.node(
            str(v),
            label=str(v),
            shape='rectangle',
            fontsize='16pt',
            width='0.8',
            height='0.10',
            fillcolor=col, style='filled',
            )
        

    for (a,b) in graph.edges():
        dot.edge(str(a),str(b))
    dot.render('mygraph.gv', view=True)

def view_shortest(G, source, target, cost=lambda u,v: 1):
    path = dijkstra(G, source, cost)[target]['path']
    dist = dijkstra(G, source, cost)[target]['dist']
    print(f"\n Travel takes: {dist} mins trough the shortest path: {path}\n")
    # colormap = {str(v): 'orange' for v in path}
    colors = lambda stop: 'orange' if stop in path else 'white'

    visualize(G, view='view', colors=colors)


    

def demo():
    # G = Graph([(1,2),(1,3),(1,4),(3,4),(3,5),(3,6), (3,7), (6,7)])
    # visualize(G)

    G = WeightedGraph([(1,2),(1,3),(1,4),(3,4),(3,5),(3,6), (3,7), (6,7)])
    # G.set_weight(1,3,4)
    view_shortest(G, 2, 6)
if __name__ == '__main__':
    demo()
