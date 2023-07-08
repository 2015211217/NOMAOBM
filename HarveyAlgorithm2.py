import numpy as np
import datetime
from AddingAlgorithms import deg_count, connecting_count

def find_cost_reduced_path(M):
    P = []

    return np.append[P, (-1, -1)], M

def harvey_algo2(runs, power_matrix, number_of_subcarriers, number_of_device, number_of_edges_per_device, L, max_PRB, number_of_PRB, number_slots_per_PRB):
    datetime_runs = 0
    connected_devices = 0
    for t in range(runs):
        start_time = datetime.datetime.now().timestamp()
        p_list = power_matrix[t]
        M = []
        degV = np.zeros(number_of_subcarriers)
        for d in range(number_of_device):
            for v in range(number_of_subcarriers):
                degV[v] += degV[v] + p_list[d * number_of_edges_per_device + int(v % number_slots_per_PRB) * L]
                M = np.append(M, (d, v))
        ## init
        P, M = find_cost_reduced_path(M)


        connected_devices += connecting_count(M, max_PRB, L, p_list, number_of_device, number_of_PRB,
                                                  number_slots_per_PRB, number_of_edges_per_device)
        datetime_runs += datetime.datetime.now().timestamp() - start_time
    return connected_devices / runs, datetime_runs / runs