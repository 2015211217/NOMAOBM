import numpy as np
import datetime
import sys
from AddingAlgorithms import deg_count,connecting_count

def harvey_algo1(runs, power_matrix, number_of_subcarriers, number_of_device, number_of_edges_per_device, L, max_PRB, number_of_PRBs, number_slots_per_PRB):
    datetime_runs = 0
    connected_devices = 0
    #The version of code for the journal paper only works for each subcarrier only have one slot
    for t in range(runs):
        start_time = datetime.datetime.now().timestamp()
        # p_list = np.zeros(1, number_of_PRB * number_of_device * number_of_slots_per_PRB)
        p_list = power_matrix[t]
        Q = []
        deg_sub = np.zeros(number_of_subcarriers)
        bestV = -1
        for d in range(number_of_device):
            bestV = -1
            M = []
            Q = np.append(Q, (d, 0))
            P = []
            while (len(Q) != 0):
                w = Q[0]
                Q = np.delete(Q, 0)
                N = []
                if w[1] == 0:
                    for s in range(number_of_subcarriers):
                        if (w[0], s) not in M:
                            N = np.append(N, (s, 0))

                elif w[1] == 1:
                    for d1 in range(number_of_device):
                        if (d1, w[0]) in M:
                            N = np.append(N, (d1, 1))
                    deg_w = deg_count(p_list, number_of_device, w[0], M)
                    if bestV == -1 or deg_w < deg_count(p_list[d * number_of_edges_per_device + int(bestV % number_slots_per_PRB) * L],  bestV, M):
                        bestV = w[0]
                else:
                    print("error during NOMA-SM1")
                ##start handling N
                for n in N:
                    ##现有的都是server nodes，方向为从w[0]到n[0], denote as 0
                    if n[1] == 1:
                        P = np.append(P, (w[0], n[0], 0))
                    else:
                        P = np.append(P, (w[0], n[0], 1))
            ##endwhile reverse the path
            deg_sub[bestV] += deg_sub[bestV] + p_list[d * number_of_edges_per_device + int(bestV % number_slots_per_PRB) * L]
            ###whiles
            v = bestV
            u = -1
            for p in P:
                if p[1] == v and p[2] == 0:
                    u = p[0]
                    M = np.append(M, (u, v)) ##M only directed from u to v, be careful
            while (u != d):
                for p in P:
                    if p[0] == u and p[2] == 1:
                        v = p[1]
                    for m in range(M.size()):
                        if M[m][0] == u and M[m][1] == v:
                            M = np.detele(M, m)
                            break
                for p in P:
                    if p[1] == v and p[2] == 0:
                        u = p[0]
                        M = np.append(M, (u, v))

        connected_devices += connecting_count(M, max_PRB, L, p_list, deg_sub, number_of_device, number_of_PRBs, number_slots_per_PRB, number_of_edges_per_device)
        datetime_runs += datetime.datetime.now().timestamp() - start_time
    return connected_devices / runs, datetime_runs / runs