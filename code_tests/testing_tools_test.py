from tools import testing_tools as tt
import networkx as nx

def test_solve_graph_runs():

    g = nx.erdos_renyi_graph(20,0.2)

    def solver(G : nx.Graph):
        labels ={}
        nodes = list(G.nodes())
        for i in range(len(nodes)):
            labels[nodes[i]]=i+1
        yield labels

    tt.solve_graph(g,solver)

    assert True==True