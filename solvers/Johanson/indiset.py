# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 17:47:54 2025

@author: Alice Mirror
"""

import networkx as nx

def indiset (G : nx.graph):
    
    indi = []
    ajd = []
    runs = 0
    
    for node in G.nodes():
        control = 0
        #print(node)
        for i in ajd:
            #print(i)
            if (i == node):
                control = 1
        #print(control)
        if (control == 0):
            ajd = ajd + list(G.adj[node])
            indi = indi + [node]
            #print(node)
        runs = runs +1  
   
    #print(indi)
    #print(runs)
    return indi