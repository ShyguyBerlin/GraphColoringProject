import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx
import io
import base64
from js import document
from random import shuffle,randint

rseed=randint(0,10000)

all_colors = list(mcolors.CSS4_COLORS.keys())
shuffle(all_colors)

def draw_graph(graph, colors, labels):
    # Assign colors to nodes
    node_colors = [colors[n] if n in colors.keys() else 'grey' for n in graph.nodes()]

    # Draw the graph to a buffer
    plt.figure(figsize=(8, 8),clear=True)
    nx.draw(graph,pos = nx.drawing.layout.spring_layout(graph,seed=rseed), with_labels=True, node_color=node_colors, labels=labels)
    buf = io.BytesIO()
    plt.savefig(buf, format='png',transparent=True)
    plt.close()
    return buf

def print_graph(graph,labels):
    colors = {node: all_colors[labels[node]] if node in labels else 'grey' for node in graph.nodes()}
    buf=draw_graph(graph,colors,labels)
    # Convert to base64 and display in HTML
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    img_element = document.getElementById("graph-img")
    if img_element is None:
        # Create img only once
        img_element = document.createElement("img")
        img_element.id = "graph-img"
        document.getElementById("graph-container").appendChild(img_element)

    # Update only the image source
    img_element.src = f"data:image/png;base64,{img_str}"

def get_delay_selection():
    return float(document.getElementById("delay-range").value)/100.0

def get_solver_selection():
    return document.getElementById("solver_select").value

def get_graph_selection():
    return document.getElementById("graph_select").value