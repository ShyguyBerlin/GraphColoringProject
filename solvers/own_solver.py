# I thought of a cheesy way to calculate k exactly with some optimizations
# let's see how efficient/fast it is

import networkx as nx
from random import shuffle,random
import math
from functools import cache
from heapq import *
from .wigderson import check_complete

# We shall use nodes to index a subgraph in each function as we make a lot of modifications and it should be faster to make the subgraph instead of copying and editing the whole graph
# This is an assumption I made without any proof

def generate_independent_sets(G : nx.Graph, nodes):
    if len(nodes)==0:
        yield []
        return
    pivot=nodes[0]
    for i in generate_independent_sets(G,nodes[1:]):
        yield i
    nodes2=[]
    edges=list(G.edges())
    for o in nodes[1:]:
        if not ((pivot,o) in edges or (o,pivot) in edges):
            nodes2.append(o)
    
    for i in generate_independent_sets(G,nodes2):
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
        for i in generate_independent_sets(G, inst[3]):
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

def simulated_solver(G : nx.Graph):
    
    phase=0 # 0 := EDGES, 1 := NODES

    labels={N:1 for N in list(G.nodes())}

    r=0.9
    stepsize=(r/10)/math.log(G.order())
    while r>0 or not check_complete(G,labels):
        match phase:
            case 0:
                for (u,v) in list(G.edges()):
                    if labels[u]==labels[v]:
                        n=0
                        if random()<(G.degree(u)+r)/(G.degree(v)+G.degree(u)+2*r):
                            n=u
                        else:
                            n=v
                        neighs=list(G.neighbors(n))
                        color=0
                        used=True
                        while used:
                            color+=1
                            used=False
                            for i in neighs:
                                if labels[i]==color:
                                    used=True
                                    break
                        labels[n]=color

                if r>0:
                    phase=1
            case 1:
                for i in list(G.nodes()):
                    if labels[i]>1 and random()<r/2:
                        labels[i]-=1
                phase=0
        
        r-=stepsize
        #if r<=0.1:
        #    stepsize*=0.5
        if r<0:
            r=0
        
        yield labels