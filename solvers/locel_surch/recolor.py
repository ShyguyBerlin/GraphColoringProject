# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 16:52:17 2025

@author: Alice Mirror
"""

import networkx as nx

def recolor(G : nx.graph, pf : list): #pf is a list of prblemfree colors
    #pf=[pf[0]]
    colors = G.graph['colors']

    for color in pf:
        
        for node in G.nodes:
        
            
            if G.nodes[node]['color'] == color: 
                
                clist=[]
                for i in range(0,colors):              
                    clist.append(0)
                   
                for adj in G.adj[node]:
                    clist.pop((G.nodes[adj]['color']-1))
                    clist.insert(G.nodes[adj]['color']-1, 1)
                      
                for n in range(1,colors+1):
                    if clist[n-1] != 1 and n != G.nodes[node]['color']:
                        G.nodes[node]['color'] = n

    clist=[]
    for i in range(0,colors):              
        clist.append(0)
    
    for i in range(1, colors+1):
        for node0 in G.nodes:

            clist.pop((G.nodes[node0]['color']-1))
            clist.insert(G.nodes[node0]['color']-1, 1)
            
    
    #print(clist)
    
    unusedc = []
    unusedcounter=0
    usedc = []
    # Map each color to itself
    mapping= {x:x for x in range(1,colors+1)}

    for i in range(0,colors):
        if clist[i] == 0:
           unusedc.append(i+1)
        else:
            usedc.append(i+1)

    if len(unusedc)==0:
        return G

    # Look at used colors from highest to lowest
#    usedc.reverse()
    for i in usedc:
        # If there is a lower unused color, map to it instead
        if True:#i>unusedc[unusedcounter]:
            mapping[i]=unusedc[unusedcounter]
            # other colors should be remapped to the next highest unused color
            unusedcounter+=1
            #
            unusedc.append(i)
        else:
            # If the current unused color is higher than the current used color, 
            # there won't be any eligible colors to remap in the future, 
            # just stop then
            break

    for i in G.nodes:
        G.nodes[i]['color']=mapping[G.nodes[i]['color']]

    return G
