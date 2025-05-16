# I thought of a cheesy way to calculate k exactly with some optimizations
# let's see how efficient/fast it is

import networkx as nx
from random import shuffle
import math
from functools import cache
from heapq import *
from solvers.wigderson import check_complete

# We shall use nodes to index a subgraph in each function as we make a lot of modifications and it should be faster to make the subgraph instead of copying and editing the whole graph
# This is an assumption I made without any proof

@cache
def generate_independent_sets(G : nx.Graph, nodes):
    nodes=list(nodes)
    if len(nodes)==0:
        yield []
        return
    pivot=nodes[0]
    for i in generate_independent_sets(G,tuple(nodes[1:])):
        yield i
    nodes2=[]
    edges=list(G.edges())
    for o in nodes[1:]:
        if not ((pivot,o) in edges or (o,pivot) in edges):
            nodes2.append(o)
    
    for i in generate_independent_sets(G,tuple(nodes2)):
        yield [pivot]+i

# This estimates the coloring number, but if it is wrong, it will output a SMALLER number
def estimate_coloring_number(G : nx.Graph, nodes) -> int:
    sub = G.subgraph(nodes)
    return len(nx.approximation.max_clique(sub))

def a_star_solver(G : nx.Graph):
    c=1
    # (Estimated Coloring number, Steps in, Nodes uncolored, Colors assigned)
    heap = [(0,0,0,list(G.nodes()),{})]
    while len(heap)>0:
        inst = heappop(heap)
        if check_complete(G,inst[4]):
            print(inst)
            yield inst[4]
            return
        for i in generate_independent_sets(G, tuple(inst[3])):
            new_nodes=[x for x in inst[3] if not x in i]
            labels=inst[4].copy()
            for n in i:
                labels[n]=inst[1]+1
            est_cost=inst[1]+1+estimate_coloring_number(G,new_nodes)
            heappush(heap,(est_cost,inst[1]+1,c,new_nodes,labels))
            c+=1
        print(inst, len(heap))
        yield inst[4]
    return {}