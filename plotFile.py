import matplotlib.pyplot as plt
import numpy as np
devices_block = 4
plot_x_number = 10


timearray = np.zeros(plot_x_number)
for i in range(plot_x_number):
    timearray[i] = (i+1) * devices_block

plt.plot(timearray, [ 4. , 8., 12., 12., 12., 12., 12., 12., 12., 12.], "r-.d" , label="MPSDA,L=1(OMA)")
plt.plot(timearray, [ 4. , 8., 12., 12., 12., 12., 12., 12., 12., 12.], "b-h", label="MIP,L=1(OMA)")

plt.plot(timearray, [ 4. , 8. ,12., 16., 20., 24., 24., 24., 24., 24.], "-.o", label="MPSDA,L=2")
plt.plot(timearray, [ 4. , 8. ,12., 16., 20., 23., 24., 24., 24., 24.], "c-v", label="MIP,L=2")

plt.plot(timearray,[ 4.  ,8., 12., 16., 20., 24., 28., 32., 36. ,36.], "g-.^", label="MPSDA,L=3")
plt.plot(timearray, [ 4., 8. ,12., 16., 20., 23., 27., 31., 34., 36.], "m-s", label="MIP,L=3")

plt.yticks(np.arange(4, 41, step = 4))
plt.xticks(np.arange(4, 41, step = 4))
plt.ylim(ymin = 4)
plt.xlim(xmin = 4)

plt.grid(b=None, which='major', axis='both')
plt.title("Results when |PRB| = 1")
plt.xlabel("No. of Contending Devices")
plt.ylabel("Average No. of Connected Devices")

plt.legend()
plt.show()