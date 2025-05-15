from solvers.greedy import *
from solvers.wigderson import *
import networkx as nx
import asyncio

async def solve_graph(G : nx.graph, solver,do_print=False,delay=0):
    print("I am using the delay",delay)

    for labels in solver(G):
        print(labels)

asyncio.run(solve_graph(nx.cycle_graph(11),so_called_easy_algorithm))