import numpy as np
import matplotlib.pyplot as plt
from BestinHindsight import BestHindsight
number_of_device = 2 #D
number_of_PRB = 10 #S
bandwidth_per_PRB = 180 #kHz
number_of_subcarrierDevices = 4 #L
target_datarate_per_device = 20 #kbps
carrier_frequency = 900 #Mhz
subcarrier_bandwidth = 15 #kHz
delta = 0.01

T = 1000
#bs_d generate, based on the paper of Li Shuai
distance_fading_T = np.zeros((T, number_of_PRB * number_of_subcarrierDevices * number_of_device))
distance_fading_T_2 = np.zeros((T, number_of_PRB * number_of_subcarrierDevices * number_of_device))
edge_numbers = number_of_PRB * number_of_subcarrierDevices * number_of_device
np.random.seed(0)
for j in range(T):
    for i in range(number_of_PRB * number_of_device):
        distance_fading_T[j][i * number_of_subcarrierDevices] = np.random.normal()
        for k in range(number_of_subcarrierDevices):
            distance_fading_T[j][i * number_of_subcarrierDevices + k] = distance_fading_T[j][i * number_of_subcarrierDevices]

period = 0
for i in range(T):
    for j in range(number_of_device):
        for k in range(number_of_PRB):
            distance_fading_T_2[i][j * number_of_PRB * number_of_subcarrierDevices + k * number_of_subcarrierDevices] = 0.95 - delta * (period + k)
            for l in range(number_of_subcarrierDevices):
                distance_fading_T_2[i][
                    j * number_of_PRB * number_of_subcarrierDevices + k * number_of_subcarrierDevices + l] = distance_fading_T_2[i][
                    j * number_of_PRB * number_of_subcarrierDevices + k * number_of_subcarrierDevices]
    period += 1

for i in range(T):
    if (i <= T/2):
        if (i % 2 == 0):
            for j in range(edge_numbers):
                distance_fading_T[i][j] = distance_fading_T_2[i][j]
    else:
        if (i % 2 == 1):
            for j in range(edge_numbers):
                distance_fading_T[i][j] = distance_fading_T_2[i][j]

#constract the graph based on the edges
edge = np.zeros(number_of_subcarrierDevices * number_of_device * number_of_PRB)

for i in range(number_of_device):
    np.random.seed(i)
    a = np.random.randint(0, number_of_PRB)
    b = np.random.randint(0, number_of_PRB)
    if a <= b:
        for j in range(a, b + 1):
            for k in range(number_of_subcarrierDevices):
                edge[k + i * number_of_subcarrierDevices * number_of_PRB + j * number_of_subcarrierDevices] = 1

best_power_sequence = BestHindsight(distance_fading_T, edge, T, edge_numbers) #works like reward
