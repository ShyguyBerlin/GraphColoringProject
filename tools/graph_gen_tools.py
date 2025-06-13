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

def determine_edge_count(edge_density, nodes, groups):
    mod = nodes % groups
    anz = nodes // groups
    anz2 = nodes // groups + 1
    edges = 0
    count1 = 1
    count2 = groups
    while count1 < groups:
        while count2 > count1:
            if(count1 <= mod):
                if(count2 <= mod):
                    edges = edges + (anz2*anz2)
                else:
                    edges = edges + (anz2*anz)
            else:
                edges = edges + (anz*anz)
            count2 = count2 - 1
        count2 = groups
        count1 = count1 + 1
    edges = round(edges*edge_density)
    return edges 

def create_nodes_in_groups(nodes, edges, groups):  # Die implementation gerade arbeitet mit modulo. Die Idee ist, dass alle Knoten in Gruppen geteilt sind anhand dessen,
    graph = nx.Graph()                             # was sie modulo der chromatischen Zahl sind. Das führt zu einer gleichmäßigen Verteilung auf die Gruppen.
                                                   # Falls das nicht unbedingt sein soll, müsste man die Implementation stark verändern
    graph = create_nodes(graph, nodes)

    edge_counter = 0
    random_counter = 1
    non_edges = list(nx.non_edges(graph))
    random_non_edges = sample(list(non_edges), min(int(nodes*(nodes-1)/2), len(non_edges)))
    while edge_counter < edges:
        if(random_counter == len(random_non_edges)):
            print("Error: not enough edges possible")
            exit(2)
        random_edge = random_non_edges[random_counter]
        test1 = random_edge[0] % groups # Das % hier ist das modulo rechnen 
        test2 = random_edge[1] % groups
        if(test1 == test2):
            random_counter = random_counter + 1
        else:
            graph.add_edge(random_edge[0], random_edge[1])
            random_counter = random_counter + 1
            edge_counter = edge_counter + 1

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

    G = nx.Graph()

    if nodes==None:
        nodes=10
    
    if seed==None:
        setseed(seed)

    if edge_density==None:
        edge_density=0.3 #arbitrary

    knoten_anzahl = int(nodes)

    kanten_anzahl = int(determine_edge_count(edge_density=edge_density, nodes=nodes, groups=chromatic_number))
    
    G = create_nodes_in_groups(knoten_anzahl, kanten_anzahl, chromatic_number)

    return G

def define_own_cograph(nodes = 10):
    G = nx.Graph()
    #G = define_own_cograph_recursive(nodes, 1)
    G = nx.random_cograph(nodes)
    return G
    


def define_own_cograph_recursive(nodes = 10, counter = 1) -> nx.Graph:
    graph = nx.Graph()
    if(nodes == 1):
        graph.add_node(counter)
        return graph
    split = randint(1, nodes-1)
    Part1 = nx.Graph()
    Part2 = nx.Graph()
    Part1 = define_own_cograph_recursive(split, counter)
    Part2 = define_own_cograph_recursive(nodes-split, counter+split)
    construction_rule = randint(1,2) # 1 ist Vereinigung, 2 ist Summe
    if(construction_rule == 1):
        graph = nx.compose(Part1, Part2)
    if(construction_rule == 2):
        graph = nx.compose(Part1, Part2)
        for node in Part1.nodes:
            for node2 in Part2.nodes:
                graph.add_edge(node, node2)

    return graph

def convert_to_text(graphs:list[nx.Graph]):
    graph6_lines = [nx.to_graph6_bytes(g, header=False).decode("ascii") for g in graphs]

    return "".join(graph6_lines)