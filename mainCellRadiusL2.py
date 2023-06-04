######
#The journal paper: for each subcarrier, there is only one slot. (experiment)
#The conference paper: for each subcarrier, there are several slots.
#####
import cmath
import numpy as np
import matplotlib.pyplot as plt
from Baseline_SDA import Baseline_SDA
from MIPSolution import MIPBranchCutGurobi
from MWFMP import MWFMP
bandwidth_per_PRB = 180*1e3 #Hz
L = 2

subcarrier_bandwidth = 15*1e3 #Hz B

transmission_power_per_PRB = 0.2 #w 23dB

number_of_PRB = 5 #S
target_datarate_per_device = 50*1e3 #kbps
number_of_subcarriers_perPRB = 12 #L * number of subcarriers per PRB
number_of_slots_per_PRB = number_of_subcarriers_perPRB * L
number_of_slots_total = number_of_slots_per_PRB * number_of_PRB

indoor_loss_dB = 10
noise_figure_dB = 5

UE_gain_dB = -4
noise_spectral_density_dBmHZ = -174

N_noise = np.power(10, noise_spectral_density_dBmHZ/10)/1000 * subcarrier_bandwidth * np.power(10, np.power(10, noise_figure_dB / 10) / 10)
# number_of_device_required = min(number_of_device_total, int(2 * number_of_PRB * number_of_slots))
plot_x_number = 7
connected_device_sequence_SDA = np.zeros(plot_x_number)
connected_device_sequence_MWFMP = np.zeros(plot_x_number)
connected_device_sequence_MIP = np.zeros(plot_x_number)
datetime_sequence_SDA = np.zeros(plot_x_number)
datetime_sequence_MIP = np.zeros(plot_x_number)
datetime_sequence_MWFMP = np.zeros(plot_x_number)
runs = 1000
devices_block = 4

for radius_range in [250, 750, 1250, 1750, 2250, 2750, 3250]:
    ##generate the new D, which refers to the
    number_of_device_required = number_of_PRB * number_of_slots_per_PRB
    np.random.seed(2)
    device_distance = np.random.uniform(0, radius_range, (runs, number_of_device_required))

    path_loss_w = np.zeros((runs, number_of_device_required))
    for i in range(runs):
        for j in range(number_of_device_required):
            path_loss_w[i][j] = np.power(10, (120.9 + 37.6 * np.log10(device_distance[i][j] / 1000) + UE_gain_dB + indoor_loss_dB) / 10)

    # path_loss_dB = 120.9 + 37.6 * np.log(number_of_device_required / 1000) + UE_gain_dB + indoor_loss_dB
    if number_of_subcarriers_perPRB <= 0 or number_of_device_required <= 0 or number_of_PRB <= 0:
        print("EXIT: INVALID INPUT!")
        exit(0)

    Xi = np.power(2, target_datarate_per_device /subcarrier_bandwidth ) - 1
    # creating the fading coefficients
    number_of_edges = number_of_device_required * number_of_slots_total

    p_matrix = np.zeros((runs, number_of_edges))
    p_matrix_copy = np.zeros((runs, number_of_edges))
    p_matrix_MWFMP = np.zeros((runs, number_of_edges))
    g_matrix = np.zeros((runs, number_of_edges))

    for t in range(runs):
        #generate data
        np.random.seed(0)
        b_list_real = np.random.randn(int(number_of_edges / L))
        np.random.seed(1)
        b_list_complex = np.random.randn(int(number_of_edges / L))
        b_list = np.zeros(int(number_of_edges / L), dtype=complex)
        b_list_X = np.zeros(int(number_of_edges / L))
        p_list = np.zeros(int(number_of_edges / L))
        # b_list_X = np.abs(np.sort_complex(-1 * b_list_X))
        for i in range(int(number_of_edges / L)):
            b_list[i] = b_list_complex[i] + b_list_complex[i] * cmath.sqrt(-1)
            b_list_X[i] = (np.power(b_list[i].real, 2) + np.power(b_list[i].imag, 2)) / path_loss_w[t][int(i / (number_of_edges/L/ number_of_device_required))]

        #for future usage, still add the multiply of L into the date generation
            for j in range(L):
                g_matrix[t][i * L+j] = b_list_X[i]
            g_matrix[t] = np.abs(np.sort(-1 * g_matrix[t]))

        p_mediate = 0
        for i in range(int(number_of_edges / L)): #p_mediate +
            p_list[i] = Xi * (N_noise / g_matrix[t][i // L])
            p_mediate += p_list[i]
        for i in range(int(number_of_edges / L)):
            for j in range(L):
                p_matrix[t][i*L+j] = p_list[i]
                p_matrix_copy[t][i*L + j] = p_list[i]
                p_matrix_MWFMP[t][i*L + j] = p_list[i]

    print("generation done")
    plot = 0
    connected_device_sequence_SDA[plot], datetime_sequence_SDA[plot] = Baseline_SDA(runs, L, number_of_PRB, transmission_power_per_PRB, p_matrix, number_of_slots_per_PRB, number_of_device_required)
    print("SDA done")
    connected_device_sequence_MWFMP[plot], datetime_sequence_MWFMP[plot] = MWFMP(runs, p_matrix_MWFMP, number_of_device_required, number_of_PRB, transmission_power_per_PRB, number_of_slots_per_PRB, L)
    print("MWFMP done")
    connected_device_sequence_MIP[plot], datetime_sequence_MIP[plot] = MIPBranchCutGurobi(10, L,  p_matrix_copy, g_matrix, number_of_edges, number_of_device_required, bandwidth_per_PRB, number_of_PRB, Xi, N_noise)
    print("MIP done")
    plot += 1
print(connected_device_sequence_SDA)
print(connected_device_sequence_MIP)
print(connected_device_sequence_MWFMP)

##plot the result
# timearray = np.zeros(plot_x_number)
# for i in range(plot_x_number):
#     timearray[i] = (i+1) * devices_block
#
# plt.xlabel = "No. of Contending Devices"
# plt.ylabel = "Average No. of Connected Devices"
# plt.plot(timearray, connected_device_sequence_SDA, "r-.d", label={"MPSDA"})
# plt.plot(timearray, connected_device_sequence_MIP, "b-.h", label={"MIP"})
# plt.legend()
# plt.show()