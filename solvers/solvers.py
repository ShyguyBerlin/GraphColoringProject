from .greedy import *
from .wigderson import so_called_easy_algorithm,wigdersons_first


solvers={"greedy": greedy_no_sort, "greedy_min":greedy_asc_deg, "greedy_max":greedy_desc_deg, "so_called_easy":so_called_easy_algorithm, "wigdersons_first":wigdersons_first}

def get_solvers():
    return solvers