from typing import List
from argparse import ArgumentParser
import numpy as np
#from subprocess import run
from QuantumTools.library import QECalculation, QEoutput, manage_input_dir,\
clean_uncommented_file, initialize_clusters

# TO DO LIST
"""
implement do something with the 0 0 0 at the right of coordinates
(library is already expanded, just i should consider if this columns appear in
the output. If the answer is yes, it should work, if not i should implement here
how to add the new coordinates + columns from the input)
# new options for scf
"""

"""
Instructions:
1. class extract input data  
2. read input and store in vector (it will be cloned)  
3. class output extracts coordinates and cell parameters  
4. modify the clone and generate input
"""

def parser():
    parser = ArgumentParser(description="Script for updating optimization calculations")
    parser.add_argument("-optin", "--optin",
                        type=str,
                        required=True,
                        help="""
                        Optimization input 
                        """)
    parser.add_argument("-optout", "--optout",
                        type=str,
                        required=True,
                        help="""
                        Optimization output
                        """)    
    parser.add_argument("-newname", "--newname",
                        type=str,
                        required=False,
                        default= 'created_new_file.in',
                        help="""
                        Name for the new input if optimization did not finish
                        """)  
 
    args = parser.parse_args()
    return args.optin,args.optout,args.newname
def substitute_coordinates(file_vector:List[str], new_coordinates: np.ndarray) -> List[str]:
   for line_number,line in enumerate(file_vector):
      splited_line = line.split();splited_line.append('end')
      if splited_line[0] == 'ATOMIC_POSITIONS':
        for i in range(0,Optimization.nat,1):
           file_vector[line_number + i +1] = str(new_coordinates[i]).replace('[','')
           file_vector[line_number + i +1] = file_vector[line_number + i +1].replace(']','')
           file_vector[line_number + i +1] = file_vector[line_number + i +1].replace("'","")
           file_vector[line_number + i +1] = file_vector[line_number + i +1] +'\n'
   return file_vector
def substitute_cell_parameters(file_vector:List[str], new_cell_parameters: np.ndarray) ->List[str]:          
   for line_number,line in enumerate(file_vector):
       splited_line = line.split();splited_line.append('end')

       if splited_line[0] == 'a':
          file_vector[line_number] = ''
       if splited_line[0] == 'b':
          file_vector[line_number] = ''           
       if splited_line[0] == 'c':
          file_vector[line_number] = ''           
       if splited_line[0] == 'cosab' or splited_line[0] == 'COSAB':
          file_vector[line_number] = ''           
       if splited_line[0] == 'cosbc'or splited_line[0] == 'COSBC':
          file_vector[line_number] = ''           
       if splited_line[0] == 'cosac' or splited_line[0] == 'COSAC':
          file_vector[line_number] = '' 
       if splited_line[0] == 'ibrav':
          file_vector[line_number] = ''       
       if splited_line[0] == 'CELL_PARAMETERS':
          for i in range(0,3,1):
              file_vector[line_number + i +1] = '' 
       elif splited_line[0] == '&SYSTEM':
            file_vector[line_number] = '&SYSTEM\n ibrav = 0\n'

       if splited_line[0] == 'ATOMIC_POSITIONS':
          if Output.cell_parameters_units == 'angstrom': 
             file_vector[line_number] = 'CELL_PARAMETERS (angstrom)\n' + \
             str(new_cell_parameters[0]).replace(']','').replace('[','') + '\n' + \
             str(new_cell_parameters[1]).replace(']','').replace('[','') + '\n' + \
             str(new_cell_parameters[2]).replace(']','').replace('[','') + '\n' + \
             file_vector[line_number]
          elif Output.cell_parameters_units == 'alat':
             file_vector[line_number] = 'CELL_PARAMETERS (angstrom)\n' + \
             str(Optimization.a*new_cell_parameters[0]).replace(']','').replace('[','') + '\n' + \
             str(Optimization.a*new_cell_parameters[1]).replace(']','').replace('[','') + '\n' + \
             str(Optimization.a*new_cell_parameters[2]).replace(']','').replace('[','') + '\n' + \
             file_vector[line_number]
   return file_vector
def generate_input(opt_input_dir_and_name:str,new_file_name:str):
   input_file = open(opt_input_dir_and_name,'r')
   file_vector = input_file.readlines()  
   updated_file_vector = substitute_coordinates(file_vector,Output.atomic_matrix)
   if Optimization.calculation_type == 'vc-relax': 
      updated_file_vector = substitute_cell_parameters(updated_file_vector,Output.cell_matrix)
      if Optimization.cell_dofree == 'ibrav': 
           print('WARNING: vc-relax with cell_dofree = ibrav, move the new input' + 
           ' from ibrav 0 to ibrav != 0') 

   if Output.calculation_finished != 1:
      generated_file = open(opt_out_dir + new_file_name,'w') 
   elif Output.calculation_finished == 1:
      generated_file_name_and_dir = opt_out_dir + opt_input_name.replace('vcrelax','scf')
      generated_file_name_and_dir = generated_file_name_and_dir.replace('relax','scf')
      generated_file = open(generated_file_name_and_dir,'w')     
      file_clean_copy = clean_uncommented_file(updated_file_vector)
      # loop checks the clean copy and edits the original vector
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
             i = 0
             # while checks in the original vector instead of the copy,
             # I think this cannot be harmful
             while updated_file_vector[line_number + i] != 'ATOMIC_SPECIES\n':
                   updated_file_vector[line_number + i] = ''
                   i = i + 1 
   for line in updated_file_vector:
       generated_file.write(line)
   generated_file.close()

   #x_file_name = generated_file_name_and_dir.replace('scf','x.scf')
   #y_file_name = generated_file_name_and_dir.replace('scf','y.scf')
   #z_file_name = generated_file_name_and_dir.replace('scf','z.scf')
   #run(['cp',generated_file_name_and_dir ,x_file_name])
   #x_file = open(opt_out_dir + new_file_name,'w')
   #run(['cp',generated_file_name_and_dir ,y_file_name])
   #y_file = open(opt_out_dir + new_file_name,'w')
   #run(['cp',generated_file_name_and_dir ,z_file_name])
   #z_file = open(opt_out_dir + new_file_name,'w')
   #for line_number,line in enumerate(file_clean_copy):
   #    splited_line = line.split();splited_line.append('end')
   #    if splited_line == 'nspin':
   #       updated_file_vector[line_number] = 'lspinorb=.true.\n' + \
   #       'noncolin=.true.\n' + ... set angles accordint to starting? pseudopotential
   #names? set U?

if __name__ == '__main__':
  opt_input_dir_and_name, opt_out_dir_and_name, new_file_name = parser()
  opt_out_name, opt_out_dir = manage_input_dir(opt_out_dir_and_name)
  opt_input_name, opt_input_dir = manage_input_dir(opt_input_dir_and_name)
  Optimization = QECalculation()
  Optimization.extract_input_information(opt_input_dir_and_name)
  Output = QEoutput()
  Output.extract_output_information(opt_out_dir_and_name)
  generate_input(opt_input_dir_and_name,new_file_name)