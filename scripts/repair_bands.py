import numpy as np
from argparse import ArgumentParser

# just valid for homogeneous kpoints (ex: 20 20 20)
################


def parser():
    parser = ArgumentParser(description="Script for repairing QuantumEspresso bands")
    parser.add_argument("-input", "--input",
                        type=str,
                        required=True,
                        help="""
                        bands output file
                        """)
    parser.add_argument("-bands", "--bands",
                       type=str,
                       required=True,
                       help="""
                       bands file to be repaired
                       """)  
    parser.add_argument("-nk", "--nk",
                       type=int,
                       required=True,
                       help="""
                       number of hygh symmetry points in the band calculation
                       """)                            
    args = parser.parse_args()
    return args.input, args.bands ,args.nk

band_points = []; first_column = []
kvector_sums = np.array([]); text_list = []
y=0; k=0;nk = 0; nbands = 0; counter = 0
kpoints_x = np.array([]);kpoints_y = np.array([]);kpoints_z = np.array([])
squared_kpoints_x = np.array([0]); squared_kpoints_y = np.array([0]); squared_kpoints_z = np.array([0])
kvector = np.array([0]) # important, first element empty
bands_output_file,bands_file,nkpoints = parser()

# Calculate number of bands and number of kpoints per band
with open(str(bands_file),'r') as f:
    while nk == 0 :
        line = f.readline()
        read_line = line.split()
        read_line.append('end')
        if read_line[0] == 'end':
            nk = counter
        counter = counter + 1
with open(str(bands_file),'r') as f:
    for line in f:
        read_line = line.split()
        read_line.append('end')
        if read_line[0] == 'end':
            nbands = nbands +1


bands_out = open(bands_output_file, "r")
line = bands_out.readline()
while line  != "                       cart. coord. in units 2pi/alat\n":
    line = bands_out.readline()
for i in range(0,nk,1):
    line = bands_out.readline()
    filtered_line = line.replace(')','').replace(',','').split()
    kpoints_x = np.append(kpoints_x,float(filtered_line[4]))
    kpoints_y = np.append(kpoints_y,float(filtered_line[5]))
    kpoints_z = np.append(kpoints_z,float(filtered_line[6]))
energies = np.loadtxt(bands_file)[:, 1]
for i in range(1, len(kpoints_x), 1):
    squared_kpoints_x = np.append(squared_kpoints_x,(kpoints_x[i]-kpoints_x[i-1])**2)
    squared_kpoints_y = np.append(squared_kpoints_y,(kpoints_y[i]-kpoints_y[i-1])**2)
    squared_kpoints_z = np.append(squared_kpoints_z,(kpoints_z[i]-kpoints_z[i-1])**2)
kvector_sums=np.sqrt(squared_kpoints_x+squared_kpoints_y+squared_kpoints_z)


counter = 0
for x in range(1, len(kvector_sums), 1):
    kvector = np.append(kvector,kvector_sums[x]+kvector[x-1])
new_bands_file = open('repaired_bands.gnu', "w")
for i in range(0,nbands):
  for j in range(0,len(kvector),1): 
    new_bands_file.write(str(kvector[j]) + ' ' + str(energies[counter]) + '\n')
    counter = counter + 1
  new_bands_file.write("\n")
new_bands_file.close

nstep = nkpoints - 1
new_band_path_file = open('repaired_bands_path.txt', "w")
for j in range(0, len(kvector), int(nk/nstep)):
    band_points.append(kvector[j])
new_band_path_file.write(f'{band_points}\n')
new_band_path_file.close
