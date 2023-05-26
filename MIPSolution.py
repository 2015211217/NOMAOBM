import numpy as np
import gurobipy
import datetime

def MIPBranchCutGurobi(runs, L, power_matrix, pathloss_matrix, number_of_edges, number_of_devices, power_max, number_of_PRBs, Xi, Noise):
    datetime_runs = 0
    connected_devices = 0
    flag = 1
    for t in range(runs):
        start_time = datetime.datetime.now().timestamp()
        power_list = power_matrix[t]
        pathloss_list = pathloss_matrix[t]

        if flag == 1:
            MODEL = gurobipy.Model()
            X = MODEL.addVars(number_of_edges, vtype=gurobipy.GRB.BINARY)
            MODEL.update()
            obj = gurobipy.LinExpr()
            for i in range(number_of_edges):
                obj += X[i]
            MODEL.setObjective(obj, gurobipy.GRB.MAXIMIZE)

            for i in range(number_of_devices):  # one device can only connect to one slot
                MODEL.addConstr(sum(X[int(i * (number_of_edges / number_of_devices) + j)] for j in
                                    range(int(number_of_edges / number_of_devices))) <= 1)
            for i in range(int(number_of_edges / number_of_devices)):  # one slot can only connect to one device
                MODEL.addConstr(
                    sum(X[int(j * (number_of_edges / number_of_devices) + i)] for j in range(number_of_devices)) <= 1)

            # one subcarrier can only hold L devices, automatically satisfied
            number_slots_per_PRB = number_of_edges / (number_of_devices * number_of_PRBs)
            for i in range(number_of_PRBs):
                MODEL.addConstr(sum(
                    X[int(k * (number_of_edges / number_of_devices) + i * number_slots_per_PRB + j)]
                    for j, k in zip(range(int(number_slots_per_PRB)), range(int(number_of_devices)))) <= power_max)
            for i in range(number_of_edges):
                MODEL.addConstr(X[i] * pathloss_list[i] * (power_list[i] - Xi * sum(
                    power_list[j] * X[j] for j in range(0, int(i - number_of_edges / number_of_devices))))
                                >= Xi * Noise * X[i])
            MODEL.update()

            # MODEL.setParam('NonConvex', 2)

            MODEL.optimize()
            GetX = MODEL.getAttr('X', X)
            for i in range(number_of_edges):
                connected_devices += int(GetX[i])

        print(connected_devices / (t+1))
        datetime_runs += datetime.datetime.now().timestamp() - start_time

    return connected_devices / runs, datetime_runs / runs