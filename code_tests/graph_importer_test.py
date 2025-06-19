import os
import tempfile
import shutil
import io

import pytest

import tools.graph_importer as gimport
import networkx as nx

def test_get_and_parse_file():
    # Step 1: Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    try:
        # Step 2: Create a temporary file in that directory
        temp_file_path = os.path.join(temp_dir, "test.txt")
        with open(temp_file_path, "w") as f:
            f.write("5\n0 1\n1 2\n2 3\n3 4\n4 0")

        # Step 3: Call the function with the path
        result = gimport.get_and_parse_file(temp_file_path,"edge-list")

        # Step 4: Save or assert the result
        assert isinstance(result,list)

        assert len(result)==1

        assert nx.is_isomorphic(result[0],nx.cycle_graph(5))
    
    finally:
        # Step 5: Clean up the temporary directory
        shutil.rmtree(temp_dir)


___cycle_graph_with_metadata=nx.cycle_graph(5)
___cycle_graph_with_metadata.graph["c"]=4

@pytest.mark.parametrize("graphs, parser, expected", [
    ("5\n0 1\n1 2\n2 3\n3 4\n4 0", "edge-list", [nx.cycle_graph(5)]),
    ("0 1 1\n0 0 1\n0 0 0", "adjacency-matrix",[nx.cycle_graph(3)]),
    ("gDhc\nm\"c\":4","gsm",[___cycle_graph_with_metadata])
])
def test_parse_graph_isomorph(graphs,parser,expected):
    parse_file = io.StringIO(graphs)

    res=gimport.parse_file(parse_file,parser)

    assert isinstance(res,list)

    assert len(res)==len(expected)

    print(res,expected)
    # test for isomorphism
    for i in range(len(res)):
        assert nx.is_isomorphic(res[i],expected[i])

    for i in range(len(res)):
        assert res[i].graph==expected[i].graph