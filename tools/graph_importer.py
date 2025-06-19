import networkx as nx

def parse_edge_list(file):
    graphs=[]
    for graph_raw in file.read().split("\n\n"):
        raw_lines = graph_raw.split("\n")
        graph :nx.graph = nx.empty_graph(int(raw_lines[0]))
        for i in raw_lines[1:]:
            nodes = i.split(" ")
            graph.add_edge(int(nodes[0]),int(nodes[1]))
        graphs.append(graph)
    return graphs

def parse_adjacency_matrix(file):
    graphs=[]
    for graph_raw in file.read().split("\n\n"):
        if graph_raw == "":
            continue
        raw_lines = graph_raw.split("\n")
        graph :nx.graph = nx.empty_graph(len(raw_lines))
        for u in range(len(raw_lines)):
            for v in range(len(raw_lines)):
                if int(raw_lines[u].split(" ")[v])!=0:
                    graph.add_edge(u,v)
        graphs.append(graph)
    return graphs

def parse_graph6(file):
    G = nx.graph6.read_graph6(file)
    if isinstance(G,list):
        return G
    return [G]

def parse_file(file, parser):
    match parser:
        case "edge-list":
            return parse_edge_list(file)

        case "adjacency-matrix":
            return parse_adjacency_matrix(file)

        case "graph6":
            return parse_graph6(file)
            
        case x:
            valids="edge-list adjacency-matrix graph6"
            if x is None:
                print(f"""No parser specified. Please use one of the following formats:
                {valids}""")
            else:
                print(f"""The format "{x}" is not supported. Please use one of the following formats:
                {valids}""")
            exit(1)

def get_and_parse_file(file_path, parser):
    with open(file_path, "r") as file:
        return (parse_file(file,parser))