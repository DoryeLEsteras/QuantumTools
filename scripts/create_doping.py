#!/usr/bin/python3
from QuantumTools.vasp_tools import Incar
from QuantumTools.qe_tools import QECalculation
from argparse import ArgumentParser
import os
import numpy as np
import re
import shutil

# TO DO LIST
"""
Esta para VASP solo
Los runs se copian en vez de generarse
"""

def parser():
    parser = ArgumentParser(description="Script to create electron/hole doping scan in QuantumEspresso or VASP")
    parser.add_argument("-input", "--input",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the INCAR or scf input file
                        """)
    parser.add_argument("-outdir", "--outdir",
                        type=str,
                        required=False,
                        default='.',
                        help="Output directory ") 
    parser.add_argument("-min", "--min",
                        type=float,
                        required=True,
                        help="Minimum value for doping scan")
    parser.add_argument("-max", "--max",
                        type=float,
                        required=True,
                        help="Maximum value for doping scan")
    parser.add_argument("-step", "--step",
                        type=float,
                        required=True,
                        help="Step value for doping scan")
    parser.add_argument("-run", "--run",
                        type=str,
                        required=False,
                        help="Run file to be copied")
    args = parser.parse_args()
    return args.input,args.outdir,args.min,args.max,args.step,args.run


if __name__ == '__main__':
   input_name_and_dir, outdir, min, max, step, run = parser()
   
   # Decide between QE or VASP
   if os.path.basename(input_name_and_dir) == 'INCAR':
      incar = Incar()
      incar.read_data(input_name_and_dir)
      if incar.nelect == 0.0:
         #incar.incar_file.append('NELECT = 0.0')
         #pattern = f"NELECT\s*=\s*0.0\d+"
         #zero_doping_value = 0.0
         print('NELECT not set in the INCAR')
         exit()
      else:
         pattern = f"NELECT\s*=\s*{incar.nelect}\d*"
         zero_doping_value = incar.nelect
      for dop in np.arange(min,max ,step):
          if round(dop - zero_doping_value,3) > 0.0:
             folder_name = f'doping_{abs(dop - zero_doping_value)/10:.3f}e'
          elif round(dop - zero_doping_value,3) < 0.0:
             folder_name = f'doping_{abs(dop - zero_doping_value)/10:.3f}h'
          elif round(dop -zero_doping_value,3) == 0.000:
             folder_name = f'doping_{abs(dop - zero_doping_value)/10:.3f}'
          if not os.path.exists(os.path.join(outdir,folder_name)):
             os.makedirs(os.path.join(outdir,folder_name))
             shutil.copy(input_name_and_dir.replace('INCAR','POSCAR'), os.path.join(outdir,folder_name,'POSCAR') )
             shutil.copy(input_name_and_dir.replace('INCAR','KPOINTS'), os.path.join(outdir,folder_name,'KPOINTS') )
             shutil.copy(input_name_and_dir.replace('INCAR','POTCAR'), os.path.join(outdir,folder_name,'POTCAR') )
             shutil.copy(run, os.path.join(outdir,folder_name, os.path.basename(run)) )
          else:
             print(f"Folder '{os.path.join(outdir,folder_name)}' already exists.")
          
          new_file = []
          for line_number, line in enumerate(incar.incar_file):
              new_file.append(re.sub(pattern, 'NELECT = ' + str(round(dop,3)) , incar.incar_file[line_number]))
              
          with open(os.path.join(outdir,folder_name, 'INCAR'),'w') as output_file:
               for line in new_file:
                   output_file.write(line)
             
   else:
      # This part will be done one day in the future
      print('QE calculation')