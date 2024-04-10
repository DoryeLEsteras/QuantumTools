#!/usr/bin/python3
from QuantumTools.vasp_tools import Poscar, Outcar
from QuantumTools.directory_and_files_tools import get_time,stop_watch
from QuantumTools.magnetic_tools import orient_magnetic_moment
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
    parser.add_argument("-cell", "--cell",
                        type=int,
                        nargs=3,
                        required=False,
                        default=[1, 1, 1],
                        help="""
                        Starting cell where to compute shape anisotropy, can be 
                        for single-shoot calculations or as an starting point for
                        an scan using rep_step and final_cell. 
                        Ex: 1 1 1 or 5 5 5
                        """)
    parser.add_argument("-rep_step", "--rep_step",
                        type=int,
                        nargs=3,
                        required=False,
                        default=[1, 1, 1],
                        help="""
                        Step to replicate the cell.
                        Ex: 1 1 1 or  2 2 1
                        """)
    parser.add_argument("-final_cell", "--final_cell",
                        type=int,
                        nargs=3,
                        required=False,
                        default=[1, 1, 1],
                        help="""
                        Final cell for the replation.
                        Ex: 8 8 8 or 8 8 1
                        """)
    args = parser.parse_args()
    return args.poscar,args.outcar,args.outdir,args.cell,args.rep_step,args.final_cell

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
    
def replicate_structure(number_cells,magnetic_moments_vector): 
    x_cell,x_coordinates,x_magmom = replicate_direction(poscar.cell_parameters,poscar.atomic_coordinates,magnetic_moments_vector,'x',number_cells[0])
    xy_cell,xy_coordinates,xy_magmom = replicate_direction(x_cell,x_coordinates,x_magmom,'y',number_cells[1])
    xyz_cell,xyz_coordinates,xyz_magmom = replicate_direction(xy_cell,xy_coordinates,xy_magmom,'z',number_cells[2])
    ang_coordinates = np.zeros((len(xyz_coordinates),3))
    for atom in range(0,len(xyz_coordinates)):
        ang_coordinates[atom] = np.matmul(poscar.cell_parameters, xyz_coordinates[atom])
        
    return xyz_cell,ang_coordinates,xyz_magmom

def calculate_dipolar_energy(coordinates,magmom,number_cells):
    # eVtomeV*1/8pi * (eV to Joule) * (m0) * (muB)^2 /  (10^-30)
    # 10**-30 is the conversion from A to m ()
    constant = 1000*((1/(8*math.pi))*(1.602177*10**-19)*(1.25663706212*10**-6)*(5.7883818066*10**-5)**2)/(10**-30) 
    E = 0
    for atomic_index_i, atom_i in enumerate(coordinates):
        for atomic_index_j, atom_j in enumerate(coordinates):
            if atomic_index_i != atomic_index_j:
                rij = atom_i-atom_j
                distance = np.linalg.norm(atom_i-atom_j)
                mirij = np.dot(magmom[atomic_index_i],rij)
                mjrij = np.dot(magmom[atomic_index_j],rij)
                mimj = np.dot(magmom[atomic_index_i],magmom[atomic_index_j])
                E = (mimj - 3*(mirij*mjrij) /(distance**2))/(distance**3) + E
    E = constant * E/(outcar.nmag*number_cells)
    return E

def compute_shape_anisotropy(scalar_magnetic_moments):
    shape_xyz = np.zeros((scan_steps,3))
    with open(os.path.join(outdir,'dipolar_energy_per_axis.txt'), 'w') as f: 
         f.write(f'# Cell Ex Ey Ez\n')
         cell = starting_cell
         loop_number = 0
         while (cell != final_cell + replication_step).any():
               print(f'Computing cell {cell[0]}x{cell[1]}x{cell[2]} of {final_cell[0]}x{final_cell[1]}x{final_cell[2]}')
               magnetic_moments_vector = orient_magnetic_moment(scalar_magnetic_moments,'x')
               xyz_cell, xyz_coordinates, xyz_magmom = replicate_structure(cell,magnetic_moments_vector)
               Ex = calculate_dipolar_energy(xyz_coordinates,xyz_magmom,np.prod(cell))
               magnetic_moments_vector = orient_magnetic_moment(scalar_magnetic_moments,'y')
               xyz_cell, xyz_coordinates, xyz_magmom = replicate_structure(cell,magnetic_moments_vector)
               Ey = calculate_dipolar_energy(xyz_coordinates,xyz_magmom,np.prod(cell))
               magnetic_moments_vector = orient_magnetic_moment(scalar_magnetic_moments,'z')
               xyz_cell, xyz_coordinates, xyz_magmom = replicate_structure(cell,magnetic_moments_vector)
               Ez = calculate_dipolar_energy(xyz_coordinates,xyz_magmom,np.prod(cell))
               cell_str = str(cell).replace('[','').replace(']','')
               f.write(f'{cell_str} {Ex:.5f} {Ey:.5f} {Ez:.5f}\n')
               shape_xyz[loop_number] = [Ex,Ey,Ez]
               loop_number = loop_number + 1
               cell = cell + replication_step
    shape_xy =shape_xyz[:,0]-shape_xyz[:,1]
    shape_zx =shape_xyz[:,2]-shape_xyz[:,0]
    shape_zy =shape_xyz[:,2]-shape_xyz[:,1]
    np.savetxt(os.path.join(outdir,'dipolar_energy_difference_scan.txt'),np.c_[replication_vector,shape_xy,shape_zx,shape_zy],newline = '\n',header = 'Cell Shape_xy Shape_zx Shape_zy', fmt=["%i"]*3+ ["%1.5f"]*3)
    return shape_xy,shape_zx,shape_zy

def plot_shape_anisotropy(shape_xy,shape_zx,shape_zy):
    fig,axs = plt.subplots(1,3,figsize=[24,9]) 
    axs[0].plot(replication_str,shape_xy,'-o',label=r', Shape$_{xy}$',  markersize=10,linewidth=2.0 )
    axs[1].plot(replication_str,shape_zx,'-o',label=r', Shape$_{zx}$',  markersize=10,linewidth=2.0 )
    axs[2].plot(replication_str,shape_zy,'-o',label=r', Shape$_{zy}$',  markersize=10,linewidth=2.0 )
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
    axs[0].tick_params(rotation=90)
    axs[1].tick_params(rotation=90)
    axs[2].tick_params(rotation=90)
    fig.tight_layout()
    plt.savefig(os.path.join(outdir,'Shape_anisotropy_scan.png'), dpi=400)
    #plt.show()
    
if __name__ == '__main__':
    start = time.time()
    poscar_file, outcar_file, outdir, starting_cell, replication_step, final_cell = parser()    
    starting_cell = np.array(starting_cell)
    replication_cell = np.array(replication_step)
    final_cell = np.array(final_cell)
    cell = starting_cell; scan_steps = 0
    replication_vector = []
    while (cell != final_cell + replication_step ).any():
          replication_vector.append(cell)
          cell = cell + replication_step
          scan_steps = scan_steps + 1
    replication_str = [str(x) for x in replication_vector]

    directions = {
        'x':0,
        'y':1,
        'z':2
    }

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
    
    shape_xy,shape_zx,shape_zy= compute_shape_anisotropy(scalar_magnetic_moments)
    plot_shape_anisotropy(shape_xy,shape_zx,shape_zy)
    with open(os.path.join(outdir,'log.txt'),'w') as f:
         f.write('Done! ' + stop_watch(start, time.time()) + '\n')
    
   