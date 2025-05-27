import networkx as nx
from solvers.solvers import get_solvers
import time
import json

def get_and_parse_file(file_path,parser):
    match parser:
        case "gml":
            return [nx.read_gml(file_path)]
        case "graphml":
            return [nx.read_graphml(file_path)]
        case "edge-list":
            with open(file_path, "r") as file:
                graphs=[]
                for graph_raw in file.read().split("\n\n"):
                    raw_lines = graph_raw.split("\n")
                    graph :nx.graph = nx.empty_graph(int(raw_lines[0]))
                    for i in raw_lines[1:]:
                        nodes = i.split(" ")
                        graph.add_edge(int(nodes[0]),int(nodes[1]))
                    graphs.append(graph)
                return graphs
        case "adjacency-matrix":
            with open(file_path, "r") as file:
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
        case "pickle":
            G = nx.read_gpickle(file_path)
            return [G]
        case "graph6":
            G = nx.graph6.read_graph6(file_path)
            if isinstance(G,list):
                return G
            return [G]
        case x:
            if x is None:
                print(f"""No parser specified. Please use one of the following formats:
                gml graphml edge-list adjacency-matrix pickle graph6""")
            else:
                print(f"""The format "{x}" is not supported. Please use one of the following formats:
                gml graphml edge-list adjacency-matrix pickle graph6""")
            exit(1)

class Test_input:
    def __init__(self,test_name,timeout,raw_graph_sets,solvers):
        self.test_name=test_name
        self.timeout=timeout
        self.graph_sets=[]
        for (file_path,set_name,parser) in raw_graph_sets:
            self.graph_sets.append(Graph_set(parser,file_path,set_name))
        self.solvers=solvers

    def get_total_steps(self):
        return sum([len(graph_set.graphs) for graph_set in self.graph_sets])*len(self.solvers)

def get_test_from_file(file_path :str) -> Test_input:
    
    stdError=f"ERROR: Cannot convert the file {file_path} to test."
    
    with open(file_path,"r") as file:
        obj=json.load(file)
        
        name="Test"
        if "name" in obj:
            name=obj["name"]
        
        timeout=100
        if "timeout" in obj:
            timeout=obj["timeout"]

        if "solvers" in obj:
            if not isinstance(obj["solvers"],list):
                print(stdError+" The \"solvers\" property shall be an array of strings, each being one of the available solving algorithms.")
                exit(1)
            solvers=obj["solvers"]
        else:
            solvers=get_solvers().keys()

        datasets=[]

        if not "datasets" in obj:
            print(stdError+f" The file misses the value \"datasets\".")
            exit(1)
    
        if not isinstance(obj["datasets"],list):
            print(stdError+f" The \"datasets\" property must be a list.")
            exit(1)

        for dataset in obj["datasets"]:
            stdDataSetError=stdError+" Each dataset must be an object containing the \"parser\" and the \"file-path\" to a dataset."
            if (not isinstance(dataset,dict)) or (not "file-path" in dataset) or (not "parser" in dataset):
                print(stdDataSetError)
                exit(1)
            setname = dataset["file-path"]
            if "name" in dataset:
                setname = dataset["name"]
            
            datasets.append((dataset["file-path"],setname,dataset["parser"]))

        test= Test_input(name,timeout,datasets,solvers)
        return test

class Graph_set:
    def __init__(self,parser,file_path,set_name):
        self.graphs=get_and_parse_file(file_path,parser)
        self.name=set_name

class Graph_set_result:
    def __init__(self,graph_set_name):
        self.name=graph_set_name
        self.orders=[]
        self.colors=[]
        self.exec_times=[]

    def add_result(self,order:int,colors:int,exec_time:float):
        self.orders.append(order)
        self.colors.append(colors)
        self.exec_times.append(exec_time)

class Test_result:
    test_name=None
    
    results : list[tuple[Graph_set_result,str]]=[]

    def add_results(self,solver_used:str,graph_set_results:list[Graph_set_result]):
        modified_results=[ (i,solver_used) for i in graph_set_results]
        self.results.extend(modified_results)


CSV_HEADER="test_name,solver,graph_set,graph_idx,graph_order_min,graph_order_max,graph_order_avg,graph_order_med,exec_time_min,exec_time_max,exec_time_avg,exec_time_med,colors_min,colors_max,colors_avg,colors_med"

def format_tests_as_csv(tests : list[Test_result]) -> str:
    csv_lines=[CSV_HEADER]
    for test in tests:
        for graph_set_result,solver in test.results:
            min_order = min(graph_set_result.orders)
            max_order = max(graph_set_result.orders)
            avg_order = sum(graph_set_result.orders)/len(graph_set_result.orders)
            med_order = sorted(graph_set_result.orders)[len(graph_set_result.orders)//2]

            min_colors = min(graph_set_result.colors)
            max_colors = max(graph_set_result.colors)
            avg_colors = sum(graph_set_result.colors)/len(graph_set_result.colors)
            med_colors = sorted(graph_set_result.colors)[len(graph_set_result.colors)//2]

            min_exec_time = min(graph_set_result.exec_times)
            max_exec_time = max(graph_set_result.exec_times)
            avg_exec_time = sum(graph_set_result.exec_times)/len(graph_set_result.exec_times)
            med_exec_time = sorted(graph_set_result.exec_times)[len(graph_set_result.exec_times)//2]

            csv_lines.append(f"\"{test.test_name}\",\"{solver}\",\"{graph_set_result.name}\",0,{min_order},{max_order},{round(avg_order,2)},{med_order},{min_exec_time},{max_exec_time},{round(avg_exec_time,4)},{round(med_exec_time,4)},{min_colors},{max_colors},{round(avg_colors,4)},{med_colors}")
    return "\n".join(csv_lines)

def format_test_as_csv(test : Test_result) -> str:
    return format_tests_as_csv([test])

#Returns (Runtime in miliseconds, Number of colors used)
def solve_graph(G : nx.graph, solver) -> tuple[float,int]:
    start_time = time.monotonic_ns()

    *_,a = solver(G)
    
    # Calculate difference, devide by 
    execution_time = (time.monotonic_ns() - start_time)/1_000_000

    return (execution_time,max(a.values()))

def run_test(input : Test_input) -> Test_result:
    print(f"Running test {input.test_name}")
    res=Test_result()
    res.test_name=input.test_name

    start_time=time.time()
    last_log=start_time
    steps_completed=0
    total_steps=input.get_total_steps()
    do_logging= (total_steps>=1000)

    for solver in input.solvers:
        if not solver in get_solvers():
            print(f"Solver {solver} not found!")
            continue

        solver_results = []
        for graph_set in input.graph_sets:
            graph_set : Graph_set = graph_set
            graph_set_result = Graph_set_result(graph_set.name)
            for graph in graph_set.graphs:
                graph : nx.Graph = graph
                exec_time, cols = solve_graph(graph,get_solvers()[solver])
                graph_set_result.add_result(graph.order(),cols,exec_time)
                steps_completed+=1
                if (do_logging and time.time()-last_log>5):
                    print(f"Done by {round(steps_completed/total_steps*100,1)}% est. time remaining: {round((time.time()-start_time)/steps_completed*(total_steps-steps_completed),1)}s")
                    last_log=time.time()
            solver_results.append(graph_set_result)
        res.add_results(solver,solver_results)
    print(f"Finished test {input.test_name}")
    return res
