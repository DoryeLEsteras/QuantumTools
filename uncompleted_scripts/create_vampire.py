from QuantumTools.vasp_tools import Poscar,Outcar,Incar
from QuantumTools.magnetic_tools import orient_magnetic_moment
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict, Field
from typing import List
import os
import numpy as np

"""
To do
For the future,implement a way to calculate the cells that interact, 100 010 ..
finish UCF 
check with alberto wich things are universal and correct
implement some kind of decission between qe or vasp
add a parser for the input data
think how to loop everything
"""

@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class Vampire:
      nmag: int = 0
      a: float = 0.0
      b: float = 0.0
      c: float = 0.0
      anisotropy: float = 0.0
      metal_labels: List = Field(default_factory=lambda:[])
      metal_magmom: np.ndarray = Field(default_factory=lambda:np.array([]))
      aniso_dir: np.ndarray = Field(default_factory=lambda:np.array([]))
      spin_dir: np.ndarray = Field(default_factory=lambda:np.array([]))

def vasp_prepare_data():
    # For the input
    poscar = Poscar()
    poscar.read_data(input_dir)
    vampire.a = np.linalg.norm(poscar.cell_parameters[0])
    vampire.b = np.linalg.norm(poscar.cell_parameters[1])
    vampire.c = np.linalg.norm(poscar.cell_parameters[2])
    #For mat
    outcar = Outcar()
    outcar.extract_information(input_dir2)
    vampire.metal_labels = poscar.atom_label_list[0:outcar.nmag]
    vampire.metal_magmom = outcar.metal_magmom
    vampire.anisotropy = anisotropy
    vampire.aniso_dir = str(orient_magnetic_moment(np.array([1]),aniso_dir)).replace('[','').replace(']','').replace(' ',',')
    vampire.spin_dir = str(orient_magnetic_moment(np.array([1]),spin_dir)).replace('[','').replace(']','').replace(' ',',')
    # For UCF
    vampire.nmag = outcar.nmag
    vampire.coordinates = poscar.atomic_coordinates
    vampire.cell_parameters = poscar.cell_parameters
    vampire.nat = poscar.nat

def write_input():
    with open(os.path.join(outdir,'input'),'w') as f:
        f.write(f"""
        #------------------------------------------ 
        # Creation attributes: 
        #------------------------------------------ 
        create:full
        create:periodic-boundaries-x 
        create:periodic-boundaries-y 
        create:periodic-boundaries-z 
        #------------------------------------------
        material:file=vampire.mat
        material:unit-cell-file = "vampire.UCF"
        #------------------------------------------ 
        # System Dimensions: 
        #------------------------------------------ 
        dimensions:unit-cell-size-x = {vampire.a}
        dimensions:unit-cell-size-y = {vampire.b}
        dimensions:unit-cell-size-z = {vampire.c}
        
        dimensions:system-size-x = 15.0 !nm 
        dimensions:system-size-y = 15.0 !nm 
        dimensions:system-size-z = 10.0 !nm 
        #------------------------------------------ 
        # Simulation attributes: 
        #------------------------------------------ 
        sim:temperature=0 
        sim:minimum-temperature=0 
        sim:maximum-temperature={Tmax}
        sim:temperature-increment={Tstep}
        sim:time-steps-increment=1
        sim:equilibration-time-steps={eq_steps}
        sim:loop-time-steps={loop_steps} 
        #------------------------------------------ 
        # Program and integrator details 
        #------------------------------------------ 
        sim:program=curie-temperature
        sim:integrator=llg-heun
        #------------------------------------------
        # Data output 
        #------------------------------------------ 
        output:temperature
        output:material-magnetisation 
        output:mean-magnetisation-length
        """)

def write_mat():
    with open(os.path.join(outdir,'vampire.mat'),'w') as f:
         f.write(f"""
             material:num-materials = {vampire.nmag}""")
    for i in range(vampire.nmag):
        with open(os.path.join(outdir,'vampire.mat'),'a') as f:
             f.write(f"""
             #---------------------------------------------------
             # Material {i+1}
             #---------------------------------------------------
             material[1]:material-name={vampire.metal_labels[i]}
             material[1]:damping-constant=1.0
             material[1]:atomic-spin-moment={vampire.metal_magmom[i]}
             material[1]:uniaxial-anisotropy-constant={vampire.anisotropy}
             material[1]:material-element={vampire.metal_labels[i]}
             material[1]:initial-spin-direction = {vampire.spin_dir}
             material[1]:uniaxial-anisotropy-direction = {vampire.aniso_dir}
             #---------------------------------------------------""")
    with open(os.path.join(outdir,'vampire.mat'),'a') as f:
         f.write('             # Interactions')

def transform_exchange():
    file = os.path.join(os.path.dirname(input_dir),'exchange_file.txt')
    J1, J2, J3 = np.loadtxt(file, delimiter=' ', usecols=(0, 2))
    J1 = 2 * J1 * 1.6021773e-22
    J2 = 2 * J2 * 1.6021773e-22
    J3 = 2 * J3 * 1.6021773e-22
    return J1, J2, J3

