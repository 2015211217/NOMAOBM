import numpy as np
import datetime
import sys
def harvey_algo1(runs, L, number_of_PRB, max_perPRB, power_matrix, number_of_slots_per_PRB, number_of_device, Xi):
    datetime_runs = 0
    connected_devices = 0
    #The version of code for the journal paper only works for each subcarrier only have one slot
    for t in range(runs):
        start_time = datetime.datetime.now().timestamp()
        # p_list = np.zeros(1, number_of_PRB * number_of_device * number_of_slots_per_PRB)
        p_list = power_matrix[t]
        PRB_power_sequence = np.zeros(number_of_PRB)
        for i in range(number_of_slots_per_PRB * number_of_PRB * number_of_device):
            PRB_i = (i % (number_of_slots_per_PRB * number_of_PRB)) // number_of_slots_per_PRB
            # if L is bigger than 1, you have to handle it
            # the same subcarrier
            p_bool_list = np.zeros(len(p_list))
            p_accumulate = 0
            for k in range((i // (number_of_slots_per_PRB * number_of_PRB)) * (
                    number_of_slots_per_PRB * number_of_PRB),
                           (i // (number_of_slots_per_PRB * number_of_PRB) + 1) * (
                                   number_of_slots_per_PRB * number_of_PRB)):
                if p_bool_list[i] == 1:
                    p_accumulate += p_list[i]

            if ((PRB_power_sequence[PRB_i] + p_accumulate + p_list[i]) < max_perPRB):
                PRB_power_sequence[PRB_i] += p_list[i]
                PRB_power_sequence[PRB_i] += p_accumulate * Xi
                p_bool_list[i] = 1
                connected_devices += 1
                for j in range((i // (number_of_slots_per_PRB * number_of_PRB)) * (
                        number_of_slots_per_PRB * number_of_PRB),
                               (i // (number_of_slots_per_PRB * number_of_PRB) + 1) * (
                                       number_of_slots_per_PRB * number_of_PRB)):
                    p_list[j] = sys.maxsize
                index_slot = (i % (number_of_slots_per_PRB * number_of_PRB))
                for j in range(number_of_device):
                    p_list[j * (number_of_slots_per_PRB * number_of_PRB) + index_slot] = sys.maxsize

        datetime_runs += datetime.datetime.now().timestamp() - start_time
    return connected_devices / runs, datetime_runs / runs