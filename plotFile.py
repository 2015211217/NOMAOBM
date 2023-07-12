import matplotlib.pyplot as plt
import numpy as np
devices_block = 1
plot_x_number = 5

fig, ax = plt.subplots()

timearray = np.zeros(plot_x_number)
for i in range(plot_x_number):
    timearray[i] = (i+1) * devices_block

plt.plot(timearray, [ 0.15719986,  1.17330567,  4.40705655, 10.80946397, 22.41047872], "b-.d" , label="NOMA-SM1")
plt.plot(timearray, [0.15015807, 1.15463812, 2.77190659, 7.50896047, 16.5554567], "g-.^", label="NOMA-SM2")
plt.plot(timearray, [ 0.15238817, 1.15527844, 4.22135728, 10.58685287, 23.37039524], "r-.h", label="MWFMP[6]")
plt.plot(timearray, [0.01215805, 0.77828554, 1.26106226, 2.71863132, 6.39005792], "-.o", label="MPSDA[6]")

# plt.yticks(np.arange(1, 6, step = 4))
plt.xticks(np.arange(1, 6, step = 1))
plt.ylim(ymin = 0)
plt.xlim(xmin = 1)

plt.grid(b=None, which='major', axis='both')
plt.title("")
plt.xlabel("No. of PRBs")
# plt.xlabel("R (kpbs)")
# plt.xlabel("Cell Radius (m)")

# plt.ylabel("Average No. of Connected Devices")
plt.ylabel("Average Runtime (s)")
#, bbox_to_anchor = (num1, ), loc = , borderaxespad =
plt.legend(frameon=False)
plt.savefig('PRBTime', format='pdf')
plt.show()
