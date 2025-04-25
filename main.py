import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import io
import base64
from js import document
from random import shuffle,randint
import asyncio
from solvers.greedy import *

rseed=randint(0,10000)

def draw_graph(graph, colors, labels):
    # Assign colors to nodes
    node_colors = [colors[n] if n in colors.keys() else 'grey' for n in graph.nodes()]

    # Draw the graph to a buffer
    plt.figure(figsize=(8, 8))
    nx.draw(graph,pos = nx.drawing.layout.spring_layout(graph,seed=rseed), with_labels=True, node_color=node_colors, labels=labels)
    plt.figtext(0.5,0.05,f"Used {max(list(labels.values()))} colors to color the graph",fontsize=22,horizontalalignment='center',verticalalignment='top')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    return buf

async def solve_graph(G : nx.graph, solver):
    # Sample graph coloring logic
    
    available_colors = list(mcolors.CSS4_COLORS.keys())
    shuffle(available_colors)

    async for labels in solver(G):
        colors = {node: available_colors[labels[node]] if node in labels else 'grey' for node in G.nodes()}
        buf=draw_graph(G,colors,labels)

        # Convert to base64 and display in HTML
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode("utf-8")
        img_element = f"<img src='data:image/png;base64,{img_str}'/>"
        document.getElementById("graph-container").innerHTML = img_element
        
        await asyncio.sleep(0.1)

def generate_graph(method):
    match(method):
        case _:
            return nx.cycle_graph(31)

def start_solver(event):
    stop_solver(event)
    global current_draw_task
    print(event)
    selected_solver = document.getElementById("solver_select").value

    selected_graph = document.getElementById("graph_select").value

    solvers={"greedy": greedy_no_sort, "greedy_min":greedy_asc_deg, "greedy_max":greedy_desc_deg}
    G = generate_graph(selected_graph)

    current_draw_task = asyncio.create_task(solve_graph(G,solvers[selected_solver]))

def stop_solver(event):
    global current_draw_task
    try:
        if current_draw_task:
            current_draw_task.cancel()
            current_draw_task = None
    except:
        print("There was nothing to stop")


