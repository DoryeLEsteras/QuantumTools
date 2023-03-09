import numpy as np
from argparse import ArgumentParser
from subprocess import run
from QuantumTools.library import manage_input_dir, handle_comments, \
     clean_uncommented_file,extract_input_information,transform_lattice_parameters




def create_wan_nscf(file_name, file_dir, nbands, k):
    nscf_file_name = file_name.replace('scf','nscf')
    seed = nscf_file_name.replace('.nscf.in', '') 
    nscf_output = str(file_dir) + str(file_name)

    with open(file_name, 'r') as file:
        lines = file.readlines()    
    clean_file = clean_uncommented_file(lines)
    for line_number, line in enumerate(clean_file):   
        splitted_line = line.split(); splitted_line.append('end')  
        for word_number, word in enumerate(splitted_line):
            if word == 'calculation':
               clean_file[line_number] = 'calculation = \'nscf\'\n'
            if word == 'verbosity':
              clean_file[line_number] = 'verbosity = \'high\'\n'
            if word == '&system' or word == '&SYSTEM':
              clean_file[line_number] = '&SYSTEM\n' + 'nosym=.true.\n' + \
               'noinv=.true.\n' + 'nbnd = ' + str(nbands) + ' \n'
            if word == '&electrons' or word == '&ELECTRONS':
              clean_file[line_number] = '&ELECTRONS\n' + 'diago_full_acc=.true.\n'
            if word == 'k_points' or word == 'K_POINTS':
              clean_file[line_number] = ''    
              clean_file[line_number + 1] = ''            
            kmesh = run(['../../QuantumTools/kmesh.pl', \
                    str(k[0]), str(k[1]), str(k[2])],capture_output=True) 
            output = kmesh.stdout; kmesh = output.decode("utf-8")
    with open(nscf_file_name, 'w') as nscf_file:   
        for line in clean_file: 
            nscf_file.write(str(line))  
        nscf_file.write(kmesh)  





if __name__ == "__main__":
    file_dir_and_name = './feps3.a.a.scf.in'
    file_name, file_dir = manage_input_dir(file_dir_and_name)
    nbands = 1
    k = [1,1,1]
    uncommented_file = handle_comments(file_name)
    clean_file = clean_uncommented_file(uncommented_file)
    nat, calculation_type, prefix, outdir, ibrav, nspin, cell_parameters_units, \
    a, b, c, cosac, cosab, cosbc, cell_matrix, atomic_positions_units, \
    atomic_matrix, kpoints = extract_input_information(clean_file)
    cell_matrix_angstrom = transform_lattice_parameters(cell_matrix,ibrav,cell_parameters_units,
                                a,b,c,cosac,cosab,cosbc)

    create_wan_nscf(file_name, file_dir, nbands, k)

