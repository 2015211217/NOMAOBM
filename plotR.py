import matplotlib.pyplot as plt
import numpy as np
devices_block = 20
plot_x_number = 7
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

fig, ax = plt.subplots()

timearray = np.zeros(plot_x_number)
for i in range(plot_x_number):
    timearray[i] = i * devices_block + 10

# plt.plot(timearray,[180.,177.94,176.865,176.98,176.295,175.505,174.115],"k-.d",label="NOMA-SM1")
# plt.plot(timearray,[180.,177.94,176.865,176.98,176.295,175.505,174.115],"g-.^",label="NOMA-SM2")
# plt.plot(timearray,[180.,178.53,172.396,160.286,145.666,130.104,114.175],"r-.h",label="MWFMP[16]")
# plt.plot(timearray,[163.92,155.58,140.38,125.35,110.325,94.55,79.295],"-.o",label="MPSDA[16]")
#
plt.plot(timearray,[3.55472338,3.69818798,3.54405466,3.43226908,3.47257302,3.53895019,3.31894549],"k-.d",label="NOMA-SM1")
plt.plot(timearray,[2.50811153,2.47923275,2.49292179,2.66359126,2.68210476,2.77029054,2.54771847],"g-.^",label="NOMA-SM2")
plt.plot(timearray,[4.39334114,4.41295296,4.33287776,4.42019525,4.48044347,4.36003773,4.36520091],"r-.h",label="MWFMP[16]")
plt.plot(timearray,[1.10353459,1.15486737,1.19511459,1.26595486,1.21426297,1.22738546,1.22984584],"-.o",label="MPSDA[16]")

# plt.yticks(np.arange(1, 6, step = 4))
plt.tick_params(labelsize = 14)
plt.xticks(np.arange(10, 150, step = 20), fontweight = 'bold')
plt.tick_params(labelsize = 14)
plt.yticks(fontweight = 'bold')

# plt.ylim(ymin = 75)
plt.ylim(ymin = 0)
plt.xlim(xmin = 10)

plt.grid(b=None, which='major', axis='both')
# plt.title("Number of connected devices with different R")
# plt.xlabel("No. of PRBs", fontsize = 16, fontweight = 'bold')
plt.xlabel("R (kpbs)", fontsize = 16, fontweight = 'bold')
# plt.xlabel("Cell Radius (m)")
# plt.ylabel("Average No. of Connected Devices", fontsize = 16, fontweight = 'bold')
plt.ylabel("Average Runtime (s)", fontsize = 16, fontweight = 'bold')
#, bbox_to_anchor = (num1, ), loc = , borderaxespad =

plt.rcParams.update({'font.size': 14})
font = {'style': 'normal', 'weight': 'bold'}
plt.legend(frameon=False, loc=9, ncol=2, bbox_to_anchor=(0.5, 1.18), prop=font)

plt.savefig('RTime.pdf', format='pdf')
plt.show()
