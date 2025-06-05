import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from random import shuffle,randint
import asyncio
from solvers.solvers import get_solvers
from web_elements import *
from random import sample

rseed=randint(0,10000)

##########Functions for defining graph###############
def create_nodes(G: nx.graph, knoten_anzahl):
    for i in range(knoten_anzahl):
        G.add_node(i)
    return G

def create_edge_density(G: nx.graph, edge_density):

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

def define_own_graph():
    input_text = get_graph_input("Knotenanzahl")
    G = nx.Graph()
    if(input_text != ""):
        knoten_anzahl = int(input_text)
        G = create_nodes(G, knoten_anzahl)

    edge_density_input = get_graph_input("edge-density-range")
    if(edge_density_input != ""):
        edge_density = float(int(edge_density_input))/100
        G = create_edge_density(G, edge_density)

    input_clique = get_graph_input("Cliquengroesse")
    if (input_clique != ""):
        clique = int(input_clique)
        G = create_clique(G, clique)

    return G

###############################################################

async def solve_graph(G : nx.graph, solver,do_print=False,delay=0):
    print("I am using the delay",delay)

    for labels in solver(G):
        if do_print and delay>0:
            print_graph(G,labels)

        if delay: await asyncio.sleep(delay)
    if do_print and delay==0:
        print_graph(G,labels)

def get_graph_input(id) -> str:
    graph_input = document.getElementById(id)
    if graph_input:
        return graph_input.value
    return None

def generate_graph(method):
    match(method):
        case "edge-list":
            raw=get_graph_input("graph-input")
            raw_lines = raw.split("\n")
            graph :nx.graph = nx.empty_graph(int(raw_lines[0]))
            print("Graph ",graph,graph.nodes())
            for i in raw_lines[1:]:
                nodes = i.split(" ")
                graph.add_edge(int(nodes[0]),int(nodes[1]))
            print("Graph ",graph,graph.nodes())
            return graph
        case "adjacency-matrix":
            raw=get_graph_input("graph-input")
            raw_lines = raw.split("\n")
            graph :nx.graph = nx.empty_graph(len(raw_lines))
            for u in range(len(raw_lines)):
                for v in range(len(raw_lines)):
                    if int(raw_lines[u].split(" ")[v])!=0:
                        graph.add_edge(u,v)
            return graph
        case "define-own-graph":
            graph: nx.graph = nx.Graph()
            graph = define_own_graph()
            return graph
        case "erdos-renyi-graph":
            return nx.erdos_renyi_graph(100,0.2,seed=rseed)

def start_solver(event):
    stop_solver(event)
    global current_draw_task
    print(event)

    delay= get_delay_selection()
    selected_solver = get_solver_selection()
    selected_graph = get_graph_selection()

    solvers=get_solvers()
    G = generate_graph(selected_graph)

    current_draw_task = asyncio.create_task(solve_graph(G,solvers[selected_solver],True,delay=delay))

def stop_solver(event):
    global current_draw_task
    try:
        if current_draw_task:
            current_draw_task.cancel()
            current_draw_task = None
    except:
        print("There was nothing to stop")


