import networkx as nx
import random

from .greedy import greedy_desc_deg

def partition(G : nx.Graph):
    pass

def flow_cut_edge(G : nx.Graph):
    """
    Partition graph using Dijkstra-based approach for better performance.
    Picks 2 random nodes, runs Dijkstra from each, assigns nodes to closest center.
    Much faster than Kernighan-Lin: O((n+m)log n) vs O(n³)
    """
    nodes = list(G.nodes())
    if len(nodes) < 2:
        # Handle edge case: graph too small to partition
        return ([G.copy()], [])

    # Pick 2 random centers
    center1, center2 = random.sample(nodes, 2)

    # Run Dijkstra from both centers
    try:
        dist1 = nx.single_source_dijkstra_path_length(G, center1)
        dist2 = nx.single_source_dijkstra_path_length(G, center2)
    except nx.NetworkXError:
        # Handle disconnected components - fall back to simple split
        mid = len(nodes) // 2
        S1, S2 = set(nodes[:mid]), set(nodes[mid:])
        print("MEEEEEP")
        return ([G.subgraph(S1).copy(), G.subgraph(S2).copy()], [])

    # Assign nodes to closest center (random tie-breaking)
    S1, S2 = set(), set()
    for node in nodes:
        d1 = dist1.get(node, float('inf'))
        d2 = dist2.get(node, float('inf'))

        if d1 < d2:
            S1.add(node)
        elif d2 < d1:
            S2.add(node)
        else:
            # Tie-breaking: assign randomly
            if random.random() < 0.5:
                S1.add(node)
            else:
                S2.add(node)

    # Ensure both partitions are non-empty
    if len(S1) == 0:
        S1.add(S2.pop())
    elif len(S2) == 0:
        S2.add(S1.pop())

    # Calculate cut edges
    cut_edges = [
        (u, v) for u, v in G.edges()
        if (u in S1 and v in S2) or (u in S2 and v in S1)
    ]

    return ([G.subgraph(S1).copy(), G.subgraph(S2).copy()], cut_edges) 

#def flow_cut_edge(G : nx.Graph):
#    G1,G2 = nx.algorithms.community.kernighan_lin_bisection(G)
#    S1,S2 = set(G1), set(G2)
#    cut_edges = [
#        (u, v) for u, v in G.edges()
#        if (u in S1 and v in S2) or (u in S2 and v in S1)
#    ]
#    return ([G.subgraph(S1).copy(),G.subgraph(S2).copy()],cut_edges)

def flow_cut_node(G : nx.Graph):
    return nx.minimum_node_cut(G)

#
# this algorithm works by separating G into 2 components and then applying itself onto the induced subgraphs
# On very small graphs, greedy is applied instead
# The resulting colorings are combined by shifting them into different ranges
#
def flow_trivial(G : nx.Graph,muffle=True):
    if G.order()<=4:
        *_,res= greedy_desc_deg(G)
        yield res
        return
    
    if not muffle:
        print("Aha", G.order())
    
    if nx.is_connected(G):
        Comps,cut=flow_cut_edge(G)
        if not muffle:
            print("comp",Comps,"cut",cut)
    else:
        Comps= [G.subgraph(c).copy() for c in nx.connected_components(G)]

    if not muffle:
        print("Aha2",len(Comps),max(G.order() for G in Comps))

    labels={}
    color_offset=0
    for i in Comps:
        for f in flow_trivial(i,True):
            yield f
            l=f
        for key in l.keys():
            labels[key]=l[key]+color_offset
        color_offset+=max(l.values())
        yield labels

    if not muffle:
        print("Aha3")

#
# this function takes two labeled graphs and constructs two dicts of adjacency sets, indexed by node; one for the first labeled graph and one for the border between the graphs
#
def build_adj_sets(labels_A,labels_B,edges_A,edges_border):
    adj_A = {n: set() for n in labels_A.values()}
    adj_B = {n: set() for n in labels_A.values()}
    for (u,v) in edges_A:
        adj_A[labels_A[u]].add(labels_A[v])
        adj_A[labels_A[v]].add(labels_A[u])
    for (u,v) in edges_border:
        if not u in labels_A.keys():
            u,v=v,u
        adj_B[labels_A[u]].add(labels_B[v])
    return adj_A,adj_B

# Merges labels_A into labels_B based on edge constraints between A and B and inside A
def merge_color_labels(labels_A,labels_B,edges_A,edges_border):
    adj_A,adj_B=build_adj_sets(labels_A,labels_B,edges_A,edges_border)
    remap={}
    to_remap=list(labels_A.values())
    used_colors=max(labels_B.values())
    
    def col_remap(Acol,Bcol):
        for src in adj_A.keys():
            if Acol in adj_A[src]:
                adj_B[src].add(Bcol)
        remap[Acol]=Bcol
    # Try to remap each color
    while len(to_remap):
        # Remap the color with the most constraints
        col=max(to_remap,key=lambda x: len(adj_B[x]))
        to_remap.remove(col)
        
        # Cannot map to a color in B, use new color
        if len(adj_B[col])==used_colors:
            col_remap(col,used_colors+1)
            used_colors+=1
            continue
        
        for remap_to in range(1,used_colors+1):
            if not remap_to in adj_B[col]:
                col_remap(col,remap_to)
                break
