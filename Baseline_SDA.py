import numpy as np
import datetime

def Baseline_SDA(runs, number_of_PRB, max_perPRB, power_matrix, number_of_slots_per_PRB, number_of_device):
    datetime_runs = 0
    connected_devices = 0
    for t in range(runs):
        start_time = datetime.datetime.now()
        current_device_index = 0
        p_list = power_matrix[t]
        for i in range(number_of_PRB):
            current_power = 0
            for j in range(number_of_slots_per_PRB):
                if current_power + p_list[current_device_index] <= max_perPRB and connected_devices <= number_of_device:
                    #assign device to the subcarrier j
                    current_power += p_list[current_device_index]
                    current_device_index += 1
                else:
                    break

        datetime_runs += datetime.datetime.now() - start_time
    return connected_devices / runs, datetime_runs / runs