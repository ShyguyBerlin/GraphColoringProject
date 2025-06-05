# This script is meant to be executed as a CLI tool and may assist in generating graph datasets

from sys import argv
from tools.graph_gen_tools import define_own_graph,convert_to_text

def print_help():
    print(f"""     Use: {argv[0]} OPTIONS \n
        Options:
        --amount -a <number> : How many graphs shall be created
        --nodes -n <count> : Sets the amount of nodes per graph
        --density -d <edge_density> : Formula to determine the density of edges, can be given as constant or formula
        --max_clique -mc <size> : Guarantees that the maximum clique will be of this size
        --chromatic-number -cn <number> : Sets an UPPER limit to the resulting coloring number
        --seed -s <number> : Sets a seed to use for random algorithms
        --output -o <path> : Will write resulting graphs to this file
        """)

def cli():
    
    amount = 1
    nodes_count=None
    clique_size=None
    density=None
    chromatic_number=None
    seed=None
    output=None

    if len(argv)<=1:
        print_help()
        exit()

    i=1

    # Helper to shorten parameter match
    def get_arg():
        nonlocal i
        if len(argv) > i+1:
            i+=1
            return argv[i]
        else:
            print("Incorrect amount/layout of arguments")
            exit(1)

    while i<len(argv):
        match(argv[i]):
            case "--amount" | "-a":
                amount = int(get_arg())
            case "--nodes" | "-n":
                nodes_count = int(get_arg())
            case "--density" | "-d":
                density = float(get_arg())
            case "--max_clique" | "-mc":
                clique_size = int(get_arg())
            case "--chromatic-number" | "-cn":
                chromatic_number = int(get_arg())
            case "--seed" | "-s":
                seed = int(get_arg())
            case "--output" | "-o":
                output = get_arg()
            case _:
                print_help()
                exit()
        i+=1
    
    if nodes_count==None:
        nodes_count = 10

    if chromatic_number!=None and clique_size!=None:
        print("""Unfortunately, the algorithm cannot set a chromatic number and a clique size.
              Decide which is more important to you and try again.""")
    
    if output==None:
        print("You have to set an output file. Printing the graphs would be useless")

    graphs = []

    if chromatic_number==None:
        for i in range(amount):
            graph= define_own_graph(nodes_count,edge_density=density,max_clique=clique_size,seed=seed)
            if seed:
                seed+=1
            graphs.append(graph)
    else:
        print("Chromatic number is not yet implemented, sry")
        exit(0)
    
    with open(output,"w") as file:
        output_string = convert_to_text(graphs)
        
        file.write(output_string)

if __name__=="__main__":
    cli()