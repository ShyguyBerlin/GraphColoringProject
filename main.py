import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from random import shuffle,randint
import asyncio
from solvers.greedy import *
from solvers.wigderson import so_called_easy_algorithm,wigdersons_first
from web_elements import *

rseed=randint(0,10000)

async def solve_graph(G : nx.graph, solver,do_print=False,delay=0):
    print("I am using the delay",delay)

    for labels in solver(G):
        if do_print and delay>0:
            print_graph(G,labels)

        if delay: await asyncio.sleep(delay)
    if do_print and delay==0:
        print_graph(G,labels)

def get_graph_input() -> str:
    graph_input = document.getElementById("graph-input")
    if graph_input:
        return graph_input.value
    return None

def generate_graph(method):
    match(method):
        case "edge-list":
            raw=get_graph_input()
            raw_lines = raw.split("\n")
            graph :nx.graph = nx.empty_graph(int(raw_lines[0]))
            print("Graph ",graph,graph.nodes())
            for i in raw_lines[1:]:
                nodes = i.split(" ")
                graph.add_edge(int(nodes[0]),int(nodes[1]))
            print("Graph ",graph,graph.nodes())
            return graph
        case "adjacency-matrix":
            raw=get_graph_input()
            raw_lines = raw.split("\n")
            graph :nx.graph = nx.empty_graph(len(raw_lines))
            for u in range(len(raw_lines)):
                for v in range(len(raw_lines)):
                    if int(raw_lines[u].split(" ")[v])!=0:
                        graph.add_edge(u,v)
            return graph
        case _:

            return nx.erdos_renyi_graph(100,0.2,seed=rseed)

def start_solver(event):
    stop_solver(event)
    global current_draw_task
    print(event)

    delay= get_delay_selection()
    selected_solver = get_solver_selection()
    selected_graph = get_graph_selection()

    solvers={"greedy": greedy_no_sort, "greedy_min":greedy_asc_deg, "greedy_max":greedy_desc_deg, "so_called_easy":so_called_easy_algorithm, "wigdersons_first":wigdersons_first}
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


