from . import greedy
from . import wigderson
import networkx as nx

def test_color_swap_success():
    graph :nx.Graph = nx.cycle_graph(5)
    graph.remove_edge(4,0)

    labels={0:1,1:2,3:2,4:1}

    assert greedy.try_swap(graph,labels,[1],1,[3])==[1,0]

def test_color_swap_fail():
    graph :nx.Graph = nx.cycle_graph(5)

    labels={0:1,1:2,3:1,4:2}

    assert greedy.try_swap(graph,labels,[1],1,[3])==None

def test_color_swap_trivial_input():
    graph :nx.Graph = nx.cycle_graph(5)

    labels={0:1,1:2,3:1,4:2}

    assert greedy.try_swap(graph,labels,[1],2,[3])==[]

def test_color_swap_solver_correctness():
    graph :nx.Graph = nx.erdos_renyi_graph(40,0.2)

    *_,res = greedy.greedy_color_swaps(graph)

    assert wigderson.check_complete(graph,res)