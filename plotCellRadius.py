import matplotlib.pyplot as plt
import numpy as np
devices_block = 500
plot_x_number = 7

fig, ax = plt.subplots()

timearray = np.zeros(plot_x_number)
for i in range(plot_x_number):
    timearray[i] = i * devices_block + 250

plt.plot(timearray, [4.27512392,4.22248856,3.97007768,3.79542859,3.97520283,3.72477274,2.90444577], "b-.d" , label="NOMA-SM1")
plt.plot(timearray, [3.20938993,2.55819094,2.89988554,2.72167742,2.92369306,2.29781795,2.35866153], "g-.^", label="NOMA-SM2")
plt.plot(timearray, [4.47053027, 4.44357101, 4.3884202,  4.4505935,  4.33564232, 4.42248696,
 4.42452576], "r-.h", label="MWFMP[6]")
plt.plot(timearray, [1.10528242, 1.14227395, 1.22205585, 1.22467608, 1.24817566, 1.25048489, 1.23927374], "-.o", label="MPSDA[6]")

# plt.yticks(np.arange(1, 6, step = 4))
plt.xticks(np.arange(250, 3500, step = 500))
plt.ylim(ymin = int(0))
plt.xlim(xmin = int(250))

plt.grid(b=None, which='major', axis='both')
# plt.title("")
# plt.xlabel("No. of PRBs")
# # plt.xlabel("R (kpbs)")
plt.xlabel("Cell Radius (m)")

# plt.ylabel("Average No. of Connected Devices")
plt.ylabel("Average Runtime (s)")
#, bbox_to_anchor = (num1, ), loc = , borderaxespad =
plt.legend(frameon=False)

plt.savefig('/home/jiang/graphs/CellRadiusTime', format='pdf')
plt.show()
