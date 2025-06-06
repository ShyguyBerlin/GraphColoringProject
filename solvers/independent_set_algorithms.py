# 3. Paket an Algorithmen

import networkx as nx
from random import shuffle
from math import sqrt,log,floor

def all_independent_sets(G):
    nodes = list(G.nodes)
    
    def backtrack(current_set, remaining_nodes):
        if not remaining_nodes:
            yield set(current_set)
            return
        
        v = remaining_nodes[0]
        rest = remaining_nodes[1:]
        
        # Exclude v
        yield from backtrack(current_set, rest)

        # Include v only if none of its neighbors are in current_set
        if all(neigh not in current_set for neigh in G.neighbors(v)):
            yield from backtrack(current_set | {v}, rest)

    yield from backtrack(set(), nodes)

def berger_rompel(G : nx.Graph, k:int=4):
    labels={}
    
    uncolored = list(G.nodes())

    
    if k>sqrt(G.order()):
        # Color all uncolored with a new color
        # 1
        taken=0
        if len(labels.values())>0:
            taken = max(labels.values())
        for i in uncolored:
            taken+=1
            labels[i]=taken

    m = floor(log(G.order(),k)) # 2
    color = 1 # 3
    print("m is",m)
    while len(uncolored)>=m*k: # 4
        U:list=uncolored.copy() # 1
        shuffle(U)
        while len(U)>=k*m: # 2
            print("\nuncolored:",uncolored)
            print("U:",U)
            partitions=[]
            while len(U)>(len(partitions)+1)*k*m:
                partitions.append(G.subgraph(U[len(partitions)*k*m:(len(partitions)+1)*k*m]))
            partitions.append(G.subgraph(U[len(partitions)*k*m:]))

            for i in partitions:
                i :nx.Graph = i
                done=False
                for X in all_independent_sets(i):
                    if len(X)>=m:
                        neighborhood :set=set()
                        Ugraph : nx.Graph=G.subgraph(U)
                        for n in X:
                            neighborhood |= set(Ugraph.neighbors(n))
                        if len(neighborhood)<=len(U)-len(U)/k:
                            print("found iset,",X)
                            # 3
                            # found good subset
                            for n in X:
                                labels[n]=color
                                uncolored.remove(n)
                            neighborhood |= set(X)
                            for n in neighborhood:
                                U.remove(n)
                            done=True
                            found=1
                            break
                if done:
                    break

        print("EEP")
        color+=1 # 3
        yield labels

    # Color all uncolored with a new color
    # 5
    if k>sqrt(G.order()):
        uncolored= [i for i in G.nodes() if not i in labels.keys()]
        taken=0
        if len(labels.values())>0:
            taken = max(labels.values())
        for i in uncolored:
            taken+=1
            labels[i]=taken
    yield labels