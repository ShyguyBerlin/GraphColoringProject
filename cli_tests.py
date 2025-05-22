from solvers.greedy import *
from solvers.wigderson import *
import networkx as nx
import asyncio

async def solve_graph(G : nx.graph, solver,do_print=False,delay=0):

    *_,a = solver(G)
    print(a)

asyncio.run(solve_graph(nx.erdos_renyi_graph(2000,0.2),so_called_easy_algorithm))