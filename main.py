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
L = 1

subcarrier_bandwidth = 15*1e3 #Hz B

transmission_power_per_PRB = np.power(10, 23/10)/1000

number_of_PRB = 1 #S
target_datarate_per_device = 20*1e3 #kbps
number_of_subcarriers_perPRB = 12 #L * number of subcarriers per PRB
number_of_slots_per_PRB = number_of_subcarriers_perPRB * L
number_of_slots_total = number_of_slots_per_PRB * number_of_PRB
indoor_loss_dB = 10
noise_figure_dB = 5
radius_range = 500
UE_gain_dB = -4
noise_spectral_density_dBmHZ = -174

N_noise = np.power(10, noise_spectral_density_dBmHZ/10)/1000 * subcarrier_bandwidth * np.power(10, noise_figure_dB / 10)
# number_of_device_required = min(number_of_device_total, int(2 * number_of_PRB * number_of_slots))
plot_x_number = 10
connected_device_sequence_SDA = np.zeros(plot_x_number)
connected_device_sequence_MWFMP = np.zeros(plot_x_number)
connected_device_sequence_MIP = np.zeros(plot_x_number)
datetime_sequence_SDA = np.zeros(plot_x_number)
datetime_sequence_MIP = np.zeros(plot_x_number)
datetime_sequence_MWFMP = np.zeros(plot_x_number)
runs = 1000
devices_block = 4
def path_loss_count(distance):
    return 120.9 + 37.6 * np.log(distance / 1000) \
           + UE_gain_dB + indoor_loss_dB

for contending_devices in range(0, plot_x_number):
    ##generate the new D, which refers to the
    number_of_device_required = (contending_devices+1) * devices_block
    np.random.seed(2)
    device_distance = np.random.uniform(0, radius_range, (runs, number_of_device_required))
    path_loss_db = np.zeros((runs, number_of_device_required))
    for i in range(runs):
        for j in range(number_of_device_required):
            path_loss_db[i][j] = path_loss_count(device_distance[i][j])
    # path_loss_dB = 120.9 + 37.6 * np.log(number_of_device_required / 1000) + UE_gain_dB + indoor_loss_dB

    if number_of_subcarriers_perPRB <= 0 or number_of_device_required <= 0 or number_of_PRB <= 0:
        print("EXIT: INVALID INPUT!")
        exit(0)

    Xi = np.power(2, target_datarate_per_device / (number_of_subcarriers_perPRB * subcarrier_bandwidth)) - 1
    # creating the fading coefficients
    number_of_different_total_slots = number_of_device_required * number_of_subcarriers_perPRB * number_of_PRB

    p_matrix = np.zeros((runs, number_of_different_total_slots * L))
    p_matrix_copy = np.zeros((runs, number_of_different_total_slots * L))
    p_matrix_MWFMP = np.zeros((runs, number_of_different_total_slots * L))
    g_matrix = np.zeros((runs, number_of_different_total_slots * L))

    for t in range(runs):
        #generate data
        np.random.seed(0)
        b_list_real = np.random.randn(number_of_different_total_slots)
        np.random.seed(1)
        b_list_complex = np.random.randn(number_of_different_total_slots)
        b_list = np.zeros(number_of_different_total_slots, dtype=complex)
        b_list_X = np.zeros(number_of_different_total_slots)
        p_list = np.zeros(number_of_different_total_slots)
        # b_list_X = np.abs(np.sort_complex(-1 * b_list_X))
        for i in range(number_of_different_total_slots):
            b_list[i] = b_list_complex[i] + b_list_complex[i] * cmath.sqrt(-1)
        for i in range(number_of_different_total_slots):
            b_list[i] = b_list[i] * np.emath.power(path_loss_db[t][int(i / (number_of_different_total_slots / number_of_device_required))], -0.5)
            b_list_X[i] = np.power(b_list[i].real, 2) + np.power(b_list[i].imag, 2)

        #for future usage, still add the multiply of L into the date generation
        for i in range(number_of_different_total_slots):
            for j in range(L):
                g_matrix[t][i * L+j] = b_list_X[i]
            g_matrix[t] = np.abs(np.sort(-1 * g_matrix[t]))

        p_mediate = 0
        for i in range(number_of_different_total_slots):
            p_list[i] = Xi * (p_mediate + N_noise / g_matrix[t][i // L])
            p_mediate += p_list[i]
        for i in range(number_of_different_total_slots):
            for j in range(L):
                p_matrix[t][i*L+j] = p_list[i]
                p_matrix_copy[t][i*L + j] = p_list[i]
                p_matrix_MWFMP[t][i*L + j] = p_list[i]

    print("generation done")
    number_of_edges = number_of_device_required * number_of_slots_total
    # connected_device_sequence_SDA[contending_devices], datetime_sequence_SDA[contending_devices] = Baseline_SDA(runs, L, number_of_PRB, transmission_power_per_PRB, p_matrix, number_of_slots_per_PRB, number_of_device_required)
    # print("SDA done")
    connected_device_sequence_MWFMP[contending_devices], datetime_sequence_MWFMP[contending_devices] = MWFMP(runs, p_matrix_MWFMP, number_of_device_required, number_of_PRB, transmission_power_per_PRB, number_of_slots_per_PRB)
    print("MWFMP done")
    # connected_device_sequence_MIP[contending_devices], datetime_sequence_MIP[contending_devices] = MIPBranchCutGurobi(10, L,  p_matrix_copy, g_matrix, number_of_edges, number_of_device_required, bandwidth_per_PRB, number_of_PRB, Xi, N_noise)
    # print("MIP done")

# print(connected_device_sequence_SDA)
# print(connected_device_sequence_MIP)
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