import matplotlib.pyplot as plt
import numpy as np
devices_block = 1
plot_x_number = 5
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

fig, ax = plt.subplots()

timearray = np.zeros(plot_x_number)
for i in range(plot_x_number):
    timearray[i] = (i+1) * devices_block

# plt.plot(timearray,[55.283,106.916,144.631,176.548,202.06],"k-.d",label="NOMA-SM1")
# plt.plot(timearray,[55.283,106.916,144.631,176.548,202.06],"g-.^",label="NOMA-SM2")
# plt.plot(timearray,[55.08,90.645,125.005,145.535,160.77],"r-.h",label="MWFMP[16]")
# plt.plot(timearray,[24.757,44.624,60.677,73.767,80.169],"-.o",label="MPSDA[16]")
#
plt.plot(timearray,[0.15719986,1.17330567,4.40705655,10.80946397,22.41047872],"k-.d",label="NOMA-SM1")
plt.plot(timearray,[0.10546957,0.92068332,2.77552159,5.69563593,13.49266609],"g-.^",label="NOMA-SM2")
plt.plot(timearray,[0.15238817,1.15527844,4.22135728,10.58685287,23.37039524],"r-.h",label="MWFMP[16]")
plt.plot(timearray,[0.01215805,0.77828554,1.26106226,2.71863132,6.39005792],"-.o",label="MPSDA[16]")

# plt.yticks(np.arange(1, 6, step = 4))
plt.tick_params(labelsize = 14)
plt.xticks(np.arange(1, 6, step = 1), fontweight = 'bold')
plt.tick_params(labelsize = 14)
plt.yticks(fontweight = 'bold')

plt.ylim(ymin = 0)
plt.xlim(xmin = 1)

plt.grid(b=None, which='major', axis='both')
# plt.title("")
plt.xlabel("No. of PRBs", fontsize = 16, fontweight = 'bold')
# plt.xlabel("R (kpbs)")
# plt.xlabel("Cell Radius (m)")

# plt.ylabel("Average No. of Connected Devices", fontsize = 16, fontweight = 'bold')
plt.ylabel("Average Runtime (s)", fontsize = 16, fontweight = 'bold')
#, bbox_to_anchor = (num1, ), loc = , borderaxespad =

plt.rcParams.update({'font.size': 14})
font = {'style': 'normal', 'weight': 'bold'}
plt.legend(frameon=False, loc=9, ncol=2, bbox_to_anchor=(0.5, 1.18), prop=font)

plt.savefig('PRBTime.pdf', format='pdf')
plt.show()
