import networkx as nx
from random import sample,randint
from random import seed as setseed

global_seed=randint(0,1000000)

def create_nodes(G: nx.Graph, knoten_anzahl):
    for i in range(knoten_anzahl):
        G.add_node(i)
    return G

def create_edge_density(G: nx.Graph, edge_density):

    knoten_anzahl = len(list(G.nodes()))
    # Anzahl Kanten ermitteln:
    number_edges = round((edge_density * knoten_anzahl * (knoten_anzahl - 1)) / 2)
    existing_edges = len(list(G.edges()))
    if (existing_edges < number_edges):
        non_edges = nx.non_edges(G)
        random_non_edges = sample(list(non_edges), (number_edges - existing_edges))
        for random_non_edge in random_non_edges:
            G.add_edge(random_non_edge[0], random_non_edge[1])
    elif (existing_edges > number_edges):
        random_existing_edges = sample(list(G.edges()), (existing_edges - number_edges))
        for random_existing_edge in random_existing_edges:
            G.remove_edge(random_existing_edge[0], random_existing_edge[1])
    return G

def create_clique(G: nx.Graph, clique):
    cliquen_liste = list(nx.find_cliques(G))
    max_clique_number = max(len(c) for c in cliquen_liste)
    #print(clique,max_clique_number,cliquen_liste)
    if (clique > max_clique_number):
        random_nodes = sample(list(G.nodes()), clique)
        for i in range(len(random_nodes)):
            for j in range(i + 1, len(random_nodes)):
                G.add_edge(random_nodes[i], random_nodes[j])
    elif (clique < max_clique_number):
        max_cliquen_list = list(nx.find_cliques(G))
        for max_c in max_cliquen_list:
            G_1 = G.subgraph(max_c)
            random_nodes = sample(list(max_c), (max_clique_number - clique))
            for ran_node in random_nodes:
                ran_edge=list(G_1.edges(ran_node))[0]

                G.remove_edge(ran_edge[0], ran_edge[1])
    return G

def create_nodes_in_groups(nodes, groups):
    graph = nx.Graph(nodes)
    return graph

def define_own_graph(nodes=10, *, edge_density=None, max_clique=None, seed=global_seed) -> nx.Graph:
    G = nx.Graph()

    if nodes==None:
        nodes=10
    
    if seed==None:
        setseed(seed)

    knoten_anzahl = int(nodes)
    
    G = create_nodes(G, knoten_anzahl)

    if edge_density != None:
        G = create_edge_density(G, edge_density)

    if max_clique != None:
        G = create_clique(G, max_clique)

    return G

def define_own_graph_chromatic(nodes=10, *, edge_density=None, chromatic_number=3, seed=global_seed) -> nx.Graph:

    if nodes==None:
        nodes=10
    
    if seed==None:
        setseed(seed)

    knoten_anzahl = int(nodes)
    
    G = create_nodes_in_groups(knoten_anzahl,chromatic_number)

    return G

def convert_to_text(graphs:list[nx.Graph]):
    graph6_lines = [nx.to_graph6_bytes(g, header=False).decode("ascii") for g in graphs]

    return "".join(graph6_lines)