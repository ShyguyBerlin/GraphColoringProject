# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 16:52:17 2025

@author: Alice Mirror
"""

import networkx as nx

def recolor(G : nx.graph, pf : []): #pf is a list of prblemfree colors
    
    colors = G.graph['colors']

    for color in pf:
        
        for node in G.nodes:
        
            
            if G.nodes[node]['color'] == color: 
                #print("thinking about")
                #print(node)
                
                clist=[]
                for i in range(0,colors):              
                    clist.append(0)
                   
                for adj in G.adj[node]:
                    #print("adj is")
                    #print(adj)
                    clist.pop((G.nodes[adj]['color']-1))
                    clist.insert(G.nodes[adj]['color']-1, 1)
                    #print(clist)
                      
                for n in range(1,colors+1):
                    if clist[n-1] != 1 and n != G.nodes[node]['color']:
                        G.nodes[node]['color'] = n
                        #print("recolored:")
                        #print(node)
                        #print(G.nodes[node])

    #print(G.nodes.data())
    
    clist=[]
    for i in range(0,colors):              
        clist.append(0)
    
    for i in range(1, colors+1):
        for node0 in G.nodes:

            clist.pop((G.nodes[node0]['color']-1))
            clist.insert(G.nodes[node0]['color']-1, 1)
            
    
    #print(clist)
    
    unusedc = []
    usedc = []
    
    for i in range(0,colors):
        if clist[i] == 0:
           unusedc.append(i+1)
        else:
            usedc.append(i+1)
    
    #print("unused colores are")
    #print(unusedc)
    #print("used colores are")   
    #print(usedc)
    
    for i in unusedc:
        #print(i)  
        for node1 in G.nodes:
            if G.nodes[node1]['color'] > i:
                #print("thinking abourt")
                #print(node1)
                #print(G.nodes[node1]['color'])
                G.nodes[node1]['color'] = G.nodes[node1]['color'] -1
                #print(G.nodes[node1]['color'])
       
    G.graph['colors'] = G.graph['colors'] - len(unusedc) 
        
    return G