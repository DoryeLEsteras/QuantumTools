#!/usr/bin/python3
from argparse import ArgumentParser
from typing import List
from QuantumTools.qe_tools import QECalculation
from QuantumTools.cluster_tools import initialize_clusters
from QuantumTools.directory_and_files_tools import manage_input_dir

def parser():
    parser = ArgumentParser(description="Script to create inputs for Force theorem calculations")
    parser.add_argument("-input", "--input",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the scf input file
                        """)
    parser.add_argument("-outdir", "--outdir",
                        type=str,
                        required=False,
                        default='./',
                        help="Relative or absolute path for output directory ")
    parser.add_argument("-k", "--k",
                        type=str,
                        required=True,
                        nargs='+',
                        help="kx ky kz for nscf calculations ")
    parser.add_argument("-conv", "--conv",
                        type=int,
                        required=True,
                        help="convergence threshold for nscf calculations")
    parser.add_argument("-mat", "--mat",
                        type=str,
                        nargs='+',
                        required=True,
                        help="Label of the magnetic atoms. Separator: spaces.")
    args = parser.parse_args()
    return args.input,args.outdir,args.k,args.conv,args.mat
    
def manage_magnetic_species(scf_input_name:str,scf_dir:str)-> List:
    scf_input_file_name = scf_dir + '/' + scf_input_name
    with open(scf_input_file_name, 'r') as scf_file:
        text = scf_file.readlines()
    pos = 1; at_type_list = [];magnetic_atom_index_list = [];pp_list = []

    # export outside
    for line_number, line in enumerate(text): 
        if line == 'ATOMIC_SPECIES\n':
           for i in range (0, Scf.ntyp ,1):
               at_type_list.append(text[line_number + pos].split()[0])
               pp_list.append(text[line_number + pos])
               pos = pos + 1

    for atom_species_number, atom_species in enumerate(at_type_list):
        for magnetic_atom_number, magnetic_atom in enumerate(mat):
            if atom_species == magnetic_atom :
               magnetic_atom_index_list.append(int(atom_species_number)+1)

    for h in range(0,len(pp_list),1):
        pp_list[h] = pp_list[h].replace(at_type_list[h] + '.',str(at_type_list[h]) + '.rel-')
    return magnetic_atom_index_list,pp_list
def manage_angles(magnetic_atom_index_list:List,spin_direction:str)-> str:
    angle_line = ''
    if spin_direction == 'x':
       angle1 = 90
       angle2 = 0
    if spin_direction == 'y':
       angle1 = 90
       angle2 = 90
    if spin_direction == 'z':
       angle1 = 0
       angle2 = 0
    for index, element_position in enumerate(magnetic_atom_index_list):
      angle_line = angle_line + 'angle1(' + str(element_position) + ') = ' + str(angle1) + '\n'
      angle_line = angle_line + 'angle2(' + str(element_position) + ') = ' + str(angle2) + '\n'
    return angle_line   
def create_nscf_input(scf_input_name:str,scf_dir:str,nscf_output_dir:str,spin_direction:str,magnetic_atom_index_list:List,pp_list:List)-> None: 
    nscf_name = scf_input_name.replace('scf',spin_direction + '.nscf')
    nscf_file = open(nscf_output_dir + '/' + nscf_name , 'w')
    scf_input_file = open(scf_dir + '/' + scf_input_name , 'r')
    angle_line = manage_angles(magnetic_atom_index_list,spin_direction)
    for line in scf_input_file:
        line_to_check = line.replace("=", ' ') 
        line_to_check = line_to_check.replace(",", ' ') 
        line_to_check_vector = line_to_check.split()
        line_to_check_vector.append('end')
        if line_to_check_vector[0] == 'calculation':
           security_check = line_to_check_vector[1]
           line = 'calculation = \'nscf\'\n'
        if line_to_check_vector[0] == 'verbosity':
           line = 'verbosity = \'high\'\n'
        if line_to_check_vector[0] == 'outdir':
           line = "outdir = '" +  Scf.outdir.replace('tmp','tmp' + '_' + spin_direction) + "'\n"
        if line_to_check_vector[0] == 'conv_thr':
           line = 'conv_thr =   1.0d' + str(conv) + '\n'
        if line_to_check_vector[0] == 'nspin':
           line = ''
        if line_to_check_vector[0] == '&system' or line_to_check_vector[0] == '&SYSTEM':
           line = '&SYSTEM\n' + 'nosym=.true.\n' + \
            'lforcet = .true.\n' + 'lspinorb = .true.\n' + 'noncolin= .true.\n' + angle_line         
        if line_to_check_vector[0] == 'ATOMIC_SPECIES':
         line = 'ATOMIC_SPECIES\n'
         for i in range(0,len(pp_list),1):
             line = line + str(pp_list[i])
             scf_input_file.readline()
         
        if line_to_check_vector[0] == '&electrons' or line_to_check_vector[0] == '&ELECTRONS':
           line = '&ELECTRONS\n' + "startingpot = 'file' \n"
        if line_to_check_vector[0] == 'k_points' or line_to_check_vector[0] == 'K_POINTS':
          line = 'K_POINTS automatic\n' + str(k[0]) + " " + str(k[1]) + " " + str(k[2]) + ' 0 0 0\n'
          scf_input_file.readline()
        nscf_file.write(str(line))
    scf_input_file.close()
    nscf_file.close()




if __name__ == '__main__':   
  provided_scf_input_file, provided_output_dir,k,conv,mat = parser()
  Scf = QECalculation()
  Scf.extract_input_information(provided_scf_input_file)
  if Scf.calculation_type != 'scf':
     print('ERROR: provided scf input does not correspond to scf calculation')
  if Scf.nspin == 4:
     print('ERROR: noncolinear flags in scf')
  else:  
     file_name,file_dir = manage_input_dir(provided_scf_input_file)
     magnetic_atom_index_list,pp_list = manage_magnetic_species(file_name,file_dir)
     create_nscf_input(file_name,file_dir,provided_output_dir,'x',magnetic_atom_index_list,pp_list)
     create_nscf_input(file_name,file_dir,provided_output_dir,'y',magnetic_atom_index_list,pp_list)
     create_nscf_input(file_name,file_dir,provided_output_dir,'z',magnetic_atom_index_list,pp_list)
     initialize_clusters('force_theorem',file_dir,file_name,'')
     print('check the names of relativistic PPs')
     



