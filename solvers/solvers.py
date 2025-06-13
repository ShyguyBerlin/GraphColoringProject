from .greedy import *
from .wigderson import so_called_easy_algorithm,wigdersons_first,wigdersons_first_greedy_color,wigdersons_second,wigdersons_second_log,wigdersons_second_sqrt
from .independent_set_algorithms import berger_rompel
from .Johanson.johanson import johnson
solvers={"greedy": greedy_no_sort,
         "greedy_min":greedy_asc_deg,
         "greedy_max":greedy_desc_deg,
         "greedy_colors":greedy_most_colors,
         "greedy_color_swaps":greedy_color_swaps,
         "so_called_easy":so_called_easy_algorithm,
         "wigdersons_first":wigdersons_first,
         "wigdersons_first_greedy_color":wigdersons_first_greedy_color,
         "wigdersons_second":wigdersons_second,
         "wigdersons_second_log":wigdersons_second_log,
         "wigdersons_second_sqrt":wigdersons_second_sqrt,
         #"berger_rompel": berger_rompel
         "johnson":johnson
         }

def get_solvers():
    return solvers