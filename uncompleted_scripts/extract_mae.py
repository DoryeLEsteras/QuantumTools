from QuantumTools.qe_tools import QEoutput
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser

# TO DO LIST
"""
If the loops are floats the strategy I used for the names will search for 1.0 and will CRASH
"""

def parser():
    parser = ArgumentParser(description="Script to extract and plot exchange parameters")
    parser.add_argument("-name_structure", "--name_structure",
                        type=str,
                        required=True,
                        help="""
                        Structure of the files, indicating with substituting with 'index' and 'component' the prefixes to perform the loop.\n Ex: files on the form fe.1.x.scf.out will be introduced as fe.index.component.scf.out
                        """)   
    parser.add_argument("-inputdir", "--inputdir",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the input file
                        """)               
    parser.add_argument("-label", "--label",
                        type=str,
                        required=False,
                        default = r'$\epsilon$, %',
                        help="""
                        Label for x_axis in the Figures. Default -> epsilon (%)
                        """),
    parser.add_argument("-min", "--min",
                        type=int,
                        required=True,
                        help="""
                        Minimum value of the scan
                        """), 
    parser.add_argument("-max", "--max",
                        type=int,
                        required=True,
                        help="""
                        Maximum value of the scan
                        """), 
    parser.add_argument("-step", "--step",
                        type=int,
                        required=False,
                        default = 1,
                        help="""
                        Step value of the scan
                        """)

    args = parser.parse_args()
    return args.name_structure,args.inputdir,args.label,args.min,args.max,args.step

  
name_format, input_dir, label, nmin, nmax, nstep = parser()


#nmin = 95
#nmax = 105
#nstep = 1
#name_format = 'cucrse.index.component.scf.out'

energy_matrix = np.zeros((int(nmax-nmin+1/nstep),3))
MAE = np.zeros((int(nmax-nmin+1/nstep),3))

x_axis = np.arange(nmin,nmax+nstep,nstep)

index = 0
for component in 'xyz':
    for loop_parameter in x_axis:
        index2 = loop_parameter -nmin
        file_name = name_format.replace('index',str(loop_parameter)).replace('component',str(component))
        Scf = QEoutput()
        Scf.extract_output_information(file_name)
        energy_matrix[index2][index] = f"{Scf.total_energy:.8f}"
    index = index + 1
energy_matrix = energy_matrix*13605.662285137

MAExy=np.array([]);MAExz=np.array([]);MAEyz=np.array([])
for loop_parameter in x_axis:
    MAExy = np.append(MAExy,energy_matrix[loop_parameter-nmin][0]-energy_matrix[loop_parameter-nmin][1])
    MAExz = np.append(MAExz,energy_matrix[loop_parameter-nmin][0]-energy_matrix[loop_parameter-nmin][2])
    MAEyz = np.append(MAEyz,energy_matrix[loop_parameter-nmin][1]-energy_matrix[loop_parameter-nmin][2])

print(f" MAEx - MAEy {MAExy}\n")
print(f" MAEx - MAEz {MAExz}\n")
print(f" MAEy - MAEz {MAEyz}")

figtot,ax = plt.subplots(1,3,figsize=[12,5]) 
ax[0].plot(x_axis,MAExy,'-ok')
ax[1].plot(x_axis,MAExz,'-ok')
ax[2].plot(x_axis,MAEyz,'-ok')
ax[0].set_ylabel(r'$MAE_{xy}$, meV/cell',fontsize = 20)
ax[1].set_ylabel(r'$MAE_{xz}$, meV/cell',fontsize = 20)
ax[2].set_ylabel(r'$MAE_{yz}$, meV/cell',fontsize = 20)
ax[0].set_xlabel(label,fontsize = 20)
ax[1].set_xlabel(label,fontsize = 20)
ax[2].set_xlabel(label,fontsize = 20)
figtot.subplots_adjust(bottom=0.1)
figtot.subplots_adjust(left=0.2)
figtot.tight_layout()
plt.show()
plt.savefig('test.png')
