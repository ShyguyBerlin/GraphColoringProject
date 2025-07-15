from .greedy import *
from .wigderson import so_called_easy_algorithm,wigdersons_first,wigdersons_first_greedy_color,wigdersons_second,wigdersons_second_log,wigdersons_second_sqrt, widgersons_first_and_elim_colors, widgersons_second_and_elim_colors
from .independent_set_algorithms import berger_rompel
from .Johanson.johanson import johnson
from .own_solver import simulated_solver
from .flow import flow_trivial,flow_merge,flow_merge_bf

from collections.abc import Callable

# Data class so we can provide more info on an algorithm before executing it
class Solver:
    def __init__(self,solver_algorithm : Callable[[nx.Graph],None], required_info: list[str]):
        self.func=solver_algorithm
        self.dependencies=required_info

# Dict of all available Solving algorithms; when you add a solver, also add it here!
solvers={"greedy": Solver(greedy_no_sort,[]),
         "greedy_min": Solver(greedy_asc_deg,[]),
         "greedy_max": Solver(greedy_desc_deg,[]),
         "greedy_colors": Solver(greedy_most_colors,[]),
         "greedy_color_swaps": Solver(greedy_color_swaps,[]),
         "so_called_easy": Solver(so_called_easy_algorithm,[]),
         "wigdersons_first": Solver(wigdersons_first,[]),
         "wigdersons_first_greedy_color": Solver(wigdersons_first_greedy_color,[]),
         "wigdersons_second": Solver(wigdersons_second,["chromatic-number"]),
         "wigdersons_second_log": Solver(wigdersons_second_log,[]),
         "wigdersons_second_sqrt": Solver(wigdersons_second_sqrt,[]),
         "berger_rompel": Solver(berger_rompel,["chromatic-number"]),
         "johnson": Solver(johnson,[]),
         "sim_solver": Solver(simulated_solver,[]),
         "flow_trivial": Solver(flow_trivial,[]),
         "flow_merge": Solver(flow_merge,[]),
         "flow_merge_bf": Solver(flow_merge_bf,[]),
         "greedy_min_and_elim_colors": Solver(greedy_asc_deg_and_elim_colors,[]),
         "greedy_max_and_elim_colors": Solver(greedy_desc_deg_and_elim_colors,[]),
         "greedy_elim_colors": Solver(greedy_elim_colors,[]),
         "greedy_elim_colors_all_paths": Solver(greedy_elim_colors_all_paths,[]),
         "greedy_color_swaps_and_elim_colors": Solver(greedy_color_swaps_and_elim_colors,[]),
         "aus_3_mach_2": Solver(aus_3_mach_2,[]),
         "aus_3_mach_2_it": Solver(aus_3_mach_2_it,[]),
         "aus_3_mach_2_elim": Solver(aus_3_mach_2_elim,[]),
         "aus_3_mach_2_elim_it": Solver(aus_3_mach_2_elim_it,[]),
         "elim_colors_basic": Solver(elim_colors_basic,[]),
         "wigdersons_first_and_elim_colors": Solver(widgersons_first_and_elim_colors,[]),
         "wigdersons_second_and_elim_colors": Solver(widgersons_second_and_elim_colors,[])
         }

# Get all solvers without dependencies
def get_generic_solvers():
    return {k : v for k, v in solvers.items() if len(v.dependencies)==0}

# get all solvers
def get_solvers():
    return solvers