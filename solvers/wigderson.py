import networkx as nx
from random import shuffle
import math
from solvers.greedy import greedy_desc_deg

# These algorithms should only be used with 3-colorable graphs I guess

def check_complete(G : nx.graph, labels: dict):
    for i in G.edges():
        c1= labels.get(i[0],-1)
        c2= labels.get(i[1],-1)
        if c1 == -1 or c2 == -1 or c1==c2:
            return False
    return True

def brute_force(G : nx.graph, min_col: int = 1):
    labels={}
    lim=min_col
    #init brute force
    for i in G.nodes():
        labels[i]=0

    nodes=list(G.nodes())

    while not check_complete(G,labels):
        yield labels
        a=0
        while True:
            # Increase color for node a by 1, if it is equal to lim, decrease to 0 and increase next node. If all node wrap, increase lim
            labels[nodes[a]] += 1
            if labels[nodes[a]] == lim:
                labels[nodes[a]] = 0
                a+=1
                if a==len(nodes):
                    lim+=1
                    break
                continue
            break
        print("I am yielding",labels)
    yield labels




def so_called_easy_algorithm(G : nx.Graph):
    nodes=list(G.nodes())
    part_size=round(math.log(len(nodes)))
    shuffle(nodes)

    labels={}
    offset=0

    while len(nodes)>0:
        subg = G.subgraph(nodes[0:min(part_size,len(nodes))])
        nodes=nodes[min(part_size,len(nodes)):]
        
        *_,lab = brute_force(subg)
        for i in lab.keys():
            labels[i]=lab[i]+offset
        offset+=max(lab.values())+1
        yield labels

def wigdersons_first( G : nx.Graph):
    labels={}


    i = 1

    while max([G.degree(n) for n in G.nodes()])>=math.sqrt(G.order()):
        n = max(G.nodes(),key=lambda x: G.degree(x))
        c=1
        while True:
            if c not in used:
                labels[node]= c
                break
            c+=1
        
        yield labels
    
    # I do not want to implement a minimum color for greedy, theoretically we should continue with i from here, but I do not think it makes a difference
    for l in greedy_desc_deg(G):
        yield l