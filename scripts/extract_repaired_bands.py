#!/usr/bin/python3
import numpy as np
from argparse import ArgumentParser
from QuantumTools.band_tools import count_nbands,count_nk

# To Do List
"""
just valid for homogeneous kpoints (ex: 20 20 20)
"""

# DESCRIPTION

"""
This script repairs the broken bands of QuantumEspresso
IN: bands.out,broken band.dat.gnu file and number of high symmetry points 
    in bands.in calculation (parser)
OUT: repaired band.dat.gnu file and file with new hygh symmetry points
"""

def parser():
    parser = ArgumentParser(description="Script for repairing QuantumEspresso bands")
    parser.add_argument("-input", "--input",
                        type=str,
                        required=True,
                        help="""
                        bands.out file
                        """)
    parser.add_argument("-bands", "--bands",
                       type=str,
                       required=True,
                       help="""
                       bands file to be repaired
                       """)  
    parser.add_argument("-hs", "--hs",
                       type=int,
                       required=True,
                       help="""
                       number of hygh symmetry points in the band calculation
                       (bands.in)
                       """)                            
    args = parser.parse_args()
    return args.input, args.bands ,args.hs
def extract_healthy_kp(bands_out_file:str,nk:int)-> np.ndarray:
    kpoints_x = np.array([]);kpoints_y = np.array([]);kpoints_z = np.array([])
    bands_out = open(bands_out_file, "r")
    line = bands_out.readline()
    while line  != "                       cart. coord. in units 2pi/alat\n":
        line = bands_out.readline()
    for i in range(0,nk,1):
        line = bands_out.readline()
        filtered_line = line.replace(')','').replace(',','').split()
        kpoints_x = np.append(kpoints_x,float(filtered_line[4]))
        kpoints_y = np.append(kpoints_y,float(filtered_line[5]))
        kpoints_z = np.append(kpoints_z,float(filtered_line[6]))
    bands_out.close()
    return kpoints_x, kpoints_y, kpoints_z
def repair_bands(kpoints_x:np.ndarray,kpoints_y:np.ndarray,kpoints_z:np.ndarray,nbands:int,nk:int)-> None:
    squared_kpoints_x = np.array([0]); squared_kpoints_y = np.array([0]); squared_kpoints_z = np.array([0])
    kvector_sums = np.array([]); kvector = np.array([0]) # important, first element empty
    band_points = []
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

if __name__ == '__main__':
   bands_out_file,bands_file,nkpoints = parser()
   nbands = count_nbands(bands_file)
   nk = count_nk(bands_file)
   # Extract data
   energies = np.loadtxt(bands_file)[:, 1]
   kpoints_x, kpoints_y, kpoints_z = extract_healthy_kp(bands_out_file,nk)
   repair_bands(kpoints_x,kpoints_y,kpoints_z,nbands,nk)
