# This script is meant to be executed as a CLI tool and may assist in generating graph datasets

from sys import argv
from tools.graph_gen_tools import define_own_graph,convert_to_text, define_own_graph_chromatic, define_own_cograph, apply_modulator
from tools.graph_gen_data_classes import ModulatorData

def print_help():
    print(f"""     Use: {argv[0]} OPTIONS \n
        Options:
        --amount -a <number> : How many graphs shall be created
        --nodes -n <count> : Sets the amount of nodes per graph
        --density -d <edge_density> : Formula to determine the density of edges, can be given as constant or formula
        --max_clique -mc <size> : Guarantees that the maximum clique will be of this size
        --chromatic-number -cn <number> : Sets an UPPER limit to the resulting coloring number
        --cograph -cg <bool> : If True, will create a Cograph and will ignore density, max_clique etc.
        --seed -s <number> : Sets a seed to use for random algorithms
        --output -o <path> : Will write resulting graphs to this file
          
        --modulator-size -ms <count> : Defines the node amount of a modulator, which will be added to each completed graph
        --modulator-density -md <edge_density> : Same as -d but for the modulator and connections with existing nodes
                , leave empty to mimic edge density of original graph
        """)

def cli():
    
    amount = 1
    nodes_count=None
    clique_size=None
    density=None
    chromatic_number=None
    cograph=None
    seed=None
    output=None

    modulator = ModulatorData(None,None)

    def post_gen_alteration(G):
        if modulator.nodes:
            return apply_modulator(G,modulator)
        return G

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
            case "--cograph" | "-cg":
                cograph = bool(get_arg())
            case "--seed" | "-s":
                seed = int(get_arg())
            case "--output" | "-o":
                output = get_arg()
            case "--modulator-size" | "-ms":
                modulator.nodes=int(get_arg())
            case "--modulator-density" |"-md":
                modulator.density=float(get_arg())
            case _:
                print_help()
                exit()
        i+=1
    
    if density==None:
        density = 0.3 # arbitrary
    
    if nodes_count==None:
        nodes_count = 10

    if chromatic_number!=None and clique_size!=None:
        print("""Unfortunately, the algorithm cannot set a chromatic number and a clique size.
              Decide which is more important to you and try again.""")
    
    if output==None:
        print("You have to set an output file. Printing the graphs would be useless")

    graphs = []

    if(cograph == True):
        graph= define_own_cograph(nodes_count)
        if seed:
            seed+=1
        graphs.append(graph)

    elif chromatic_number==None:
        for i in range(amount):
            graph= define_own_graph(nodes_count,edge_density=density,max_clique=clique_size,seed=seed)
            if seed:
                seed+=1
            graphs.append(post_gen_alteration(graph))
    else:
        if(chromatic_number < 2):
            print("Chromatic number is too small")
            exit(0)
        elif(chromatic_number > nodes_count):
            print("Chromatic number is too high")
            exit(0)
        for i in range(amount):
            graph= define_own_graph_chromatic(nodes_count,edge_density=density,chromatic_number=chromatic_number,seed=seed)
            if seed:
                seed+=1
            graphs.append(post_gen_alteration(graph))

        #print("Chromatic number is not yet implemented, sry")
        #exit(0)
    
    with open(output,"w") as file:
        output_string = convert_to_text(graphs)
        
        file.write(output_string)

if __name__=="__main__":
    cli()