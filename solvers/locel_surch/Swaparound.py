# -*- coding: utf-8 -*-
"""
Created on Sun Jul  6 11:32:25 2025

@author: Alice Mirror
"""

import networkx as nx
import color_to as ct

def swaparound(G : nx.graph, node : int()):
    
    if G.nodes[node]['used'] == False:
        
        colors = G.graph['colors']
        
        problemnode = False
        
        #print("node is")
        #print(node)    
    
        clist=[]
        for i in range(0,colors):              
            clist.append(0)
        
        #print(clist)
        
        for adj in G.adj[node]:
                    
            #print("adj is")
            #print(adj)
            #print(G.nodes[adj]['color'])
            #print(G.nodes[adj]['color']-1)
            clist.pop((G.nodes[adj]['color']-1))
            #print(clist)
            clist.insert(G.nodes[adj]['color']-1, 1)
            #print(clist)
                
        a0 = 0
        for i in clist:
            a0 = a0 + i
                
        #print("a0 is")              
        #print(a0)
                    
        if a0 >= colors-1:
            #print("is a problem node:")
            #print(node)
            problemnode = True
            
        if problemnode == True:
            
            oldcolor = G.nodes[node]['color']
            G.nodes[node]['used'] = True
            
            if G.nodes[node]['color'] +1 > colors:  
                G.nodes[node]['color'] = 1 
            else:
                G.nodes[node]['color'] = G.nodes[node]['color'] + 1
        
            for adj in G.adj[node]:
                G = ct.color_to(G, adj, G.nodes[node]['color'], oldcolor)
            
            for node1 in G.nodes:
                 G.nodes[node1]['used'] = False
            
            return G
            
        else:
            
            #print("is not a problemnode")
            #print(node)
            return G
    
    else:
        #print("was already used")
        #print(node)
        return G
        
        
        
        
    
