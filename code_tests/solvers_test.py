from solvers import greedy
from solvers import wigderson
from solvers import solvers
from tools.graph_gen_tools import convert_to_text_gsm
import networkx as nx

import pytest

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

@pytest.mark.parametrize("solver", solvers.get_generic_solvers().values(), ids=solvers.get_generic_solvers().keys())
def test_generic_solvers_correctness(solver : solvers.Solver):
    for i in range(3):
        graph :nx.Graph = nx.erdos_renyi_graph(25,0.2)

        graph_copied=graph.copy()

        *_,res = solver.func(graph)

        assert wigderson.check_complete(graph,res) # solver should create a valid solution

        assert nx.is_isomorphic(graph,graph_copied) # solver should not change the graph

        assert not 0 in res.values() # Guarantee that colors begin at 1

def test_make_better_correctness():
    make_betters={
        "greedy_no_sort_make_better": solvers.get_solvers()["greedy_no_sort_make_better"],
        "greedy_asc_deg_make_better": solvers.get_solvers()["greedy_asc_deg_make_better"],
        "greedy_desc_deg_make_better": solvers.get_solvers()["greedy_desc_deg_make_better"],
        "greedy_color_swaps_make_better": solvers.get_solvers()["greedy_color_swaps_make_better"]
    }
    for s in make_betters.keys():
        for i in range(150):
            graph :nx.Graph = nx.erdos_renyi_graph(25,0.2)

            graph_copied=graph.copy()

            *_,res = make_betters[s].func(graph)

            #print(s,graph,convert_to_text_gsm([graph]))

            assert wigderson.check_complete(graph,res) # solver should create a valid solution

            assert nx.is_isomorphic(graph,graph_copied) # solver should not change the graph

            assert not 0 in res.values() # Guarantee that colors begin at 1


@pytest.mark.parametrize("solver", solvers.get_generic_solvers().values(), ids=solvers.get_generic_solvers().keys())
def test_generic_solvers_correctness_dense(solver : solvers.Solver):
    for i in range(3):
        graph :nx.Graph = nx.erdos_renyi_graph(35,0.9)

        graph_copied=graph.copy()

        *_,res = solver.func(graph)

        assert wigderson.check_complete(graph,res) # solver should create a valid solution

        assert nx.is_isomorphic(graph,graph_copied) # solver should not change the graph

        assert not 0 in res.values() # Guarantee that colors begin at 1

def test_generic_solvers_correct_listing():
    assert not "berger-rompel" in solvers.get_generic_solvers().keys()