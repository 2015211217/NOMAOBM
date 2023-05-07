import numpy as np
import matplotlib.pyplot as plt
from BestinHindsight import BestHindsight
number_of_device = 1000 #D
number_of_PRB = 10 #S
bandwidth_per_PRB = 180 #kHz
target_datarate_per_device = 20 #kbps

carrier_frequency = 900 #Mhz
subcarrier_bandwidth = 15 #kHz Bs
number_of_subcarrierDevices = number_of_PRB * bandwidth_per_PRB / subcarrier_bandwidth #L

delta = 0.01
UE_gain_dB = -4
indoor_loss_dB = 10
path_loss_dB = 120.9 + 37.6 * np.log(number_of_device / 1000) + UE_gain_dB + indoor_loss_dB
noise_figure_dB = 5
noise_spectral_density_dBHZ = -174
N_noise = noise_spectral_density_dBHZ * subcarrier_bandwidth * np.power(10, noise_figure_dB / 10)


if number_of_subcarrierDevices <= 0 or number_of_device <= 0 or number_of_PRB <= 0 :
    print("EXIT: INVALID INPUT!")
    exit(0)

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
    a = np.random.randint(1, number_of_PRB)
    b = np.random.randint(1, number_of_PRB)
    if a <= b:
        for j in range(a, b + 1):
            for k in range(number_of_subcarrierDevices):
                edge[k + i * number_of_subcarrierDevices * number_of_PRB + j * number_of_subcarrierDevices] = 1
# compose the edge_weight
Xi = np.pow(2, target_datarate_per_device / (number_of_subcarrierDevices * subcarrier_bandwidth)) - 1
mediate_upper = np.zeros((T, number_of_PRB * number_of_subcarrierDevices * number_of_device))
edge_weight = np.zeros((T, number_of_PRB * number_of_subcarrierDevices * number_of_device))
for i in range(T):
    for j in range(number_of_device*number_of_PRB):
        for k in range(number_of_subcarrierDevices):
            mediate_upper[i][j * number_of_subcarrierDevices + k] = N_noise * Xi * np.power(1 + Xi, number_of_device - k + 1)

for i in range(T):
    for j in range(number_of_subcarrierDevices * number_of_device * number_of_PRB):
        edge_weight[i][j] = mediate_upper[i][j] / (distance_fading_T * np.power(path_loss_dB, -1/2))

best_power_sequence = BestHindsight(edge_weight, edge, T, edge_numbers, number_of_device) #works like reward
##plot the result
timearray = ([i + 1] for i in range(T))
plt.xlabel = "T"
plt.ylabel = "Regret"
plt.errorbar(timearray, best_power_sequence)

plt.legend()
plt.show()