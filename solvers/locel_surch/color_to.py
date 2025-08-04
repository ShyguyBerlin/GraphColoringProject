# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 17:16:51 2025

@author: Alice Mirror
"""

import networkx as nx

def color_to(G : nx.graph, node : int(), colorfrom : int(), colorto : int()):
    
    G = G
    
    if G.nodes[node]['color'] == colorfrom and G.nodes[node]['used'] != True:
        #print("nightbor is")
        #print(node)
        #print("changing color from")
        #print(G.nodes[node]['color'])
        G.nodes[node]['used'] = True
        G.nodes[node]['color'] = colorto
        #print("to")
        #print(G.nodes[node]['color'])
        
        for adj in G.adj[node]:
            
            G = color_to(G, adj, G.nodes[node]['color'], colorfrom)
        
        #print(G.graph)
        #print(G.nodes.data())
        
    return G
        