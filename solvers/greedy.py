import networkx as nx

async def solve_graph( G : nx.graph):
    labels={}

    for node in G.nodes():
        used = {labels.get(neigh) for neigh in G.neighbors(node)}
        c=1
        while True:
            if c not in used:
                labels[node]= c
                break
            c+=1
        
        yield labels