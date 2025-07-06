# 1.VL vom 25.4.2025

import networkx as nx
from random import shuffle

def greedy_no_sort( G : nx.graph):
    labels={}

    for node in G.nodes():
        used = {labels.get(neigh) for neigh in G.neighbors(node)}
        c=1
        while True:
            if c not in used:
                labels[node]= c
                break
            c+=1
        
        yield labels

def greedy_asc_deg( G : nx.graph):
    labels={}

    G_sorting =G.copy()
    sorting=[]
    for i in range(len(G)):
        deg=max([G_sorting.degree(n) for n in G_sorting.nodes()])
        nodes = list(G_sorting.nodes())
        shuffle(nodes)
        for node in nodes:
            if G_sorting.degree(node)==deg:
                sorting.append(node)
                G_sorting.remove_node(node)
                break
    sorting.reverse()

    for node in sorting:
        used = {labels.get(neigh) for neigh in G.neighbors(node)}
        c=1
        while True:
            if c not in used:
                labels[node]= c
                break
            c+=1
        
        yield labels

def greedy_desc_deg( G : nx.graph):
    labels={}

    G_sorting =G.copy()
    sorting=[]
    for i in range(len(G)):
        deg=min([G_sorting.degree(n) for n in G_sorting.nodes()])
        nodes = list(G_sorting.nodes())
        shuffle(nodes)
        for node in nodes:
            if G_sorting.degree(node)==deg:
                sorting.append(node)
                G_sorting.remove_node(node)
                break
    sorting.reverse()

    for node in sorting:
        used = {labels.get(neigh) for neigh in G.neighbors(node)}
        c=1
        while True:
            if c not in used:
                labels[node]= c
                break
            c+=1
        
        yield labels

def greedy_most_colors( G : nx.graph):
    labels={}

    G_remaining :list =list(G.nodes())

    while len(G_remaining)>0:
        most_colored_neigh_node = max(G_remaining, key=lambda x: len([neigh for neigh in G.neighbors(x) if neigh in labels.keys()]))
        used = [labels.get(neigh) for neigh in G.neighbors(most_colored_neigh_node)]
        c=1
        while True:
            if c not in used:
                labels[most_colored_neigh_node]= c
                break
            c+=1
        
        G_remaining.remove(most_colored_neigh_node)
        yield labels
    
    return

def greedy_color_swaps( G : nx.graph):
    for i in greedy_color_swaps_continue(G,{}):
        yield i

def try_swap(G : nx.Graph, labels :dict, nodes :list , new_color:int, blocked_nodes:list):
    # Node has color, change can be made
    if len(nodes)==0:
        return []
    
    if not nodes[-1] in labels.keys():
        return False
    
    for i in range(len(nodes)-1):
        if not nodes[i] in labels.keys():
            return False
        if labels[nodes[i]]!=labels[nodes[i+1]]:
            return False

    old_color=labels.get(nodes[0])
    if old_color == new_color:
        return []
    
    search=nodes

    # This should include all nodes touching the start node which either have the same color as the start node or new_color
    # Nodes which do not have a color label are ignored
    searched=[]

    while len(search)>0:
        n=search.pop()
        searched.append(n)

        neighs=G.neighbors(n)
        for i in neighs:

            # No color
            if not i in labels.keys():
                continue
            col= labels.get(i)

            # irrelevant color
            if not (col==old_color or col==new_color):
                continue

            if i in blocked_nodes:
                return None
            
            if not i in search and not i in searched:
                search.append(i)


    return searched  # Swap successful

def swap(labels:dict, keys_to_swap:list, valueA:int, valueB:int):
    """
    Swaps color labels valueA and valueB for the nodes in keys_to_swap.
    """
    if valueA == valueB:
        return

    for node in keys_to_swap:
        if node in labels:
            if labels[node] == valueA:
                labels[node] = valueB
            elif labels[node] == valueB:
                labels[node] = valueA

def greedy_color_swaps_continue(G :nx.Graph, labels :dict):
    
    labels={}

    G_sorting =G.copy()
    sorting=[]
    for i in range(len(G)):
        deg=min([G_sorting.degree(n) for n in G_sorting.nodes()])
        nodes = list(G_sorting.nodes())
        shuffle(nodes)
        for node in nodes:
            if G_sorting.degree(node)==deg:
                sorting.append(node)
                G_sorting.remove_node(node)
                break
    sorting.reverse()

    for node in sorting:
        neighs= {(labels.get(neigh),neigh) for neigh in G.neighbors(node)}
        used = [i[0] for i in neighs]
        c=1
        while True:
            if c not in used:
                labels[node]= c
                break
            c+=1
        
        could_swap=False
        for alt_col in range(1,c):
            for exg_col in range(alt_col+1,c):
                res=try_swap(G,labels,[i[1] for i in neighs if i[0]==alt_col],exg_col,[i[1] for i in neighs if i[0]==exg_col])
                if res!=None:
                    swap(labels,res,alt_col,exg_col)
                    could_swap=True
                    c=alt_col
                    break
            if could_swap:
                break
        
        labels[node]=c

        yield labels
    
    return

def greedy_color_swaps_and_elim_colors(G:nx.Graph):
    labels = {}
    coloramount = 1
    *_,labels = greedy_color_swaps(G)

    for node in G.nodes():
        if coloramount < labels[node]:
            coloramount = labels[node]

    labels = do_the_elim(G, labels, coloramount)
    yield labels


def elim_colors_basic(G: nx.Graph):
    labels={}
    coloramount = 1

    for node in G.nodes():
        labels[node] = coloramount
        coloramount+=1
    coloramount-=1

    labels = do_the_elim(G, labels, coloramount)
    yield labels

def greedy_elim_colors( G : nx.graph):
    labels={}
    coloramount = 1

    for node in G.nodes():
        used = {labels.get(neigh) for neigh in G.neighbors(node)}
        c=1
        while True:
            if c not in used:
                labels[node]= c
                if c > coloramount:
                    coloramount = c
                break
            c+=1
            
        
    labels = do_the_elim(G, labels, coloramount)
    yield labels

def do_the_elim(G:nx.Graph, labels, maxcolor):
    lasti = 1
    for i in range(1, maxcolor+1):
        labels, G, test = try_elim_color_simple(G, labels, i, maxcolor)
        if(test == 0):
            lasti = i
            break
    if(test == 0):
        for node in G.nodes():
            if(labels[node] == maxcolor):
                labels[node] = lasti
        labels = do_the_elim(G, labels, maxcolor-1)
    return labels

def try_elim_color_simple(G:nx.graph, labels, currcolor, maxcolor):
    fail = 0
    labelscopy = labels.copy()

    for node in G.nodes():
        if(labelscopy[node] == currcolor):
            used =  {labelscopy.get(neigh) for neigh in G.neighbors(node)}
            notused = list(range(1,maxcolor+1))
            notused.remove(currcolor)
            for i in range(1,maxcolor+1):
                if i in used:
                    if i in notused:
                        notused.remove(i)
            if len(notused) == 0:
                fail = 1
            else:
                labelscopy[node] = notused[0]
    if(fail == 1):
        return labels, G, 1
    else:
        #print("ELIMINATING COLOR,",currcolor,maxcolor,G.nodes,G.edges,labels,labelscopy)
        return labelscopy, G, 0

