# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 17:08:14 2025

@author: Alice Mirror
"""
import networkx as nx
import indiset as iset

def johnson(G : nx.graph):
 
    colors = 0
    surching = 1

    

    while(surching == 1):
        indi = iset.indiset(G)
        G.remove_nodes_from(indi)
        colors = colors + 1
        if (G.number_of_nodes() == 0):
            surching = 0
    
    return colors
