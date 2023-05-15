######
#The journal paper: for each subcarrier, there is only one slot. (experiment)
#The conference paper: for each subcarrier, there are several slots.
#####

import numpy as np
import matplotlib.pyplot as plt
from Baseline_SDA import Baseline_SDA
from MIPSolution import MIPBranchCutGurobi
bandwidth_per_PRB = 180*1e3 #kHz
subcarrier_bandwidth = 15*1e3 #kHz Bs
carrier_frequency = 900*1e3 #Mhz
transmission_power_per_PRB = np.power(10, 23/10)
number_of_PRB = 10 #S
target_datarate_per_device = 20 #kbps
L = 1
number_of_subcarriers_perPRB = int(number_of_PRB * bandwidth_per_PRB / subcarrier_bandwidth) #L * number of subcarriers per PRB
number_of_slots_per_PRB = number_of_subcarriers_perPRB * L
number_of_slots_total = number_of_slots_per_PRB * number_of_PRB

indoor_loss_dB = 10
noise_figure_dB = 5
UE_gain_dB = -4
noise_spectral_density_dBHZ = -174
N_noise = noise_spectral_density_dBHZ * subcarrier_bandwidth * np.power(10, noise_figure_dB / 10)

# number_of_device_required = min(number_of_device_total, int(2 * number_of_PRB * number_of_slots))
connected_device_sequence_SDA, connected_device_sequence_MIP = np.zeros(10)
datetime_sequence_SDA, datetime_sequence_MIP = np.zeros(10)

for contending_devices in range(1, 10):
    number_of_device_required = contending_devices * 100
    path_loss_dB = 120.9 + 37.6 * np.log(number_of_device_required / 1000) + UE_gain_dB + indoor_loss_dB
    if number_of_subcarriers_perPRB <= 0 or number_of_device_required <= 0 or number_of_PRB <= 0 :
        print("EXIT: INVALID INPUT!")
        exit(0)
    runs = 1000
    Xi = np.power(2, target_datarate_per_device / (number_of_subcarriers_perPRB * subcarrier_bandwidth)) - 1
    # creating the fading coefficients
    number_of_different_total_slots = number_of_device_required * number_of_subcarriers_perPRB * number_of_PRB
    p_matrix, g_matrix = np.zeros((runs, number_of_different_total_slots))

    for t in range(runs):
        #generate data
        b_list = np.random.randn(number_of_different_total_slots, 2).view(np.complex128)
        b_list_X = np.zeros(number_of_different_total_slots)
        p_list = np.zeros(number_of_different_total_slots)
        for i in range(number_of_different_total_slots):
            b_list_X[i] = np.power(np.abs(b_list.flatten()[i] * np.power(path_loss_dB, 1 / 2)), 2)
        b_list = np.abs(np.sort_complex(-1 * b_list))
        #for future usage, still add the multiply of L into the date generation
        for i in range(number_of_different_total_slots):
            for j in range(L):
                g_matrix[t][i*L+j] = b_list[i]

        p_mediate = 0
        for i in range(number_of_device_required):
            p_list[i] = Xi * (p_mediate + N_noise / b_list[i])
            p_mediate += p_list[i]
        for i in range(number_of_different_total_slots):
            for j in range(L):
                p_matrix[t][i*L+j] = p_list[i]

    number_of_edges = number_of_device_required * number_of_slots_total
    connected_device_sequence_SDA[contending_devices], datetime_sequence_SDA[contending_devices] = Baseline_SDA(runs, number_of_PRB, transmission_power_per_PRB, p_matrix, number_of_slots_per_PRB, number_of_device_required)
    connected_device_sequence_MIP[contending_devices], datetime_sequence_MIP[contending_devices] = MIPBranchCutGurobi(runs, p_matrix,g_matrix, number_of_edges, number_of_device_required, bandwidth_per_PRB, number_of_PRB, Xi, N_noise)



##plot the result
timearray = ([i + 1] * 100 for i in range(10))

plt.xlabel = "No. of Contending Devices"
plt.ylabel = "Average No. of Connected Devices"
plt.errorbar(timearray, connected_device_sequence_SDA)
plt.errorbar(timearray, connected_device_sequence_MIP)

plt.legend()
plt.show()