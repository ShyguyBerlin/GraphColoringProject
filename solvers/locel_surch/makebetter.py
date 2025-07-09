# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 18:50:50 2025

@author: Alice Mirror
"""

import networkx as nx
import check_colors as cc
import recolor as rc
import Swaparound as sr

def makebetter(G : nx.graph):
    
    
    #check a colors without problemetic nodes
    problemfree = cc.check(G)
    
    #print("are problemfree:")
    #print(problemfree)
    
    #G1 = nx.Graph()
    
    if len(problemfree) != 0:
        #print("recoloring")
        G = rc.recolor(G, problemfree)
    
    
    for color in range(1,G.graph['colors']):
        for node in G.nodes:
            if G.nodes[node]['color'] == color:
                G = sr.swaparound(G,node)
                
                problemfree = cc.check(G)
                
                if len(problemfree) != 0:
                    #print("recoloring")
                    G = rc.recolor(G, problemfree)
        
        for node1 in G.nodes:
             G.nodes[node1]['used'] = False
            
    return G
    
    
    
    
    