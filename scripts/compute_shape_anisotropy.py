#!/usr/bin/python3
from QuantumTools.vasp_tools import Poscar, Outcar
from QuantumTools.directory_and_files_tools import get_time,stop_watch
import numpy as np
import math
import matplotlib.pyplot as plt
import os
from argparse import ArgumentParser
import time

def parser():
    parser = ArgumentParser(description="Script to compute shape anisotropy")
    parser.add_argument("-poscar", "--poscar",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path of the POSCAR file.
                        """)
    parser.add_argument("-outcar", "--outcar",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path of the OUTCAR file.
                        """)
    parser.add_argument("-outdir", "--outdir",
                        type=str,
                        required=False,
                        default='.',
                        help="Output directory ") 
    parser.add_argument("-ncells", "--ncells",
                        type=int,
                        required=True,
                        help="""
                        Number of cells por the single-shoot or scan simulation.
                        """)
    parser.add_argument("-dim", "--dim",
                        type=str,
                        required=True,
                        help="""
                        Replicate structure in 2D or 3D. Options 2D or 3D.
                        """)
    parser.add_argument("-mode", "--mode",
                        type=str,
                        required=True,
                        help="""
                        Single-shoot or scan. Options: single or scan.
                        """)
   
    args = parser.parse_args()
    return args.poscar,args.outcar,args.outdir,args.ncells,args.dim,args.mode

def orient_magnetic_moment(scalar_magnetic_moments,direction):
    magnetic_moment_vector = []
    if direction == 'x':
       for i in scalar_magnetic_moments:
           magnetic_moment_vector.append([i,0,0])
    if direction == 'y':
       for i in scalar_magnetic_moments:
           magnetic_moment_vector.append([0,i,0])
    if direction == 'z':
       for i in scalar_magnetic_moments:
           magnetic_moment_vector.append([0,0,i])
    magnetic_moment_vector = np.array(magnetic_moment_vector)
    return magnetic_moment_vector

def replicate_direction(old_cell,old_coordinates,old_magmom,direction:str, number_cells:int):
    new_cell_parameters = np.copy(old_cell)
    new_coordinates = np.copy(old_coordinates)
    new_cell_parameters[directions[direction]] = old_cell[directions[direction]] * number_cells
    new_magmom = np.copy(old_magmom)
    for i in range(number_cells-1):
        for line_number, line in enumerate(new_coordinates):
            new_coordinates[line_number][directions[direction]]= old_coordinates[line_number][directions[direction]] + 1 + i
            #print(new_coordinates[line_number][directions[direction]])
        old_coordinates = np.append(old_coordinates,new_coordinates,axis=0)
        new_magmom = np.append(old_magmom,new_magmom,axis=0)
    #print(new_magmom.shape,old_coordinates.shape)
    #print('\n')
    #print(old_coordinates)
    return new_cell_parameters, old_coordinates, new_magmom
    
def replicate_structure(number_cells:int,magnetic_moments_vector):
    x_cell,x_coordinates,x_magmom = replicate_direction(poscar.cell_parameters,poscar.atomic_coordinates,magnetic_moments_vector,'x',number_cells)
    xy_cell,xy_coordinates,xy_magmom = replicate_direction(x_cell,x_coordinates,x_magmom,'y',number_cells)
    if dimension == '3D':
       xy_cell,xy_coordinates,xy_magmom = replicate_direction(xy_cell,xy_coordinates,xy_magmom,'z',number_cells)
    
    ang_coordinates = np.zeros((len(xy_coordinates),3))
    for atom in range(0,len(xy_coordinates)):
        ang_coordinates[atom] = np.matmul(poscar.cell_parameters, xy_coordinates[atom])
        
    return xy_cell,ang_coordinates,xy_magmom

    # Tengo que hacer la 3D

def calculate_dipolar_energy(xy_coordinates,xy_magmom,number_cells):
    # eVtomeV*1/8pi * (eV to Joule) * (m0) * (muB)^2 /  (10^-30)
    # 10**-30 is the conversion from A to m ()
    constant = 1000*((1/(8*math.pi))*(1.602177*10**-19)*(1.25663706212*10**-6)*(5.7883818066*10**-5)**2)/(10**-30) 
    E = 0
    for atomic_index_i, atom_i in enumerate(xy_coordinates):
        for atomic_index_j, atom_j in enumerate(xy_coordinates):
            if atomic_index_i != atomic_index_j:
                rij = atom_i-atom_j
                distance = np.linalg.norm(atom_i-atom_j)
                mirij = np.dot(xy_magmom[atomic_index_i],rij)
                mjrij = np.dot(xy_magmom[atomic_index_j],rij)
                mimj = np.dot(xy_magmom[atomic_index_i],xy_magmom[atomic_index_j])
                E = (mimj - 3*(mirij*mjrij) /(distance**2))/(distance**3) + E
    E = constant * E/(2*number_cells**2)
    return E

def single_shoot(cell):
    #print(f'Computing single shoot of {number_cells}')
    magnetic_moments_vector = orient_magnetic_moment(scalar_magnetic_moments,'x')
    xy_cell, xy_coordinates, xy_magmom = replicate_structure(cell,magnetic_moments_vector)
    Ex = calculate_dipolar_energy(xy_coordinates,xy_magmom,cell)
    magnetic_moments_vector = orient_magnetic_moment(scalar_magnetic_moments,'y')
    xy_cell, xy_coordinates, xy_magmom = replicate_structure(cell,magnetic_moments_vector)
    Ey = calculate_dipolar_energy(xy_coordinates,xy_magmom,cell)
    magnetic_moments_vector = orient_magnetic_moment(scalar_magnetic_moments,'z')
    xy_cell, xy_coordinates, xy_magmom = replicate_structure(cell,magnetic_moments_vector)
    Ez = calculate_dipolar_energy(xy_coordinates,xy_magmom,cell)
    shape_xy =Ex-Ey
    shape_zx =Ez-Ex
    shape_zy =Ez-Ey
    print(f' Number of cells {number_cells} Shape_xy {shape_xy} Shape_zx {shape_zx} Shape_zy {shape_zy}')

