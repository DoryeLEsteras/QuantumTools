#!/usr/bin/python3
import numpy as np
from argparse import ArgumentParser


# TO DO LIST
"""
- Using an input more standard than the grep 0 0 0
- Thus, extending in a better way to other cell hoppings
- add possibility of output directory
- fix the name of the output, now is weird, instead of parsering a label,
  you can parse an outdir and having an internal prefix. Also the extension
  of the output files is missing
- parser nwan and d orbitals
- more submatrices to understand the hoppings (for example take the d-ligand)
  and do just dij -px, just dij-py ...; just particular Fe atom...
"""

# DESCRIPTION
"""
Reformats and filters the Hamiltonian extracting hoppings, that can be rounded
for better analysis. The input and the possibility of more cells than the 0 0 0
is still rudimentary
"""

def parser():
    parser = ArgumentParser(description="""Script to transform Wannier Hamiltonian 
                                         and extract hopping parameters""")
    parser.add_argument("-out", "--out",
                        type=str,
                        required=True,
                        help="""
                        Prefix for the output files
                        """)   
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
                        help="""
                        Cutoff to round the hopping parameters
                        """)     
    args = parser.parse_args()
    return args.input,args.out,args.cut

# Instructions 

"""
The input is directly the grep '0 0 0' of the hr file
"""
nwan = 56
dorbitals = 20

# personalized ranges of the matrix NOT IMPLEMENTED
#selected_col=29
#selected_row=1

provided_input_name,provided_output_name,cut = parser()
if cut == None:
   cut = 0.0001
input_file = open(provided_input_name, 'r')
provided_output_name_d_d_hoppings = 'd_d_hoppings.' + provided_output_name
provided_output_name_d_l_hoppings = 'd_l_hoppings.' + provided_output_name
provided_output_name_l_d_hoppings = 'l_d_hoppings.' + provided_output_name
provided_output_name_l_l_hoppings = 'l_l_hoppings.' + provided_output_name
d_d_output_file = open(provided_output_name_d_d_hoppings, 'w')
d_l_output_file = open(provided_output_name_d_l_hoppings, 'w')
l_d_output_file = open(provided_output_name_l_d_hoppings, 'w')
l_l_output_file = open(provided_output_name_l_l_hoppings, 'w')

# create Hamiltonian
hamiltonian = np.zeros((nwan, nwan))
d_d_hamiltonian = np.zeros((dorbitals, dorbitals))
ligand_ligand_hamiltonian = np.zeros((nwan - dorbitals, nwan - dorbitals))
d_ligand_hamiltonian = np.zeros((dorbitals, nwan - dorbitals))
ligand_d_hamiltonian = np.zeros((nwan - dorbitals, dorbitals))
for line in input_file:
    readed_line=line.split()
    i = int(readed_line[3]) 
    j = int(readed_line[4])
    real = readed_line[5]
    im = readed_line[6]
    hamiltonian [i-1][j-1] = round(float(real),4)


# given the Hamiltonian create sub hamiltonians dividing just d-d ligand-ligand
# and diagonals

"""
 __________________
 |   d-d |   d-l  |
 |_______|________|
 |  l-d  |   l-l  |
 |_______|________| 

"""

# d_d_hoppings
for index1 in range(1, dorbitals+1, 1):
    for index2 in range(1, dorbitals+1, 1):
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
for index1 in range(1, nwan-dorbitals+1, 1):
    for index2 in range(1, nwan-dorbitals+1, 1):
        old_index1 = index1 + dorbitals
        old_index2 = index2 + dorbitals
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
for index1 in range(1, dorbitals+1, 1):
    for index2 in range(1, nwan-dorbitals+1, 1):
        old_index1 = index1 
        old_index2 = index2 + dorbitals 
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
for index1 in range(1, nwan-dorbitals+1, 1):
    for index2 in range(1, dorbitals+1, 1):
        old_index1 = index1 + dorbitals 
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


"""
for row in range(selected_row-1, selected_row+5, 1):
    for col in range(selected_col-1, selected_col+2, 1):
        output_file2.write(str(d_ligand_hamiltonian[selected_row][selected_col]))
        output_file2.write(' ')
    output_file2.write('\n')

"""