def write_ucf():
    with open(os.path.join(outdir,'vampire.UCF'),'w') as f:
         f.write(f"""
         # Unit cell size (Angstrom):
         1 1 1
         # Unit cell lattice vectors:
         {vampire.cell_parameters[0,0]} {vampire.cell_parameters[0,1]} {vampire.cell_parameters[0,2]} 
         {vampire.cell_parameters[1,0]} {vampire.cell_parameters[1,1]} {vampire.cell_parameters[1,2]} 
         {vampire.cell_parameters[2,0]} {vampire.cell_parameters[2,1]} {vampire.cell_parameters[2,2]} 
         # Atoms
         {vampire.nmag} {vampire.nmag}""")
         for i in range(vampire.nat):   
             f.write(f"""         
         {i} {vampire.coordinates[i,0]} {vampire.coordinates[i,1]} {vampire.coordinates[i,2]} {i}""")
         f.write('\n')
         f.write('         # Interactions\n')
         f.write(f'         {2*vampire.nmag**2} tensorial')
         f.write(f"""
         0  0  0  -1  0  0  {J1} 0.0 0.0 0.0  {J1} 0.0 0.0 0.0 {J1} 
         1  1  1  -1  0  0  {J1} 0.0 0.0 0.0  {J1} 0.0 0.0 0.0 {J1}
         2  2  2  -1  0  0  {J1} 0.0 0.0 0.0  {J1} 0.0 0.0 0.0 {J1}  
         3  3  3  -1  0  0  {J1} 0.0 0.0 0.0  {J1} 0.0 0.0 0.0 {J1}
         4  0  0   1  0  0  {J1} 0.0 0.0 0.0  {J1} 0.0 0.0 0.0 {J1}
         5  1  1   1  0  0  {J1} 0.0 0.0 0.0  {J1} 0.0 0.0 0.0 {J1}
         6  2  2   1  0  0  {J1} 0.0 0.0 0.0  {J1} 0.0 0.0 0.0 {J1} 
         7  3  3   1  0  0  {J1} 0.0 0.0 0.0  {J1} 0.0 0.0 0.0 {J1}
         8  1  0  -1  0  0  {J2} 0.0 0.0 0.0  {J2} 0.0 0.0 0.0 {J2}
         9  3  2  -1  0  0  {J2} 0.0 0.0 0.0  {J2} 0.0 0.0 0.0 {J2}
         10 0  1   0 -1  0  {J2} 0.0 0.0 0.0  {J2} 0.0 0.0 0.0 {J2}
         11 0  1   0  0  0  {J2} 0.0 0.0 0.0  {J2} 0.0 0.0 0.0 {J2} 
         12 2  3   0 -1  0  {J2} 0.0 0.0 0.0  {J2} 0.0 0.0 0.0 {J2} 
         13 1  0   0  0  0  {J2} 0.0 0.0 0.0  {J2} 0.0 0.0 0.0 {J2} 
         14 2  3   0  0  0  {J2} 0.0 0.0 0.0  {J2} 0.0 0.0 0.0 {J2} 
         15 3  2   0  0  0  {J2} 0.0 0.0 0.0  {J2} 0.0 0.0 0.0 {J2} 
         16 1  0   0  1  0  {J2} 0.0 0.0 0.0  {J2} 0.0 0.0 0.0 {J2}
         17 3  2   0  1  0  {J2} 0.0 0.0 0.0  {J2} 0.0 0.0 0.0 {J2}
         18 0  1   1  0  0  {J2} 0.0 0.0 0.0  {J2} 0.0 0.0 0.0 {J2}  
         19 2  3   1  0  0  {J2} 0.0 0.0 0.0  {J2} 0.0 0.0 0.0 {J2} 
         20 0  1   1 -1  0  {J2} 0.0 0.0 0.0  {J2} 0.0 0.0 0.0 {J2} 
         21 2  3   1 -1  0  {J2} 0.0 0.0 0.0  {J2} 0.0 0.0 0.0 {J2}
         22 1  0  -1  1  0  {J2} 0.0 0.0 0.0  {J2} 0.0 0.0 0.0 {J2} 
         23 3  2  -1  1  0  {J2} 0.0 0.0 0.0  {J2} 0.0 0.0 0.0 {J2}
         24 0  0   0 -1  0  {J3} 0.0 0.0 0.0  {J3} 0.0 0.0 0.0 {J3} 
         25 1  1   0 -1  0  {J3} 0.0 0.0 0.0  {J3} 0.0 0.0 0.0 {J3} 
         26 2  2   0 -1  0  {J3} 0.0 0.0 0.0  {J3} 0.0 0.0 0.0 {J3} 
         27 3  3   0 -1  0  {J3} 0.0 0.0 0.0  {J3} 0.0 0.0 0.0 {J3} 
         28 0  0   0  1  0  {J3} 0.0 0.0 0.0  {J3} 0.0 0.0 0.0 {J3}  
         29 1  1   0  1  0  {J3} 0.0 0.0 0.0  {J3} 0.0 0.0 0.0 {J3} 
         30 2  2   0  1  0  {J3} 0.0 0.0 0.0  {J3} 0.0 0.0 0.0 {J3} 
         31 3  3   0  1  0  {J3} 0.0 0.0 0.0  {J3} 0.0 0.0 0.0 {J3} 
         """)

if __name__ == "__main__":
    anisotropy = 0.0
    aniso_dir = 'x'
    spin_dir = 'z'
    input_dir = 'POSCAR'
    input_dir2 = 'OUTCAR'
    Tmax = 1000
    Tstep = 1
    eq_steps = 100000
    loop_steps = 10000
    outdir = '.'
    vampire = Vampire()
    vasp_prepare_data()
    write_input()
    write_mat()
    J1, J2, J3 = transform_exchange()
    write_ucf()
        