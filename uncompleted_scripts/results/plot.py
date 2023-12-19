import numpy as np
import matplotlib.pyplot as plt

data_file = 'J.txt'
x_axis = np.loadtxt(data_file)[:, 0]
J1iso= np.loadtxt(data_file)[:, 1]/6
J2iso= np.loadtxt(data_file)[:, 2]/6
J3iso= np.loadtxt(data_file)[:, 3]/6
J4iso= np.loadtxt(data_file)[:, 4]/6
J5iso= np.loadtxt(data_file)[:, 5]/6
 
figtot,ax = plt.subplots(1,5,figsize=[16,6]) 
x_axis = x_axis - 100
ax[0].plot(x_axis,J1iso,'-ok', color='black' )
ax[1].plot(x_axis,J2iso,'-ok', color='black' )
ax[2].plot(x_axis,J3iso,'-ok', color='black' )
ax[3].plot(x_axis,J4iso,'-ok', color='black' )
ax[4].plot(x_axis,J5iso,'-ok', color='black' )
ax[0].set_ylabel(r'$J_1$, meV',fontsize = 20)
ax[1].set_ylabel(r'$J_2$, meV',fontsize = 20)
ax[2].set_ylabel(r'$J_3$, meV',fontsize = 20)
ax[3].set_ylabel(r'$J_4$, meV',fontsize = 20)
ax[4].set_ylabel(r'$J_5$, meV',fontsize = 20)
ax[0].set_xlabel(r'$\epsilon$, %',fontsize = 20)
ax[1].set_xlabel(r'$\epsilon$, %',fontsize = 20)
ax[2].set_xlabel(r'$\epsilon$, %',fontsize = 20)
ax[3].set_xlabel(r'$\epsilon$, %',fontsize = 20)
ax[4].set_xlabel(r'$\epsilon$, %',fontsize = 20)
figtot.subplots_adjust(bottom=0.1)
figtot.subplots_adjust(left=0.2)
figtot.tight_layout()
plt.show()
 #plt.savefig(output_dir + '/' + prefix + '.Total_J_vs' + label  + '.png')