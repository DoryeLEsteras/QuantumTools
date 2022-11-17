import numpy as np
from argparse import ArgumentParser
#from PythonFunctionLib.python_function_lib import grep
# extraer datos de outputs
################
nstep=15
nbands=5

def parser():
    parser = ArgumentParser(description="Script for creating SpinW input files")
    parser.add_argument("-input", "--input",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the bands input file
                        """)
    parser.add_argument("-bands", "--bands",
                       type=str,
                       required=True,
                       help="""
                       bands file to be repaired
                       """)                        
    parser.add_argument("-nstep", "--nstep",
                        type=str,
                        required=True,
                        help="number of calculated points between high symmetry points")
    parser.add_argument("-nbands", "--nbands",
                        type=str,
                        required=True,
                        default='',
                        help="number of Kohn states in the bands calculation")
    args = parser.parse_args()
    return args.input, args.bands, args.nstep,args.nbands

band_points=first_column=squared_kpoints_x=squared_kpoints_y=squared_kpoints_z=kvector_sums=kvector=[]
y=k=0
bands_output_file,bands_file,nstep,nbands = parser()

bands_out = open(bands_output_file, "r")
text_list = bands_out.readlines()
print(text_list.index("cart. coord. in units 2pi/alat"))
kpoints_x = np.loadtxt("kpfm.txt")[:, 0] # esto hay que extraerlo
kpoints_y = np.loadtxt("kpfm.txt")[:, 1]
kpoints_z = np.loadtxt("kpfm.txt")[:, 2]
energies = np.loadtxt(bands_file)[:, 1]

kvector=[0] # important, first element empty
squared_kpoints_x=[0]
squared_kpoints_y=[0]
squared_kpoints_z=[0]
for i in range(1, len(kpoints_x), 1):
    squared_kpoints_x.append((kpoints_x[i]-kpoints_x[i-1])**2)
    squared_kpoints_y.append((kpoints_y[i]-kpoints_y[i-1])**2)
    squared_kpoints_z.append((kpoints_z[i]-kpoints_z[i-1])**2)
squared_kpoints_x = np.around(squared_kpoints_x,9)
squared_kpoints_y = np.around(squared_kpoints_y,9)
squared_kpoints_z = np.around(squared_kpoints_z,9)
kvector_sums=np.sqrt(squared_kpoints_x+squared_kpoints_y+squared_kpoints_z)
for x in range(1, len(kvector_sums), 1):
    kvector.append(kvector_sums[x]+kvector[x-1])
new_bands_file = open("./bands.txt", "a")
for i in range(0,nbands):
  for j in kvector:
    k = k + i + 1
    #print(k)
    new_bands_file.write(f'{j} {energies[k]}\n')
    new_bands_file.write("\n")
new_bands_file.close
new_band_path_file = open("./band_path.txt", "a")
for j in range(0, len(kvector), nstep):
    band_points.append(kvector[j])
    #band_points.append(" ")
new_band_path_file.write(f'{band_points}\n')
new_band_path_file.close