# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 13:38:24 2025

@author: Alice Mirror
"""

import networkx as nx
import makebetter as mb

def make_better_coloring(G : nx.graph, coloring : dict()):
    
    G1 = nx.Graph(colors = 0)
    
    #print(G.nodes)
    
    G1.add_nodes_from(G.nodes, color = 0, used = False)
    G1.add_edges_from(G.edges)
    
    #print(G1.graph)
    #print(G1.nodes.data())
    
    highestcolor = 1
    
    for node in G.nodes:
        G1.nodes[node]['color'] = coloring[node]
        
        
        #print(coloring[node])
        #print(highestcolor)
        
        if coloring[node] > highestcolor:
            highestcolor = coloring[node]
            #print("new highest color is")
            #print(highestcolor)
    
    G1.graph['colors'] = highestcolor
      
    #print(G1.graph)
    #print(G1.nodes.data())
    
    G1 = mb.makebetter(G1)
    
    #print(G1.graph)
    #print(G1.nodes.data())
    
    #G2 = nx.Graph
    #G2.add_nodes_from(G1.nodes)
    #G2.add_edges_from(G1.edges)
    
    newcoloring = {}
    
    for node in G1.nodes:
        newcoloring[node] = G1.nodes[node]['color']
        #print(newcoloring)
    
    return newcoloring