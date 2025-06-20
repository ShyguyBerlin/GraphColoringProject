import networkx as nx
import json

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
    graphs=[]
    for i in file.read().split("\n"):
        if i=="":
            continue
        graphs.append(nx.graph6.from_graph6_bytes(i.encode(encoding="utf-8")))
    return graphs

def parse_gsm(file):
    lines = file.read().split("\n")
    meta = {}
    graphs = []

    def process_meta(meta):
        return json.loads("{"+meta+"}")

    for i in range(len(lines)):
        line=lines[i]

        if len(line)==0:
            continue

        line_type=line[0]
        line=line[1:]
        match line_type:
            case 'g':
                graphs.append(nx.graph6.from_graph6_bytes(line.encode(encoding="utf-8")))
            case 's':
                graphs.append(nx.sparse6.from_sparse6_bytes(line.encode(encoding="utf-8")))
            case 'm':
                if len(graphs)==0:
                    d = process_meta(line)
                    for key in d.keys():
                        meta[key]=d[key]
                else:
                    d = process_meta(line)
                    for key in d.keys():
                        graphs[-1].graph[key]=d[key]
            case x:
                print(f"ERROR: incorrect gsm format. Found illegal character '{x}' in line {i} at position 0.")
                exit(1)
    for i in graphs:
        for key in meta.keys():
            if not key in i.graph.keys():
                i.graph[key]=meta[key]

    return graphs

def parse_file(file, parser):
    match parser:
        case "edge-list":
            return parse_edge_list(file)

        case "adjacency-matrix":
            return parse_adjacency_matrix(file)

        case "graph6":
            return parse_graph6(file)
            
        case "gsm":
            return parse_gsm(file)

        case x:
            valids="edge-list adjacency-matrix graph6 gsm"
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