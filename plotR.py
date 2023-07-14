import matplotlib.pyplot as plt
import numpy as np
devices_block = 20
plot_x_number = 7

fig, ax = plt.subplots()

timearray = np.zeros(plot_x_number)
for i in range(plot_x_number):
    timearray[i] = i * devices_block + 10

plt.plot(timearray,[180.,177.94,176.865,176.98,176.295,175.505,174.115],"k-.d",label="NOMA-SM1")
plt.plot(timearray,[180.,177.94,176.865,176.98,176.295,175.505,174.115],"g-.^",label="NOMA-SM2")
plt.plot(timearray,[180.,178.53,172.396,160.286,143.666,122.104,95.175],"r-.h",label="MWFMP[10]")
plt.plot(timearray,[163.92,155.58,140.38,122.35,106.325,90.55,79.295],"-.o",label="MPSDA[10]")

# plt.yticks(np.arange(1, 6, step = 4))
plt.tick_params(labelsize = 14)
plt.xticks(np.arange(10, 150, step = 20), fontweight = 'bold')
plt.tick_params(labelsize = 14)
plt.yticks(fontweight = 'bold')

plt.ylim(ymin = 75)
plt.xlim(xmin = 10)

plt.grid(b=None, which='major', axis='both')
# plt.title("Number of connected devices with different R")
# plt.xlabel("No. of PRBs", fontsize = 16, fontweight = 'bold')
plt.xlabel("R (kpbs)", fontsize = 16, fontweight = 'bold')
# plt.xlabel("Cell Radius (m)")
plt.ylabel("Average No. of Connected Devices", fontsize = 16, fontweight = 'bold')
# plt.ylabel("Average Runtime (s)", fontsize = 16, fontweight = 'bold')
#, bbox_to_anchor = (num1, ), loc = , borderaxespad =

plt.rcParams.update({'font.size': 14})
font = {'style': 'normal', 'weight': 'bold'}
plt.legend(frameon=False, loc=9, ncol=2, bbox_to_anchor=(0.5, 1.18), prop=font)

plt.savefig('R.pdf', format='pdf')
plt.show()
