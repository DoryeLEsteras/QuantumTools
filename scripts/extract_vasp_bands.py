#!/usr/bin/python3
import os
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from QuantumTools.directory_and_files_tools import manage_input_dir
from QuantumTools.vasp_tools import Outcar

def parser():
    parser = ArgumentParser(description="Script for Wannier bands with VASP")
    parser.add_argument("-outcar", "--outcar",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the OUTCAR file 
                        """)
    parser.add_argument("-outdir", "--outdir",
                       type=str,
                       required=False,
                       default='',
                       help="""
                       Number of high symmetry points in the band calculation
                       """) 
    parser.add_argument("-hs", "--hs",
                       type=int,
                       required=True,
                       help="""
                       Number of high symmetry points in the band calculation
                       """) 
    args = parser.parse_args()
    return args.outcar, args.outdir,args.hs

def vasp_extract_band_kpoints(high_symmetry_points_number:int) -> np.ndarray:
    with open (outcar,'r') as f:
         for line in f:
             line = line.split()
             if len(line)> 1:
                if line[0] == 'k-points' and line[-1] == 'h' and line[4] == '2pi/SCALE': 
                   k_matrix = np.zeros((Vasp_outcar.nk+1,3))
                   for i in range(Vasp_outcar.nk):
                       line = f.readline().split()
                       k_matrix[i+1][0] = float(line[0])
                       k_matrix[i+1][1] = float(line[1])
                       k_matrix[i+1][2] = float(line[2])
    distance = np.array([])
    kvector = np.array([0])
    band_points = np.array([])
    for i in range(1, Vasp_outcar.nk+1, 1):
        distance = np.append(distance,np.linalg.norm(k_matrix[i][:]-k_matrix[i-1][:]))
    for x in range(1, len(distance), 1):
        kvector = np.append(kvector,distance[x] + kvector[x-1])
    #nstep = high_symmetry_points_number - 1
    for j in range(0, len(kvector), int(Vasp_outcar.nk/high_symmetry_points_number)):
        band_points = np.append(band_points,kvector[j])
    print(band_points)
    return band_points,kvector

def vasp_extract_electronic_bands(kvector:np.ndarray)-> None:
    bands_up = np.zeros((Vasp_outcar.nbands,Vasp_outcar.nk))
    bands_down = np.zeros((Vasp_outcar.nbands,Vasp_outcar.nk))
    with open (outcar,'r') as f:
        for line in f:
            line = line.split()
            if len(line)>1: 
                if line[0] == 'Fermi' and line[1] == 'energy:':
                   f.readline();f.readline()
                   for k in range(Vasp_outcar.nk):
                       f.readline();f.readline();f.readline()
                       for band in range(Vasp_outcar.nbands):
                           line = f.readline().split()[1] 
                           bands_up[band][k] = line
                   f.readline();f.readline();f.readline()
                   for k in range(Vasp_outcar.nk):
                       f.readline();f.readline();f.readline()
                       for band in range(Vasp_outcar.nbands):
                           line = f.readline().split()[1] 
                           bands_down[band][k] = line
    band_vector_up = np.array([])
    band_vector_down = np.array([])
    for dim1 in range(Vasp_outcar.nbands):
        band_vector_up = np.append(band_vector_up,bands_up[:][dim1])
        band_vector_up = np.append(band_vector_up,' ')
    if Vasp_outcar.ispin == 2:
       for dim1 in range(Vasp_outcar.nbands):
           band_vector_down = np.append(band_vector_down,bands_down[:][dim1])
           band_vector_down = np.append(band_vector_down,' ')

    kp = np.append(kvector,' ')
    kpf = np.array([])
    for i in range(0,Vasp_outcar.nbands):
        kpf = np.append(kpf,kp)
    with open(os.path.join(outdir,'dft_up.dat.gnu'),'w') as f:
        for element in range(len(kpf)):
            f.write(str(kpf[element]) + ' ' + str(band_vector_up[element]) + '\n')
    with open(os.path.join(outdir,'dft_down.dat.gnu'),'w') as f:
        for element in range(len(kpf)):
            f.write(str(kpf[element]) + ' ' + str(band_vector_down[element]) + '\n') 

"""
def plot_wannier_and_dft_bands(wannier_bands_up:str,wannier_bands_down:str,kpf:np.ndarray,dft_bands_up:np.ndarray) -> None:
    #wannier_kpoints = np.loadtxt(wannier_bands_up)[:, 0]
    #wannier_bands_up = np.loadtxt(wannier_bands_up)[:, 1]
    #dft_kpoints = np.loadtxt(dft_bands_up)[:, 0]
    #dft_bands_up = np.loadtxt(dft_bands_up)[:, 1]
    fig,ax = plt.subplots(figsize=[5,7]) 
    #ax.plot(wannier_kpoints,wannier_bands_up,'-', color='blue',label='m = -3')
    ax.plot(kpf,dft_bands_up,'-', color='red',label='m = -2')
    #if ispin == 2:
       #wannier_bands_down = np.loadtxt(wannier_bands_down)[:, 1]
      # dft_bands_down = np.loadtxt(dft_bands_down)[:, 1]
     #  ax.plot(wannier_kpoints,wannier_bands_down,'-', color='blue',label='m = -2')
       #ax.plot(kpf,dft_bands_up,'-', color='red',label='m = -2')
    ax.set_ylabel(r'PDOS (states/eV)',fontsize = 20)
    ax.set_xlabel(r'Energy (eV)',fontsize = 20)
    ax.tick_params(axis='both',  labelsize=15)
    #ax.set_xlim(0, 1000.0)
    #ax.set_ylim(-50, 50.0)
    ax.legend()
    plt.show()
"""    

if __name__ == '__main__':
    outcar,outdir,high_symmetry_points_number = parser()
    outcar_name,outcar_dir = manage_input_dir(outcar)
    if outdir == '':
       outdir = outcar_dir 

    Vasp_outcar = Outcar()
    Vasp_outcar.extract_information(outcar)
    
    band_points,kvector = vasp_extract_band_kpoints(high_symmetry_points_number)
    vasp_extract_electronic_bands(kvector)
    #plot_wannier_and_dft_bands(wannier_bands_up,wannier_bands_down,kpf,dft_bands_up)
