import numpy as np
import datetime
from AddingAlgorithms import deg_count, connecting_count

def find_cost_reduced_path(M, P, v_index, number_of_devices, number_of_servers, degV, S, root):
    # DFS的逻辑
    matchedNeighbors_v = []
    for m in M:
        if m[1] == v_index:
            matchedNeighbors_v = matchedNeighbors_v.append(m[0])
    for u in matchedNeighbors_v:
        P = P.append((u, v_index, 1))#1 means the edge is from v to u
        unmatched_u = []
        for k in range(number_of_servers):
            unmatched_u = unmatched_u.append(k)
        for i in range(number_of_devices):
            for m in M:
                if m[0] == u:
                    unmatched_u = np.delete(unmatched_u, m[1])
        for w in unmatched_u:
            if w not in S or degV[w] > degV[v_index]:
                continue
            S = np.delete(S, w)
            P = P.append((u, w, 0))
            if degV[w] < degV[root]:
                return P, M, S
    #remove the original parent u
            P_return, M_return, S_return = find_cost_reduced_path(M, P, w, number_of_devices, number_of_servers, degV, S, root)
    return np.append[P, (-1, -1)], M

def harvey_algo2(runs, power_matrix, number_of_subcarriers, number_of_device, number_of_edges_per_device, L, max_PRB, number_of_PRB, number_slots_per_PRB):
    datetime_runs = 0
    connected_devices = 0
    for t in range(runs):
        start_time = datetime.datetime.now().timestamp()
        p_list = power_matrix[t]
        M = []
        P = []
        S = []
        for i in range(number_of_subcarriers):
            S = S.append(i)
        degV = np.zeros(number_of_subcarriers)
        for d in range(number_of_device):
            for v in range(number_of_subcarriers):
                degV[v] += degV[v] + p_list[d * number_of_edges_per_device + int(v % number_slots_per_PRB) * L]
                M = np.append(M, (d, v))
        ## init
        root = 0
        while(number_of_device * number_of_edges_per_device):
            S = np.delete(S, root)
            P, M, S = find_cost_reduced_path(M, P, 0, number_of_device, number_of_subcarriers, degV, S, root)
            if P[0] == -1:
                break
            else:
                for path in P:
                    if (path[2] == 0):
                        M = M.append((path[0],path[1]))
                        #d * number_of_edges_per_device + int(bestV % number_slots_per_PRB) * L
                        degV[path[1]] += degV[path[1]] + p_list[path[0] * number_of_edges_per_device + int(path[1] % number_slots_per_PRB) * L]
                    else:
                        M = np.delete(M, (path[0], path[1]))
                        degV[path[1]] -= degV[path[1]] + p_list[path[0] * number_of_edges_per_device + int(path[1] % number_slots_per_PRB) * L]

                P = []
                max_deg_index = 0
                for k in range(number_of_subcarriers):
                    if degV[k] > degV[max_deg_index] and k in S:
                        max_deg_index = k
                root = max_deg_index

            #find the cost reduces path, adjust all the inputs based on it.
        connected_devices += connecting_count(M, max_PRB, L, p_list, number_of_device, number_of_PRB,
                                                  number_slots_per_PRB, number_of_edges_per_device)
        datetime_runs += datetime.datetime.now().timestamp() - start_time
    return connected_devices / runs, datetime_runs / runs