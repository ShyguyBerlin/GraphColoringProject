# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 19:00:39 2025

@author: Alice Mirror
"""

import networkx as nx

def check(G : nx.graph):

    color = 1
    
    problemC = []
    problemfree = []
    colors = G.graph['colors']
    
    for color in range(1, colors+1):
        #print("checking color")
        #print(color)
        problemfree.append(color)         
       
        
        for node in G.nodes:
           
           if G.nodes[node]['color'] == color:
           
                #print("checking node")
                #print(node)
                #print("with color")
                #print(G.nodes[node]['color'])
                #print(color)
                
                clist = []
                
                for i in range(0,colors):              
                    clist.append(0)
                
                #print(clist)
                
                for adj in G.adj[node]:
                    #print("adj is")
                    #print(adj)
                    #print(G.nodes[adj]['color']-1)
                    clist.pop((G.nodes[adj]['color']-1))
                    clist.insert(G.nodes[adj]['color']-1, 1)
                    #print(clist)
                
                a0 = 0
                for i in clist:
                    a0 = a0 + i
                
                #print("a0 is")              
                #print(a0)
                    
                if a0 == colors-1:
                    #print("is a problem node")
                    #print(node)
                    problemC.append(color)                    
                    problemfree.remove(color)
                    break
                    
                #print(problemC)
                #print(problemfree)
                
    return problemfree