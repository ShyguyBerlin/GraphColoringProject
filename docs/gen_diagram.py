import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

import pandas as pd
import plotly.express as px

def make_diagram(input:str,output:str,prop_to_plot="colors_avg",solver_whitelist=[],solver_blacklist=[],graphset_whitelist=[],graphset_blacklist=[],graphset_wildcard_whitelist=[],graphset_wildcard_blacklist=[],zoom_to=0):
    
    # Load CSV
    df = pd.read_csv(input)

    # Filter based on whitelist
    if len(solver_whitelist)>0:
        df = df[df["solver"].isin(solver_whitelist)]
    if len(graphset_whitelist)>0:
        df = df[df["graph_set"].isin(graphset_whitelist)]

    if len(solver_blacklist)>0:
        df = df[~df["solver"].isin(solver_blacklist)]
    if len(graphset_blacklist)>0:
        df = df[~df["graph_set"].isin(graphset_whitelist)]

    if len(graphset_wildcard_whitelist)>0:
        graphset_wildcard_whitelist = ["("+x+")" for x in graphset_wildcard_whitelist]
        
        pattern = "|".join(graphset_wildcard_whitelist)

        df = df[df["graph_set"].str.contains(pattern,case=False)]
    
    if len(graphset_wildcard_blacklist)>0:
        graphset_wildcard_blacklist = ["("+x+")" for x in graphset_wildcard_blacklist]
        
        pattern = "|".join(graphset_wildcard_blacklist)

        df = df[~df["graph_set"].str.contains(pattern,case=False)]

    # Plot: X = solver (categorical), Y = value, Color = metadata
    fig = px.scatter(
        df,
        x="solver",
        y=prop_to_plot,
        color="graph_set",   # metadata column
        hover_data=df.columns,  # show all info on hover
    )

    # Fix zoom/offset (set constant Y range, e.g., 0–400)
    if zoom_to!=0:
        fig.update_yaxes(range=[0, zoom_to])

    fig.update_xaxes(title=None )

    fig.update_layout(margin=dict(t=5,l=20))

    # Write figure to disk
    fig.write_image(output,scale=2,height=362,width=512)

import os

#   make_diagram(input:str,output:str,solver_whitelist=[],solver_blacklist=[],graphset_whitelist=[],graphset_blacklist=[],zoom_to=0)
if __name__=="__main__":

    if not os.path.exists("docs/diagrams"):
        os.makedirs("docs/diagrams")

    make_diagram("docs/data/generic_test_merger_focus.csv","docs/diagrams/merger_pic1.png",graphset_wildcard_whitelist=["_50n"],solver_blacklist=["merge_recolor_color_swaps"])
    make_diagram("docs/data/generic_test_merger_focus.csv","docs/diagrams/merger_pic2.png",graphset_wildcard_whitelist=["_300n"],solver_blacklist=["merge_trivial","merge_recolor_color_swaps"])
    make_diagram("docs/data/generic_test_merger_focus.csv","docs/diagrams/merger_pic3.png",graphset_wildcard_whitelist=["_300n"],solver_blacklist=["merge_trivial","greedy_max","merge_recolor_bf"])
    make_diagram("docs/data/generic_test_merger_focus.csv","docs/diagrams/merger_pic4.png",graphset_wildcard_whitelist=["_300n"],solver_whitelist=["greedy_color_swaps","merge_recolor_color_swaps"],prop_to_plot="exec_time_avg")
    make_diagram("docs/data/generic_test_merger_focus.csv","docs/diagrams/merger_pic5.png",graphset_wildcard_whitelist=["_300n"],solver_whitelist=["greedy_max","merge_recolor"],prop_to_plot="exec_time_avg")

    make_diagram("docs/data/generic_test_greedy.csv","docs/diagrams/greedy_pic1.png",graphset_wildcard_whitelist=["_300n"],solver_blacklist=["greedy_color_swaps"])
    make_diagram("docs/data/generic_test_greedy.csv","docs/diagrams/greedy_pic2.png",graphset_wildcard_whitelist=["_300n"],solver_whitelist=["greedy_max","","greedy_color_swaps"])
