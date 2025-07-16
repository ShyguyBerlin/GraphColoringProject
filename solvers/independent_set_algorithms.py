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

        # Remove all neighbors of v but add v
        rem:list= remaining_nodes[1:].copy()
        for i in G.neighbors(v):
            if i>v and i in rem:
                rem.remove(i)

        yield from backtrack(current_set | {v}, rem)

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
    #print("m is",m)
    while len(uncolored)>=m*k: # 4
        U:list=uncolored.copy() # 1
        shuffle(U)
        while len(U)>=k*m: # 2
            #print("\nuncolored:",len(uncolored),uncolored)
            #print("U:",len(U),U)
            partitions=[] # 1
            while len(U)>(len(partitions)+2)*k*m:
                partitions.append(G.subgraph(U[len(partitions)*k*m:(len(partitions)+1)*k*m]))
            partitions.append(G.subgraph(U[len(partitions)*k*m:]))
            #print("partitions: ",len(partitions))
            #print("looking for iset of size",m)
            for i in partitions: # 2
                i :nx.Graph = i
                #print("partition")
                #print(list(i.nodes()),list(i.edges()))
                done=False
                for X in all_independent_sets(i):
                    if len(X)==m:
                        #print("Iset good")
                        neighborhood :set=set()
                        Ugraph : nx.Graph=G.subgraph(U)
                        for n in X:
                            neighborhood |= set(Ugraph.neighbors(n))
                        if len(neighborhood)<=len(U)-len(U)/k:
                            neighborhood |= set(X)
                            #print("found iset,",X)
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
                        #print("neighborhood too smol")
                if done:
                    break

        #print("EEP")
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

#"Test","johnson","tests/input/250_8cn_250n_35d.gsm",0,250,250,250.0,250,0.3075,0.3075,0.3075,0.3075,23.1264,51.6251,38.8428,39.3422,25.0,33.0,29.904,30.0
#"Test","johnson","tests/input/250_8cn_250n_70d.gsm",0,250,250,250.0,250,0.6149,0.6149,0.6149,0.6149,43.605,99.6086,72.3014,72.6353,12.0,44.0,24.6,24.0
#"Test","berger_rompel, X>=m","tests/input/250_8cn_250n_35d.gsm",0,250,250,250.0,250,0.3075,0.3075,0.3075,0.3075,299.0658,683.8709,565.942,601.6281,41.0,47.0,43.728,44.0
#"Test","berger_rompel, X>=m","tests/input/250_8cn_250n_70d.gsm",0,250,250,250.0,250,0.6149,0.6149,0.6149,0.6149,455.1391,807.6338,685.0964,707.2383,65.0,81.0,73.684,74.0