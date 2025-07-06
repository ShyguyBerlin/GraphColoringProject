# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 17:08:14 2025

@author: Alice Mirror
"""
import networkx as nx
import solvers.Johanson.indiset as iset

def johnson(G : nx.Graph):
 
    G=G.copy()

    labels={}
    colors = 1
    surching = 1

    

    while(surching == 1):
        indi = iset.indiset(G)
        G.remove_nodes_from(indi)
        for i in indi:
            labels[i]=colors
        colors = colors + 1
        if (G.number_of_nodes() == 0):
            surching = 0
        yield labels
    yield labels

# Same as johnson, but indipendent set does not regard the node degrees
def johnson_naive(G : nx.Graph):
 
    G=G.copy()

    labels={}
    colors = 1
    surching = 1

    

    while(surching == 1):
        indi = iset.indiset_naive(G)
        G.remove_nodes_from(indi)
        for i in indi:
            labels[i]=colors
        colors = colors + 1
        if (G.number_of_nodes() == 0):
            surching = 0
        yield labels
    yield labels
