
from hypothesis import given, strategies
import unittest


import graphs as g



def equal(self, edges1, edges2):
    return self.assertSetEqual(edges1, edges2) 

smallints = strategies.integers(min_value=0, max_value=10)

weights_random = strategies.floats(min_value=10, max_value=50)

twoints = strategies.tuples(smallints, smallints)

edges_with_weight = strategies.tuples(twoints, weights_random)

edge_list_with_weight = strategies.lists(edges_with_weight, unique_by=(lambda x: x[0][0], lambda x: x[0][1]))

@given(edge_list_with_weight)
def test(edges_with_weight):
    eds = list()
    weights = list()
    for entry in edges_with_weight:
        eds.append(entry[0])
        weights.append(entry[1])
    G = g.WeightedGraph(eds)
    
    for a, b in eds:
        assert a in G.vertices() and b in G.vertices()
        assert (a, b) in G.edges() or (b, a) in G.edges()
    
    for (a, b) in G.edges():
        assert a in G.vertices() and b in G.vertices()
    
    for v in G.vertices():
        for neighbor in G.neighbors(v):
            assert v in G.neighbors(neighbor)
    



if __name__ == '__main__':
    test()