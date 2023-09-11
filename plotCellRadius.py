import matplotlib.pyplot as plt
import numpy as np
devices_block = 500
plot_x_number = 7
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

fig, ax = plt.subplots()


timearray = np.zeros(plot_x_number)
for i in range(plot_x_number):
    timearray[i] = i * devices_block + 250

plt.plot(timearray,[3.08184722, 3.24558106, 3.44789984, 3.23802193, 3.44502254, 3.36319669,3.20673553] ,"k-.d",label="NOMA-SM1")
plt.plot(timearray,[2.42455449, 2.22120813,2.11205048,2.19059827,2.11573276,2.45021497,2.45022841],"g-.^",label="NOMA-SM2")
plt.plot(timearray,[4.47053027, 4.44357101, 4.3884202,  4.4505935,  4.33564232, 4.42248696,4.42452576],"r-.h",label="MWFMP[16]")
plt.plot(timearray,[1.10528242, 1.14227395, 1.22205585, 1.22467608, 1.24817566, 1.25048489, 1.25927374],"-.o",label="MPSDA[16]")

# plt.plot(timearray,[180.,178.53,172.396,153.286,134.666,116.104,99.175],"k-.d",label="NOMA-SM1")
# plt.plot(timearray,[180.,178.53,172.396,153.286,134.666,116.104,99.175],"g-.^",label="NOMA-SM2")
# plt.plot(timearray,[180.,173.66,164.09,141.795,120.13,96.995,69.82],"r-.h",label="MWFMP[16]")
# plt.plot(timearray,[180.,163.224,145.792,125.092,100.155,69.228,31.58],"-.o",label="MPSDA[16]")

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

# plt.ylabel("Average No. of Connected Devices", fontsize = 16, fontweight = 'bold')
plt.ylabel("Average Runtime (s)", fontsize = 16, fontweight = 'bold')
#, bbox_to_anchor = (num1, ), loc = , borderaxespad =
plt.rcParams.update({'font.size': 14})
plt.legend(frameon=False, loc=9, ncol=2, bbox_to_anchor=(0.5, 1.18), prop=font)

# plt.tight_layout()
plt.savefig('CellRadiusTime.pdf', format='pdf')

plt.show()