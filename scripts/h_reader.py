#!/usr/bin/python3
import numpy as np
from argparse import ArgumentParser
from typing import List,Tuple,TextIO
import os


# TO DO LIST
"""
- pep8 lenght 
- las funciones reciben mas parametros de los necesarios
- norb no debe ser 20 debe ser un str 1-20 en el parser.
  Esto se propaga y tiene 3 consecuencias: 1. Hacer que el codigo admita casos donde los orbitales seleccionados
  no estan al principio del H, 2. generalizar el codigo para cualquier grupo de orbitales que no sean d o f
  y 3. refactorizar la parte de bucles que genera las matrices en una funcion sencilla
  Hints:
       - parser norb es str
       - en create_hamiltonians: norb = norb.split('-') ; norb_dim = max-min +1; min = norb[0]; max = norb[1]
"""     
# DESCRIPTION
"""
Reformats and filters the Hamiltonian extracting hoppings, that can be rounded
for better analysis. 
"""

"""
def fragment_hamiltonian(fragment:str,file_to_write:TextIO,hamiltonian_fragment:np.ndarray,norb_dim:int,min:int,hamiltonian:np.ndarray): 
    for index1 in range(1, nwan-norb_dim+1, 1):
        for index2 in range(1, nwan-norb_dim+1, 1):
            if fragment == 'selection':
               old_index1 = index1 + min - 1
               old_index2 = index2 + min - 1
            elif fragment == 'no_selection':
               old_index1 = -index1 + min - 1
               old_index2 = -index2 + min - 1
            elif fragment == 'selected_unselected':    
               old_index1 =  index1 + min 
               old_index2 = -index2 + min
            elif fragment == 'unselected_selected':
               old_index1 = -index1 + min 
               old_index2 =  index2 + min

            hamiltonian_fragment[index1-1][index2-1] = hamiltonian[old_index1][old_index2] 
            if hamiltonian_fragment[index1-1][index2-1] > 0 and hamiltonian_fragment[index1-1][index2-1] < cut: #filter data here
               hamiltonian_fragment[index1-1][index2-1] = 0
            if hamiltonian_fragment[index1-1][index2-1] < 0 and hamiltonian_fragment[index1-1][index2-1] > -cut: #filter data here
               hamiltonian_fragment[index1-1][index2-1] = 0
            file_to_write.write(str(hamiltonian_fragment[index1-1][index2-1]))
            file_to_write.write(' ')
        file_to_write.write('\n')
    file_to_write.close()
"""

def parser():
    parser = ArgumentParser(description="""Script to transform Wannier Hamiltonian 
                                         and extract hopping parameters""")
    parser.add_argument("-input", "--input",
                        type=str,
                        required=True,
                        help="""
                        file name including directory to the input file, produced
                        by the grep command
                        """)  
    parser.add_argument("-cut", "--cut",
                        type=float,
                        required=False,
                        default= '0.0001',
                        help="""
                        Cutoff to round the hopping parameters
                        """)  
    parser.add_argument("-outdir", "--outdir",
                        type=str,
                        required=False,
                        default= '.',
                        help="""
                        outpur directory
                        """)                              
    parser.add_argument("-norb", "--norb",
                        type=int,
                        required=True,
                        help="""
                        Range of orbitals to study in format: First-Last
                        Ex: 1-20 
                        """)
    args = parser.parse_args()
    return args.input,args.cut,args.outdir,args.norb

def read_file(provided_input_name_and_dir:str) -> Tuple[List, int]:
    with open(provided_input_name_and_dir,'r') as f:
         read_vector = f.readlines()
    nwan = int(read_vector[1])
    return read_vector, nwan

def define_hamiltonian(read_vector:List,nwan:int,cell:str) -> np.ndarray:    
    # create Hamiltonian matrix
    hamiltonian = np.zeros((nwan, nwan))
    cell = cell.split()
    for line in read_vector:
        line=line.split()
        if len(line) == 7:
            if line[0] == cell[0] and line[1] == cell[1] and line[2] == cell[2]:
                i = int(line[3]) 
                j = int(line[4])
                real = line[5]
                im = line[6]
                hamiltonian [i-1][j-1] = round(float(real),4)
    return hamiltonian 

def create_hamiltonians(outdir:str,hamiltonian:np.ndarray,nwan:int,norb:int,cell:str) -> None:
    d_d_hamiltonian = np.zeros((norb,norb))
    ligand_ligand_hamiltonian = np.zeros((nwan - norb, nwan - norb))
    d_ligand_hamiltonian = np.zeros((norb, nwan - norb))
    ligand_d_hamiltonian = np.zeros((nwan - norb, norb))
    provided_output_name_d_d_hoppings = cell.replace(' ','_') + '_d_d_hoppings.txt'
    provided_output_name_d_l_hoppings = cell.replace(' ','_') + '_d_l_hoppings.txt'
    provided_output_name_l_d_hoppings = cell.replace(' ','_') + '_l_d_hoppings.txt'
    provided_output_name_l_l_hoppings = cell.replace(' ','_') + '_l_l_hoppings.txt'
    d_d_output_file = open(os.path.join(outdir,provided_output_name_d_d_hoppings), 'w')
    d_l_output_file = open(os.path.join(outdir,provided_output_name_d_l_hoppings), 'w')
    l_d_output_file = open(os.path.join(outdir,provided_output_name_l_d_hoppings), 'w')
    l_l_output_file = open(os.path.join(outdir,provided_output_name_l_l_hoppings), 'w')
    """
     given the Hamiltonian create sub hamiltonians dividing just d-d ligand-ligand
     and diagonals
     __________________
     |   d-d |   d-l  |
     |_______|________|
     |  l-d  |   l-l  |
     |_______|________| 

    d could be f orbitals (or personalised groups of orbitals)
    """
    
