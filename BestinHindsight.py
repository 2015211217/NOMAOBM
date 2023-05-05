import numpy as np

def BestHindsight(distance_fading_T,edge, T, edge_numbers):
    power_of_devices_T = [0] * T
    power_of_devices = 0
    distance_fading = [0] * edge_numbers #full-information

    for t in range(T):
        distance_fading = distance_fading_T[t]
        #transform distance_fading into power level

        #finding the best one in hindsight

