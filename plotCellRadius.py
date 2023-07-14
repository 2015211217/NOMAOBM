import matplotlib.pyplot as plt
import numpy as np
devices_block = 500
plot_x_number = 7

fig, ax = plt.subplots()

timearray = np.zeros(plot_x_number)
for i in range(plot_x_number):
    timearray[i] = i * devices_block + 250

plt.plot(timearray,[180.,178.53,172.396,153.286,134.666,116.104,99.175],"k-.d",label="NOMA-SM1")
plt.plot(timearray,[180.,178.53,172.396,153.286,134.666,116.104,99.175],"g-.^",label="NOMA-SM2")
plt.plot(timearray,[180.,178.66,172.09,151.795,125.13,101.995,78.82],"r-.h",label="MWFMP[10]")
plt.plot(timearray,[180.,163.224,145.792,125.092,100.155,69.228,31.58],"-.o",label="MPSDA[10]")

# plt.yticks(np.arange(1, 6, step = 4))
font = {'style': 'normal', 'weight': 'bold'}

plt.tick_params(labelsize = 14)
plt.xticks(np.arange(250, 3500, step = 500), fontweight = 'bold')
plt.tick_params(labelsize = 14)
plt.yticks(fontweight = 'bold')

plt.ylim(ymin = int(0))
plt.xlim(xmin = int(250))

plt.grid(b=None, which='major', axis='both')
# plt.title("")
# plt.xlabel("No. of PRBs")
# # plt.xlabel("R (kpbs)")
plt.xlabel("Cell Radius (m)", fontsize = 16, fontweight = 'bold')

plt.ylabel("Average No. of Connected Devices", fontsize = 16, fontweight = 'bold')
# plt.ylabel("Average Runtime (s)", fontsize = 16, fontweight = 'bold')
#, bbox_to_anchor = (num1, ), loc = , borderaxespad =
plt.rcParams.update({'font.size': 14})
plt.legend(frameon=False, loc=9, ncol=2, bbox_to_anchor=(0.5, 1.18), prop=font)

# plt.tight_layout()
plt.savefig('CellRadiusNumber.pdf', format='pdf')
plt.show()