#    fragment_hamiltonian('selection',d_d_hamiltonian,d_d_output_file,20,1,hamiltonian) 
    
    # d_d_hoppings
    for index1 in range(1, norb+1, 1):
        for index2 in range(1, norb+1, 1):
            d_d_hamiltonian[index1-1][index2-1] = hamiltonian[index1-1][index2-1]
            if d_d_hamiltonian[index1-1][index2-1] > 0 and d_d_hamiltonian[index1-1][index2-1] < cut: #filter data here
               d_d_hamiltonian[index1-1][index2-1] = 0 
            if d_d_hamiltonian[index1-1][index2-1] < 0 and d_d_hamiltonian[index1-1][index2-1] > -cut: #filter data here
               d_d_hamiltonian[index1-1][index2-1] = 0         
            d_d_output_file.write(str(d_d_hamiltonian[index1-1][index2-1]))
            d_d_output_file.write(' ')
        d_d_output_file.write('\n')
    d_d_output_file.close()

    # l_l_hoppings
    for index1 in range(1, nwan-norb+1, 1):
        for index2 in range(1, nwan-norb+1, 1):
            old_index1 = index1 + norb
            old_index2 = index2 + norb
            ligand_ligand_hamiltonian[index1-1][index2-1] = hamiltonian[old_index1-1][old_index2-1] 
            if ligand_ligand_hamiltonian[index1-1][index2-1] > 0 and ligand_ligand_hamiltonian[index1-1][index2-1] < cut: #filter data here
               ligand_ligand_hamiltonian[index1-1][index2-1] = 0
            if ligand_ligand_hamiltonian[index1-1][index2-1] < 0 and ligand_ligand_hamiltonian[index1-1][index2-1] > -cut: #filter data here
               ligand_ligand_hamiltonian[index1-1][index2-1] = 0
            l_l_output_file.write(str(ligand_ligand_hamiltonian[index1-1][index2-1]))
            l_l_output_file.write(' ')
        l_l_output_file.write('\n')
    l_l_output_file.close()

    # d_l_hoppings
    for index1 in range(1, norb+1, 1):
        for index2 in range(1, nwan-norb+1, 1):
            old_index1 = index1 
            old_index2 = index2 + norb
            d_ligand_hamiltonian[index1-1][index2-1] = hamiltonian[old_index1-1][old_index2-1] 
            if d_ligand_hamiltonian[index1-1][index2-1] > 0 and d_ligand_hamiltonian[index1-1][index2-1] < cut: #filter data here
               d_ligand_hamiltonian[index1-1][index2-1] = 0 
            if d_ligand_hamiltonian[index1-1][index2-1] < 0 and d_ligand_hamiltonian[index1-1][index2-1] > -cut: #filter data here
               d_ligand_hamiltonian[index1-1][index2-1] = 0 
            d_l_output_file.write(str(d_ligand_hamiltonian[index1-1][index2-1]))
            d_l_output_file.write('  ')
        d_l_output_file.write('\n')
    d_l_output_file.close()

    # l_d_hoppings
    for index1 in range(1, nwan-norb + 1, 1):
        for index2 in range(1, norb + 1, 1):
            old_index1 = index1 + norb 
            old_index2 = index2 
            ligand_d_hamiltonian[index1-1][index2-1] = hamiltonian[old_index1-1][old_index2-1] 
            if ligand_d_hamiltonian[index1-1][index2-1] > 0 and ligand_d_hamiltonian[index1-1][index2-1] < cut: #filter data here
               ligand_d_hamiltonian[index1-1][index2-1] = 0 
            if ligand_d_hamiltonian[index1-1][index2-1] < 0 and ligand_d_hamiltonian[index1-1][index2-1] > -cut: #filter data here
               ligand_d_hamiltonian[index1-1][index2-1] = 0 
            l_d_output_file.write(str(ligand_d_hamiltonian[index1-1][index2-1]))
            l_d_output_file.write(' ')
        l_d_output_file.write('\n')
    l_d_output_file.close()
    

if __name__ == '__main__':
    provided_input_name_and_dir,cut,outdir,norb = parser()
    readed_H,nwan = read_file(provided_input_name_and_dir)
    # Extract the cells around 0 0 0 and 0 0 0 itself
    cells_to_extract = ['0 0 0','-1 0 0','1 0 0','0 -1 0',
                        '0 1 0','-1 -1 0','1 1 0','-1 1 0','1 -1 0']
    for cell in cells_to_extract:
        hamiltonian = define_hamiltonian(readed_H,nwan,cell)
        create_hamiltonians(outdir,hamiltonian,nwan,norb,cell)