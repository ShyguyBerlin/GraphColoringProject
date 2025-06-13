from ..solvers import greedy
from ..solvers import wigderson
from ..solvers import solvers
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


# Test the color_swap solver on 5 random graphs
def test_color_swap_solver_correctness():
    for i in range(5):
        graph :nx.Graph = nx.erdos_renyi_graph(40,0.2)

        *_,res = greedy.greedy_color_swaps(graph)

        assert wigderson.check_complete(graph,res)

def test_all_solvers_correctness():
    for solver in solvers.get_solvers().values():
        for i in range(3):
            graph :nx.Graph = nx.erdos_renyi_graph(25,0.2)

            *_,res = solver(graph)

            assert wigderson.check_complete(graph,res)

def test_all_solvers_correctness_dense():
    for solver in solvers.get_solvers().values():
        for i in range(3):
            graph :nx.Graph = nx.erdos_renyi_graph(35,0.9)

            *_,res = solver(graph)

            assert wigderson.check_complete(graph,res)