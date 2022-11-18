import numpy as np
from argparse import ArgumentParser


# TO DO LIST
"""
- more submatrices to understand the hoppings (for example take the d-ligand)
  and do just dij -px, just dij-py ...; just particular Fe atom...
- parser
- put different output files (you are reusing one outputname all the time)
"""

# Instructions 

"""
The input is directly the grep '0 0 0' of the hr file
"""

nwan = 84; 
dorbitals = 20

input_file = open('h_up_000.dat', 'r')
output_file = open('test.txt', 'a')

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

for index1 in range(1, dorbitals, 1):
    for index2 in range(1, dorbitals, 1):
        d_d_hamiltonian[index1-1][index2-1] = hamiltonian[index1-1][index2-1] 
        #output_file.write(str(d_d_hamiltonian[index1-1][index2-1]))
        #output_file.write(' ')
    #output_file.write('\n')

for index1 in range(1, nwan-dorbitals+1, 1):
    for index2 in range(1, nwan-dorbitals+1, 1):
        old_index1 = index1 + dorbitals
        old_index2 = index2 + dorbitals
        ligand_ligand_hamiltonian[index1-1][index2-1] = hamiltonian[old_index1-1][old_index2-1] 
        #output_file.write(str(ligand_ligand_hamiltonian[index1-1][index2-1]))
        #output_file.write(' ')
    #output_file.write('\n')

for index1 in range(1, dorbitals+1, 1):
    for index2 in range(1, nwan-dorbitals+1, 1):
        old_index1 = index1 
        old_index2 = index2 + dorbitals 
        d_ligand_hamiltonian[index1-1][index2-1] = hamiltonian[old_index1-1][old_index2-1] 
        if d_ligand_hamiltonian[index1-1][index2-1] < 0.01: #filter data here
           d_ligand_hamiltonian[index1-1][index2-1] = 0
        output_file.write(str(d_ligand_hamiltonian[index1-1][index2-1]))
        output_file.write(' | ')
    output_file.write('\n')

for index1 in range(1, nwan-dorbitals+1, 1):
    for index2 in range(1, dorbitals+1, 1):
        old_index1 = index1 + dorbitals 
        old_index2 = index2 
        ligand_d_hamiltonian[index1-1][index2-1] = hamiltonian[old_index1-1][old_index2-1] 
        #output_file.write(str(ligand_d_hamiltonian[index1-1][index2-1]))
        #output_file.write(' ')
    #output_file.write('\n')




