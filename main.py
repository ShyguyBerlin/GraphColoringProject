import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from random import shuffle,randint
import asyncio
from solvers.solvers import get_generic_solvers
from web_elements import *
from random import sample
from tools.graph_gen_tools import define_own_graph

rseed=randint(0,10000)



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
            nodes=None
            edge_density=None
            max_clique=None

            nodes_input = get_graph_input("Knotenanzahl")
            if nodes_input != "":
                nodes=int(nodes_input)

            edge_density_input = get_graph_input("edge-density-range")
            if edge_density_input != "":
                edge_density = float(int(edge_density_input))/100

            input_clique = get_graph_input("Cliquengroesse")
            if (input_clique != ""):
                max_clique = int(input_clique)
            
            graph: nx.graph = nx.Graph()
            graph = define_own_graph(nodes,edge_density=edge_density,max_clique=max_clique)
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

    solvers=get_generic_solvers()
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


