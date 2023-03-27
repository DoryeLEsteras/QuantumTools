from typing import List
from argparse import ArgumentParser
from QuantumTools.library import QECalculation, QEoutput, manage_input_dir,\
clean_uncommented_file
import numpy as np
"""
Instructions:
1. class extract input data -> done
2. read input and store in vector (it will be cloned) -> done
3. class output extracts coordinates and cell parameters -> done

4. if relax -> update coordinates elif vcrelax and cell_dofree != ibrav update
coordinates and cell parameters; elif vcrelax and cell_dofree == ibrav transform
to ibrav != 0 and update coordinates and cell parameters.if End final coordinates -> new input is an scf (think about expanding possibilities)
5. chekear error en cell parameters
# implement do something with the 0 0 0 at the right of coordinates
"""
# this is going to be the phylosophy create these functions to substitute cell and coordinates
def substitute_coordinates(file_vector:List[str], new_coordinates: np.ndarray) -> List[str]:
   for line_number,line in enumerate(file_vector):
       splited_line = line.split();splited_line.append('end')
       if splited_line[0] == 'ATOMIC_POSITIONS':
          for i in range(0,Optimization.nat,1):
              file_vector[line_number + i +1] = str(new_coordinates[i])
   return file_vector
def substitute_cell_parameters(file_vector:List[str], new_cell_parameters: np.ndarray) ->List[str]:
   for line_number,line in enumerate(file_vector):
       splited_line = line.split();splited_line.append('end')
       if splited_line[0] == 'CELL_PARAMETERS':
          for i in range(0,3,1):
              file_vector[line_number + i +1] = str(new_cell_parameters[i])
   return file_vector

if __name__ == '__main__':
  subfix = '2'
  opt_input_dir_and_name = './debug_update_opt/relax.in'
  opt_out_dir_and_name = './debug_update_opt/o2.relax.out'
  opt_out_name, opt_out_dir = manage_input_dir(opt_out_dir_and_name)
  opt_input_name, opt_input_dir = manage_input_dir(opt_input_dir_and_name)
  Optimization = QECalculation()
  Optimization.extract_input_information(opt_input_dir_and_name)
  Output = QEoutput()
  Output.extract_output_information(opt_out_dir_and_name)

  input_file = open(opt_input_dir_and_name,'r')
  file_vector = input_file.readlines()  
  updated_file_vector = substitute_coordinates(file_vector,Output.atomic_matrix)
  if Optimization.calculation_type == 'vc-relax': 
     updated_file_vector = substitute_cell_parameters(updated_file_vector,Output.cell_matrix)
     if Optimization.cell_dofree == 'ibrav': 
          print('WARNING: vc-relax with cell_dofree = ibrav, move the new input\
          from ibrav 0 to ibrav != 0') 

  if Output.calculation_finished != 1:
     generated_file = open(opt_out_dir + opt_input_name.replace('relax','relax' + subfix),'w') 
  elif Output.calculation_finished == 1:
     generated_file = open(opt_out_dir + opt_input_name.replace('relax','scf'),'w')
     #ACABAR ESTO
     file_clean_copy = clean_uncommented_file(updated_file_vector)
     for line_number,line in enumerate(file_clean_copy):
         line = line.split()
         line.append('end')
         if line[0] == 'calculation':
             updated_file_vector[line_number] = "calculation = 'scf'\n"
         if line[0] == 'etot_conv_thr': 
              updated_file_vector[line_number] = ''
         if line[0] == 'forc_conv_thr': 
              updated_file_vector[line_number] = ''
         if line[0] == 'nstep': 
              updated_file_vector[line_number] = ''
         if line[0] == 'tstress': 
             updated_file_vector[line_number] = "tstress = .false.\n "
             print('Warning: pressure deactivated to avoid problems')
         if line[0] == 'tprnfor': 
             updated_file_vector[line_number] = "tprnfor = .false.\n "
             print('Warning: forces deactivated to avoid problems')
         if line[0] == '&CELL' or line[0] == '&IONS': 
             updated_file_vector[line_number] = ''
             check = updated_file_vector[line_number+1]
             check = check.split('=')
             check.append('end')
             if check[0] == '/':
                updated_file_vector[line_number+1] = ''
             if check[0] == '/n':
                updated_file_vector[line_number+1] = ''
                updated_file_vector[line_number+2] = ''
             if check[0] == 'cell_dofree':
                updated_file_vector[line_number+1] = ''
                updated_file_vector[line_number+2]= ''
         if line[0] == '&IONS': 
             updated_file_vector[line_number] = ''
  for line in updated_file_vector:
      generated_file.write(line)
      """
    inside of these two modes we should consider four options:
    - ibrav = 0 and there is no a -> cell parameters are in A, is direct
    - ibrav = 0 and there is  a -> cell parameters are in crystal, is direct (is better 
    to put express cell parameters as cell*a to avoid problems with possible wannier and remove
    the a in the input)
    -ibrav != 0 and cell_dofree != ibrav -> change ibrav line to 0 and put cell parameters
    in A
    -ibrav != 0 and cell_dofree = ibrav -> we are fucked, warning to user
    """
