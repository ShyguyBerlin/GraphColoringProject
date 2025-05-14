import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from random import shuffle,randint
import asyncio
from solvers.greedy import *
from web_elements import *

async def solve_graph(G : nx.graph, solver,do_print=False,delay=0):
    print("I am using the delay",delay)
    async for labels in solver(G):
        if do_print and delay>0:
            print_graph(G,labels)

        if delay: await asyncio.sleep(delay)
    if do_print and delay==0:
        print_graph(G,labels)

def generate_graph(method):
    match(method):
        case _:
            return nx.cycle_graph(31)

def start_solver(event):
    stop_solver(event)
    global current_draw_task
    print(event)

    delay= get_delay_selection()
    selected_solver = get_solver_selection()
    selected_graph = get_graph_selection()

    solvers={"greedy": greedy_no_sort, "greedy_min":greedy_asc_deg, "greedy_max":greedy_desc_deg}
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


