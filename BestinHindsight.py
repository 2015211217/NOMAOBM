import numpy as np
from scipy.optimize import linear_sum_assignment

def BestHindsight(edge_weight, edge, T, edge_numbers, number_of_device):
    edge_weight_copy = [[0] * (edge_numbers / number_of_device)] * number_of_device
    loss = [0] * T
    loss_t = 0
    for t in range(T):
        for i in range(edge_numbers):
            edge_weight_copy[i / number_of_device][i % number_of_device] = edge_weight[t][i] * edge[i]

        #finding the best one in hindsight


    rindex, cindex = linear_sum_assignment(edge_weight_copy)

    for i in range(number_of_device):

        result = 0

        result += edge_weight_copy[rindex[i]][cindex[i]]

        loss_t += result
        loss[t] = loss_t

    return loss