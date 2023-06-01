import datetime
import numpy as np
from scipy.optimize import linear_sum_assignment
import sys

def MWFMP(runs, power_matrix, number_of_device, number_of_PRBs, Pmax, number_of_slots_perPRB):
    datetime_runs = 0
    connected_devices = 0
    #The version of code for the journal paper only works for each subcarrier only have one slot
    for t in range(runs):
        start_time = datetime.datetime.now().timestamp()
        p_list = power_matrix[t]
        ####the minimum weight matching found
        p_matrix = np.zeros((number_of_device, int(len(p_list) / number_of_device)))
        for i in range(number_of_device):
            for j in range(int(len(p_list) / number_of_device)):
                p_matrix[i][j] = -1 * p_list[i * int(len(p_list) / number_of_device) + j]

        rindex, cindex = linear_sum_assignment(p_matrix) #chose the minimum one...

        #rindex -> row cindex -> line
        ####truncation what will happen when the number of device exceed the slot number?
        ##build a chosen matrix, it would be easier
        p_chosen_matrix = np.zeros((number_of_device, int(len(p_list) / number_of_device)))
        for i in range(len(rindex)):
            p_chosen_matrix[rindex[i]][cindex[i]] = -1 * p_matrix[rindex[i]][cindex[i]]

        Power_PRB = np.zeros(number_of_PRBs)
        for PRB in range(number_of_PRBs):
            #calculate the total power per block, work on p_matrix
            for i in range(number_of_device):
                for j in range(PRB * number_of_slots_perPRB, (PRB + 1) * number_of_slots_perPRB):
                    Power_PRB[PRB] += p_chosen_matrix[i][j]

            while(Power_PRB[PRB] > Pmax):
                #find the minimum in this PRB and exclude it
                #right now the usage of power is not considered
                p_min = sys.maxsize
                row_min = -1
                line_min = -1
                for row in rindex:
                    for line in cindex:
                        if (p_chosen_matrix[row][line] < p_min and p_chosen_matrix[row][line] != 0):
                            p_min = p_chosen_matrix[row][line]
                            row_min = row
                            line_min = line
                Power_PRB[PRB] -= p_chosen_matrix[row_min][line_min]
                p_chosen_matrix[row_min][line_min] = 0
        connected_devices += np.count_nonzero(p_chosen_matrix)

        datetime_runs += datetime.datetime.now().timestamp() - start_time
    return connected_devices / runs, datetime_runs / runs