#    print("before remap A:",labels_A,"B:",labels_B)
#    print("remap",remap,"edges_a",edges_A)
    for k in labels_A.keys():
        labels_B[k]=remap[labels_A[k]]
#    print("after:",labels_B)
#    print("adjA",adj_A,"adjB",adj_B)
    return labels_B


# An LLM was insulting me for my inoptimal implementation, so I let them fix it, it runs ~25% faster, I won't complain
def merge_color_labels_optimized(labels_A, labels_B, edges_A, edges_border):                                        
    """                                                                                                             
    Optimized version of color merging with better data structures                                                  
    """                                                                                                             
    # Pre-compute color sets for faster lookups                                                                     
    colors_A = set(labels_A.values())                                                                               
    colors_B = set(labels_B.values())                                                                               
    max_color_B = max(labels_B.values()) if labels_B else 0                                                         
                                                                                                                    
    # Build adjacency more efficiently                                                                              
    adj_A = {color: set() for color in colors_A}                                                                    
    adj_B = {color: set() for color in colors_A}                                                                    
                                                                                                                    
    # Process internal edges of A                                                                                   
    for u, v in edges_A:                                                                                            
        color_u, color_v = labels_A[u], labels_A[v]                                                                 
        adj_A[color_u].add(color_v)                                                                                 
        adj_A[color_v].add(color_u)                                                                                 
                                                                                                                    
    # Process border edges                                                                                          
    for u, v in edges_border:                                                                                       
        if u in labels_A:                                                                                           
            adj_B[labels_A[u]].add(labels_B[v])                                                                     
        elif v in labels_A:                                                                                         
            adj_B[labels_A[v]].add(labels_B[u])                                                                     
                                                                                                                    
    # Greedy color assignment                                                                                       
    remap = {}                                                                                                      
    next_color = max_color_B + 1                                                                                    
                                                                                                                    
    # Sort colors by constraint count for better assignment                                                         
    colors_to_assign = sorted(colors_A, key=lambda c: len(adj_B[c]), reverse=True)                                  
                                                                                                                    
    for color_a in colors_to_assign:                                                                                
        forbidden = adj_B[color_a]                                                                                  
                                                                                                                    
        # Try to find an available color in B                                                                       
        assigned = False                                                                                            
        for color_b in range(1, max_color_B + 1):                                                                   
            if color_b not in forbidden:                                                                            
                remap[color_a] = color_b                                                                            
                # Update constraints for remaining colors                                                           
                for other_color in adj_A[color_a]:                                                                  
                    if other_color in adj_B:                                                                        
                        adj_B[other_color].add(color_b)                                                             
                assigned = True                                                                                     
                break                                                                                               
                                                                                                                    
        if not assigned:                                                                                            
            remap[color_a] = next_color                                                                             
            next_color += 1                                                                                         
                                                                                                                    
    # Apply remapping                                                                                               
    for node in labels_A:                                                                                           
        labels_B[node] = remap[labels_A[node]]                                                                      
                                                                                                                    
    return labels_B


#
# this algorithm works by separating G into 2 components and then applying itself onto the induced subgraphs
# On very small graphs, greedy is applied instead
# The resulting colorings are combined trying merging the colorings in a good way, without changing the colorings themselves
#
def flow_merge(G : nx.Graph,muffle=True):
    if G.order()<=10:
        *_,res= greedy_desc_deg(G)
        yield res
        return
    
    if not muffle:
        print("Aha", G.order())
    
    if nx.is_connected(G):
        Comps,cut=flow_cut_edge(G)
        if not muffle:
            print("comp",Comps,"cut",cut)
    else:
        cut=[]
        Comps= [G.subgraph(c).copy() for c in nx.connected_components(G)]
        labels={}
        for i in Comps:
            for f in flow_merge(i,True):
                for k in f.keys():
                    labels[k]=f[k]
                yield labels
        return

    if not muffle:
        print("Aha2",len(Comps),max(G.order() for G in Comps))

    labels={}
    did_comp1=False
    for i in Comps:
        for f in flow_merge(i,True):
            yield f
            l=f
        if did_comp1:
            merge_color_labels_optimized(l,labels,list(i.edges()),cut)
        else:
            labels=l
            did_comp1=True

        yield labels

    if not muffle:
        print("Aha3")