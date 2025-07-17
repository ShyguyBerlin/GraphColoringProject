import networkx as nx
from random import shuffle
import make_better_coloring as mbc
import greedy as gy

def greedy_no_sort_make_better( G : nx.graph):
  labels = {}
  
  labels = gy.greedy_no_sort(G)
  labels = mbc.make_batter_coloring(G, labels)

  yield labels

def greedy_asc_deg_make_better( G : nx.graph):
    labels={}

    labels = gy.greedy_asc_deg(G)
    labels = mbc.make_batter_coloring(G, labels)
        
    yield labels

def greedy_desc_deg_make_better( G : nx.graph):
    labels={}

    labels = gy.greedy_desc_deg(G)
    labels = mbc.make_batter_coloring(G, labels)
  
    yield labels

def greedy_color_swaps_make_better( G : nx.graph):
    labels = {}
    
    labels = gy.greedy_color_swaps(G)
      
    labels = mbc.make_batter_coloring(G, labels)

    yield labels
