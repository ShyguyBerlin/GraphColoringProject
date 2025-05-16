from solvers.greedy import *
from solvers.wigderson import *
import networkx as nx
import asyncio

def solve_graph(G : nx.graph, solver,do_print=False,delay=0):
    print("I am using the delay",delay)

    for labels in solver(G):
        print(labels)

solve_graph(nx.erdos_renyi_graph(200,0.2),wigdersons_first)