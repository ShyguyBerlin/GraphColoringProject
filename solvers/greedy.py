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