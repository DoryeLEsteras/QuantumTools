
import os
from argparse import ArgumentParser

from typing import List
import numpy as np
from QuantumTools.library import manage_input_dir, substitute_pattern,initialize_clusters, QECalculation




"""
AA AB AC
BA BB BC
CA CB CC
"""

# como se gestionara esto, tiene que ser siempre ibrav 0? con cell param en angstrom?
# hay que cuidar que las coordenadas sean en crystal?
#

def create_scan(line_to_be_modified:int, readed_vector:List) -> None:
    Scf = QECalculation()
    Scf.extract_input_information(file_dir_and_name)
    original_cell_parameters = Scf.cell_matrix_angstrom

"""
    if str(original_kp[2]) == '1':
        for i in range(kpmin,kpmax + kpstep,kpstep):
            new_file_name = file_name.replace('scf.in', 'kx' + str(i) + '.ky'  + str(i) + '.kz' + '1' + '.scf.in')  
            readed_vector[line_to_be_modified] = str(i) + " " + str(i) + " " + '1 ' + str(Scf.kpoints[3]) +\
                 " " +  str(Scf.kpoints[4]) + " " + str(Scf.kpoints[5])
            with open(os.path.join(file_dir,new_file_name),'w') as file:
                for line in readed_vector:
                    file.write(line) 
    if str(original_kp[2]) != '1':
        for i in range(kpmin,kpmax + kpstep,kpstep): 
            new_file_name = file_name.replace('scf.in', 'kx' + str(i) + '.ky'  + str(i) + '.kz' + str(i) + '.scf.in')  
            readed_vector[line_to_be_modified] = str(i) + " " + str(i) + " " + str(i) + " "  + str(Scf.kpoints[3]) +\
                   " " +  str(Scf.kpoints[4]) + " " + str(Scf.kpoints[5])
            with open(os.path.join(file_dir,new_file_name),'w') as file:
                for line in readed_vector:
                    file.write(line) 
"""

if __name__ == '__main__':
    #file_dir_and_name,outdir,kpmin,kpmax,kpstep = parser()
    file_dir_and_name = '.\'
    file_name,file_dir = manage_input_dir(file_dir_and_name)
    line_to_be_modified,readed_vector = extract_info()
    create_scan(line_to_be_modified,readed_vector)