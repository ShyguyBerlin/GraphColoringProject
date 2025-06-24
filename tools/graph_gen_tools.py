import networkx as nx
from random import sample,randint,random
from random import seed as setseed
from .graph_gen_data_classes import ModulatorData

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
    # Calculates the amount of all possible edges
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

def apply_modulator(G : nx.Graph,modulator:ModulatorData) -> nx.Graph :
    
    if modulator.nodes==None or modulator.nodes==0:
        return G

    if modulator.density==None:
        modulator.density=nx.function.density(G)

    m_graph=nx.erdos_renyi_graph(modulator.nodes,modulator.density)

    union_graph : nx.Graph =nx.disjoint_union(G,m_graph)

    union_nodes=list(union_graph.nodes())
    m_nodes=union_nodes[G.order():]
    g_nodes=union_nodes[:G.order()]

    for i in m_nodes:
        for o in g_nodes:
            if random()<modulator.density:
                union_graph.add_edge(i,o)

    return union_graph

def define_own_graph(nodes=10, *, edge_density=None, max_clique=None, seed=global_seed) -> nx.Graph:
    G = nx.Graph()

    if nodes==None:
        nodes=10
    
    if True:
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
    
    if True:
        setseed(seed)

    if edge_density==None:
        edge_density=0.3 #arbitrary

    knoten_anzahl = int(nodes)

    kanten_anzahl = int(determine_edge_count(edge_density=edge_density, nodes=nodes, groups=chromatic_number))
    
    G = create_nodes_in_groups(knoten_anzahl, kanten_anzahl, chromatic_number)

    G.graph["chromatic-number"]=chromatic_number

    return G

def define_own_cograph(nodes = 10):
    G = nx.Graph()
    G = define_own_cograph_recursive(nodes, 1)
    #G = nx.random_cograph(nodes)
    return G

def define_own_cograph_first(nodes = 10, mode = False ):
    graph = nx.Graph()
    split = randint(1, nodes-1)
    Part1 = nx.Graph()
    Part2 = nx.Graph()
    Part1 = define_own_cograph_recursive(split, 1)
    Part2 = define_own_cograph_recursive(nodes-split, 1+split)
    if(mode == True):
        graph = nx.union(Part1, Part2)
    if(mode == False):
        graph = nx.full_join(Part1, Part2, rename=("G", "H"))
    return graph
        


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
        graph = nx.union(Part1, Part2)
    if(construction_rule == 2):
        graph = nx.full_join(Part1, Part2, rename=("G", "H"))

    return graph

def convert_to_text(graphs:list[nx.Graph]):
    graph6_lines = [nx.to_graph6_bytes(g, header=False).decode("ascii") for g in graphs]

    return "".join(graph6_lines)

import json

def add_gsm_header(metadata,gsm_text):
    if metadata==None or len(metadata.keys())==0:
        return gsm_text
    header=json.dumps(metadata)[1:-1]
    return "m"+header+"\n"+gsm_text

def trim_graph_set_metadata(metadata,graphs):
    for g in graphs:
        dup_props=[]
        for prop in g.graph.keys():
            if prop in metadata and metadata[prop] == g.graph[prop]:
                dup_props.append(prop)
        
        for prop in dup_props:
            del g.graph[prop]

def convert_to_text_gsm(graphs:list[nx.Graph]):
    lines=[]
    for g in graphs:
        lines.append("g"+nx.to_graph6_bytes(g, header=False).decode("ascii"))
        if len(g.graph.keys())>0:
            lines.append("m"+json.dumps(g.graph)[1:-1]+"\n")

    return "".join(lines)