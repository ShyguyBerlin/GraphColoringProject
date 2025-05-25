# 3.VL vom 9.5.2025

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
        labels[i]=1

    nodes=list(G.nodes())

    while not check_complete(G,labels):
        yield labels
        a=0
        while True:
            # Increase color for node a by 1, if it is equal to lim, decrease to 0 and increase next node. If all node wrap, increase lim
            labels[nodes[a]] += 1
            if labels[nodes[a]] > lim:
                labels[nodes[a]] = 0
                a+=1
                if a==len(nodes):
                    lim+=1
                    break
                continue
            break
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

# this only works for 3-colorable graphs
# I have made a small adjustment that should fix this requirement
def wigdersons_first( G : nx.Graph):
    labels={}

    G=G.copy() # 1

    i = 0 # 2
    while G.order()>0 and max([G.degree(n) for n in G.nodes()])>=math.sqrt(G.order()): # 3
        n = max(G.nodes(),key=lambda x: G.degree(x))    # 1
        *_,col = greedy_desc_deg(G.subgraph(G.neighbors(n))) # 2
        for neigh in col:
            labels[neigh]=col[neigh]+i

        used_colors = max(col.values())+1 # adjustment to work for any k
        labels[n]=i+used_colors # 3 (adjusted)

        i+= used_colors # 4 (adjusted)

        G.remove_nodes_from(list(G.neighbors(n))) # 5
        G.remove_node(n) # 5
        yield labels
    
    for res in greedy_desc_deg(G):
        for label in res:
            labels[label]=res[label]+i
        yield labels

# Again, this is a modified version, because we do not know the actual k
# We try to guess k, but in the end it does not make a big difference
def wigdersons_second( G : nx.Graph):
    for i in __wigdersons_second(G):
        yield i
    
    return

def __wigdersons_second(G :nx.Graph):
    labels={}
    G=G.copy()

    def fk(n):
        if(n<=4):
            return 1
        k=math.log(n) # arbitrary
        return math.ceil(n**(1-1/(k-1)))

    col=0

    while G.order()>0:
        n = max(G.nodes(), key=lambda x: G.degree(x)) # 1
        if G.degree(n) < fk(G.order()):
            # If the highest degree of the graph is less than fk, we can stop
            break
        neighs=list(G.neighbors(n))
        if len(neighs)>0:
            *_, res = __wigdersons_second(G.subgraph(neighs)) # 2
        else:
            res={}
        max_col=max(res.values())
        if len(res.values())==0:
            max_col=0
        labels[n]=max_col+col+1 # 3
        for i in res:
            labels[i]=res[i]+col
        col+=max_col # 4
        
        removes=list(G.neighbors(n)) # 5
        removes.append(n)
        G.remove_nodes_from(removes)
        yield labels

    if G.order()==0:
        return

    *_,rem_lab = greedy_desc_deg(G)
    for i in rem_lab:
        labels[i]=rem_lab[i]+col
        yield labels