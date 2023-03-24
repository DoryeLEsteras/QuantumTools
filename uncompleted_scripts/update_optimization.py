from typing import List
from argparse import ArgumentParser
from QuantumTools.library import QECalculation, QEoutput

"""
Instructions:
1. class extract input data -> done
2. read input and store in vector (it will be cloned) -> done
3. class output extracts coordinates and cell parameters -> done
4. if relax -> update coordinates elif vcrelax and cell_dofree != ibrav update
coordinates and cell parameters; elif vcrelax and cell_dofree == ibrav transform
to ibrav != 0 and update coordinates and cell parameters.
5. if End final coordinates -> new input is an scf (think about expanding possibilities)
# chekear error en cell parameters
"""

def store_input_file(input_file_name_and_dir:str) -> List:
   input_file = open(input_file_name_and_dir,'r')
   file_vector = input_file.readlines()
   return file_vector


if __name__ == '__main__':
  opt_input_dir_and_name = './debug_update_opt/relax.in'
  opt_out_dir_and_name = './debug_update_opt/nii2.vcrelax.out'
  #opt_out_name, opt_out_dir = manage_input_dir(opt_out_dir_and_name)
  #opt_input_name, opt_input_dir = manage_input_dir(opt_input_dir_and_name)
  Optimization = QECalculation()
  Optimization.extract_input_information(opt_input_dir_and_name)
  input_vector = store_input_file(opt_input_dir_and_name)
  Output = QEoutput()
  Output.extract_output_information(opt_out_dir_and_name)

  #test_output = open('test.txt','w')
  #for line in input_vector:
  #  test_output.write(line)

