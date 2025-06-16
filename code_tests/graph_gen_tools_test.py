import tools.graph_gen_tools as ggt
import networkx as nx

class Test_trim_graph_set_metadata():
    def test_ignore_none(self):
        ggt.trim_graph_set_metadata(None,[])
        assert True==True
    
    def test_trim_one(self):
        metadata={"a":5,"b":3}
        G=nx.Graph()
        G.graph["a"]=5
        ggt.trim_graph_set_metadata(metadata,[G])
        assert G.graph=={}
    
    def test_not_trim_update(self):
        metadata={"a":5,"b":3}
        G=nx.Graph()
        G.graph["a"]=6
        ggt.trim_graph_set_metadata(metadata,[G])
        assert G.graph=={"a":6}
class Test_convert_to_text_gsm:

    def test_simple(self):
        G=nx.empty_graph(5)
        G.add_edge(2,4)
        assert ggt.convert_to_text_gsm([G]) == "g"+nx.to_graph6_bytes(G, header=False).decode("ascii")

    def test_graph_with_metadata(self):
        G=nx.empty_graph(5)
        G.add_edge(2,4)
        G.graph["something"]="else"
        assert ggt.convert_to_text_gsm([G]) == "g"+nx.to_graph6_bytes(G, header=False).decode("ascii")+"m\"something\": \"else\"\n"

    def test_graphs_with_metadata(self):
        G=nx.empty_graph(5)
        G.add_edge(2,4)
        G.graph["something"]="else"
        H=nx.empty_graph(5)
        H.add_edge(2,4)
        H.graph["no"]="change"
        assert ggt.convert_to_text_gsm([G,H]) == "g"+nx.to_graph6_bytes(G, header=False).decode("ascii")+"m\"something\": \"else\"\n"+"g"+nx.to_graph6_bytes(H, header=False).decode("ascii")+"m\"no\": \"change\"\n"