from .greedy import *
from .wigderson import so_called_easy_algorithm,wigdersons_first,wigdersons_second


solvers={"greedy": greedy_no_sort, "greedy_min":greedy_asc_deg, "greedy_max":greedy_desc_deg, "greedy_colors":greedy_most_colors, "so_called_easy":so_called_easy_algorithm, "wigdersons_first":wigdersons_first,"wigdersons_second":wigdersons_second}

def get_solvers():
    return solvers