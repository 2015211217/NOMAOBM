import matplotlib.pyplot as plt
import numpy as np
devices_block = 20
plot_x_number = 7

fig, ax = plt.subplots()

timearray = np.zeros(plot_x_number)
for i in range(plot_x_number):
    timearray[i] = i * devices_block + 10

plt.plot(timearray, [4.35168353, 4.42678476, 4.375383, 4.23532837, 3.97733568, 4.12813582, 4.02363161], "b-.d" , label="NOMA-SM1")
plt.plot(timearray, [4.04991896, 3.8897451,  4.21934991, 4.14625098, 3.95735613, 3.84597541, 3.7800392], "g-.^", label="NOMA-SM2")
plt.plot(timearray,  [4.39334114, 4.41295296, 4.33287776, 4.42019525, 4.48044347, 4.36003773, 4.36520091], "r-.h", label="MWFMP[6]")
plt.plot(timearray, [1.10353459, 1.15486737, 1.19511459, 1.26595486, 1.21426297, 1.22738546, 1.22984584], "-.o", label="MPSDA[6]")

# plt.yticks(np.arange(1, 6, step = 4))
plt.xticks(np.arange(10, 150, step = 20))
plt.ylim(ymin = 0)
plt.xlim(xmin = 10)

plt.grid(b=None, which='major', axis='both')
# plt.title("Number of connected devices with different R")
# plt.xlabel("No. of PRBs")
plt.xlabel("R (kpbs)")
# plt.xlabel("Cell Radius (m)")
# plt.ylabel("Average No. of Connected Devices")
plt.ylabel("Average Runtime (s)")
#, bbox_to_anchor = (num1, ), loc = , borderaxespad =
plt.legend(frameon=False)

plt.savefig('RTime', format='pdf')
plt.show()
