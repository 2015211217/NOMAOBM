import numpy as np

def deg_count(power_index_v, index_v, M):
    deg = 0
    for m in M:
        if m[1] == index_v:
            deg += deg + power_index_v
    return deg

def connecting_count(M, max_PRB, L, p_list, number_of_PRBs, number_slots_per_PRB, number_of_edges_per_device):
    ##At first, check wether the matching number is over L
    count_v = np.zeros(int(number_slots_per_PRB / L)) #calculate the number of subcarriers
    p_PRB = np.zeros(int(p_list.size()/number_of_PRBs))
    for index_m in range(len(M)):
        count_v[M[index_m][1]] += 1
        if count_v[M[index_m][1]] >= L:
            count_v[M[index_m][1]] -= 1
            M = np.delete(M, index_m)
            index_m -= 1
    ##then consider the constrains, yeah
    for i in range(p_PRB.size()):
        for index_m in range(len(M)):
            if M[index_m][1] >= i * number_slots_per_PRB and M[index_m][1] <= (i+1) * number_slots_per_PRB:
                p_PRB[i] += p_PRB[i] + p_list[M[index_m][0] * number_of_edges_per_device + int(M[index_m][1] % number_slots_per_PRB)]
                if p_PRB[i] > max_PRB:
                    p_PRB[i] -= p_PRB[i] + p_list[M[index_m][0] * number_of_edges_per_device + int(M[index_m][1] % number_slots_per_PRB)]
                    M = np.delete(M, index_m)
                    index_m -= 1

    return M.size()