def compute_shape_anisotropy(number_cells,scalar_magnetic_moments):
    shape_xyz = np.zeros((number_cells,3))
    with open(os.path.join(outdir,'dipolar_energy_per_axis_scan.txt'), 'w') as f: 
         f.write(f'# Shape_xy Shape_zx Shape_zy\n')
         for cell in range(1,number_cells+1):
             if dimension == '3D':
                print(f'Computing cell {cell}x{cell}x{cell} of {number_cells}')
             else:
                print(f'Computing cell {cell}x{cell}x{1} of {number_cells}')
             magnetic_moments_vector = orient_magnetic_moment(scalar_magnetic_moments,'x')
             xy_cell, xy_coordinates, xy_magmom = replicate_structure(cell,magnetic_moments_vector)
             Ex = calculate_dipolar_energy(xy_coordinates,xy_magmom,cell)
             magnetic_moments_vector = orient_magnetic_moment(scalar_magnetic_moments,'y')
             xy_cell, xy_coordinates, xy_magmom = replicate_structure(cell,magnetic_moments_vector)
             Ey = calculate_dipolar_energy(xy_coordinates,xy_magmom,cell)
             magnetic_moments_vector = orient_magnetic_moment(scalar_magnetic_moments,'z')
             xy_cell, xy_coordinates, xy_magmom = replicate_structure(cell,magnetic_moments_vector)
             Ez = calculate_dipolar_energy(xy_coordinates,xy_magmom,cell)
             f.write(f'{cell} {Ex} {Ey} {Ez}\n')
             shape_xyz[cell-1] = [Ex,Ey,Ez]
    shape_xy =shape_xyz[:,0]-shape_xyz[:,1]
    shape_zx =shape_xyz[:,2]-shape_xyz[:,0]
    shape_zy =shape_xyz[:,2]-shape_xyz[:,1]
    print(f'Shape_xy {shape_xy[-1]} Shape_zx {shape_zx[-1]} Shape_zy {shape_zy[-1]}')
    np.savetxt(os.path.join(outdir,'dipolar_energy_diference_scan.txt'),np.c_[shape_xy,shape_zx,shape_zy],newline = '\n',header = 'Shape_xy Shape_zx Shape_zy', fmt='%1.5f')
    return shape_xy,shape_zx,shape_zy

def plot_shape_anisotropy(shape_xy,shape_zx,shape_zy,number_cells):
    x_axis = np.arange(1,number_cells+1)
    fig,axs = plt.subplots(1,3,figsize=[18,7]) 
    axs[0].plot(x_axis,shape_xy,'-o',label=r', Shape$_{xy}$',  markersize=10,linewidth=2.0 )
    axs[1].plot(x_axis,shape_zx,'-o',label=r', Shape$_{zx}$',  markersize=10,linewidth=2.0 )
    axs[2].plot(x_axis,shape_zy,'-o',label=r', Shape$_{zy}$',  markersize=10,linewidth=2.0 )
    axs[0].set_ylabel('Shape anisotropy (meV / Cr)',fontsize = 25)
    axs[0].set_xlabel('Number of cells',fontsize = 25)
    axs[1].set_ylabel('Shape anisotropy (meV / Cr)',fontsize = 25)
    axs[1].set_xlabel('Number of cells',fontsize = 25)
    axs[2].set_ylabel('Shape anisotropy (meV / Cr)',fontsize = 25)
    axs[2].set_xlabel('Number of cells',fontsize = 25)
    axs[0].tick_params(labelsize=20)
    axs[1].tick_params(labelsize=20)
    axs[2].tick_params(labelsize=20)
    axs[0].legend(loc=7,fontsize=15)
    axs[1].legend(loc=7,fontsize=15)
    axs[2].legend(loc=7,fontsize=15)
    fig.tight_layout()
    plt.savefig(os.path.join(outdir,'Shape_anisotropy_scan.png'), dpi=400)
    #plt.show()
    
if __name__ == '__main__':
    start = time.time()
    poscar_file, outcar_file, outdir, number_cells, dimension, mode = parser()    
    #dimension = '2D'
    #mode = 'single' # scan or single
    #number_cells = 100
    directions = {
        'x':0,
        'y':1,
        'z':2
    }
    #file = 'shape_poscar_cart'
    #scalar_magnetic_moments = [2.736387,2.736302,2,2]
    outcar = Outcar()
    outcar.extract_information(outcar_file)
    scalar_magnetic_moments = outcar.metal_magmom
    #scalar_magnetic_moments = [3,3]
    poscar = Poscar()
    poscar.read_data(poscar_file)
    if poscar.units_atomic_coordinates.lower() == 'cartesian':
       for i in range(0,len(poscar.atomic_coordinates)):
           poscar.atomic_coordinates[i] = np.matmul(np.linalg.inv(poscar.cell_parameters),poscar.atomic_coordinates[i])
    poscar.atomic_coordinates = poscar.atomic_coordinates[0:outcar.nmag]
    if mode == 'single':
       single_shoot(number_cells)
    else:
       shape_xy,shape_zx,shape_zy= compute_shape_anisotropy(number_cells,scalar_magnetic_moments)
       plot_shape_anisotropy(shape_xy,shape_zx,shape_zy,number_cells)
    with open(os.path.join(outdir,'log.txt'),'w') as f:
         f.write('Done! ' + stop_watch(start, time.time()) + '\n')
   