from typing import List
from argparse import ArgumentParser
from QuantumTools.library import QECalculation, QEoutput, manage_input_dir
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
def substitute_coordinates(input_file_name_and_dir:str, new_coordinates: np.ndarray) -> List:
   input_file = open(input_file_name_and_dir,'r')
   file_vector = input_file.readlines()
   for line_number,line in enumerate(file_vector):
       splited_line = line.split();splited_line.append('end')
       if splited_line[0] == 'ATOMIC_POSITIONS':
          for i in range(0,Optimization.nat,1):
              file_vector[line_number + i +1] = str(new_coordinates[i])
   return file_vector


if __name__ == '__main__':
  subfix = '2'
  opt_input_dir_and_name = './debug_update_opt/first.stacking.vcrelax.in'
  opt_out_dir_and_name = './debug_update_opt/first.stacking.vcrelax.out'
  opt_out_name, opt_out_dir = manage_input_dir(opt_out_dir_and_name)
  opt_input_name, opt_input_dir = manage_input_dir(opt_input_dir_and_name)
  Optimization = QECalculation()
  Optimization.extract_input_information(opt_input_dir_and_name)
  Output = QEoutput()
  Output.extract_output_information(opt_out_dir_and_name)
  if Output.calculation_finished == 1:
     print('prepare scf (soc no soc ?)')
  elif Optimization.calculation_type == 'relax':
       generated_file = open(opt_out_dir + opt_input_name.replace('relax','relax' + subfix),'w')
       input_vector = substitute_coordinates(opt_input_dir_and_name,Output.atomic_matrix)
       print(input_vector)      
       #generated_file.write(input_vector)

   # update coordinates  
 # elif Optimization.calculation_type == 'vc-relax' and Optimization.cell_dofree != 'ibrav':
  # update coordinates and cell param
 # elif Optimization.calculation_type == 'vc-relax' and Optimization.cell_dofree == 'ibrav':
     #duru
