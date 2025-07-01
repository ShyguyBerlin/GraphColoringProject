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

def berger_rompel(G : nx.Graph):
    labels={}
    
    uncolored = list(G.nodes())

    if not "chromatic-number" in G.graph.keys():
        print("ERROR: berger_rompel needs the property \"chromatic-number\", try not to run this solver if you do not have it.")
        exit(1)

    k=G.graph["chromatic-number"]

    if k>sqrt(G.order()):
        # Color all uncolored with a new color
        # 1
        taken=0
        if len(labels.values())>0:
            taken = max(labels.values())
        for i in uncolored:
            taken+=1
            labels[i]=taken
        yield labels
        return

    m = floor(log(G.order(),k)) # 2
    color = 1 # 3
    print("m is",m)
    while len(uncolored)>=m*k: # 4
        U:list=uncolored.copy() # 1
        shuffle(U)
        while len(U)>=k*m: # 2
            print("\nuncolored:",len(uncolored),uncolored)
            print("U:",len(U),U)
            partitions=[] # 1
            while len(U)>(len(partitions)+1)*k*m:
                partitions.append(G.subgraph(U[len(partitions)*k*m:(len(partitions)+1)*k*m]))
            partitions.append(G.subgraph(U[len(partitions)*k*m:]))
            print("partitions: ",len(partitions))
            for i in partitions: # 2
                i :nx.Graph = i
                done=False
                for X in all_independent_sets(i):
                    if len(X)==m:
                        neighborhood :set=set()
                        Ugraph : nx.Graph=G.subgraph(U)
                        for n in X:
                            neighborhood |= set(Ugraph.neighbors(n))
                        neighborhood |= set(X)
                        if len(neighborhood)<=len(U)-len(U)/k:
                            print("found iset,",X)
                            # 3
                            # found good subset
                            for n in X:
                                labels[n]=color
                                uncolored.remove(n)
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