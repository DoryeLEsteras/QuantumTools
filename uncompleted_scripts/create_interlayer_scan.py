from QuantumTools.vasp_tools import Poscar
from QuantumTools.qe_tools import QECalculation
from argparse import ArgumentParser
import os
import numpy as np
import shutil


"""
To Do -> change lattice parameter for other cases more than CrSBr
"""

def parser():
    parser = ArgumentParser(description="Script to create interlayer separation scan in QuantumEspresso or VASP")
    parser.add_argument("-input", "--input",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the POSCAR or scf input file
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
    parser.add_argument("-cutoff", "--cutoff",
                        type=float,
                        required=True,
                        help="A safe value in the middle of the interlayer. Just atoms below this value remain unshifted")
    args = parser.parse_args()
    return args.input,args.outdir,args.min,args.max,args.step,args.run,args.cutoff


if __name__ == '__main__':
   input_name_and_dir, outdir, min, max, step, run, cutoff = parser()
   
   # Decide between QE or VASP
   if os.path.basename(input_name_and_dir) == 'POSCAR':
      poscar = Poscar()
      poscar.read_data(input_name_and_dir)

      # Finds the atoms to shift
      atoms_to_be_shifted = []
      for atom_number, atom in enumerate(poscar.atomic_coordinates):
          if poscar.atomic_coordinates[atom_number,2] > cutoff:
             atoms_to_be_shifted.append(atom_number)
      
      # creates the shift in the coordinates
      new_coordinates =  np.copy(poscar.atomic_coordinates)
      for d in np.arange(min,max + step,step):
          for atom_index in atoms_to_be_shifted:
              new_coordinates[atom_index,2] = poscar.atomic_coordinates[atom_index,2] + d

      """careful just valid for CrSBr"""  
      # creates the shift in the cell parameters
      new_cell_parameters =  np.copy(poscar.cell_parameters)
      for d in np.arange(min,max + step,step):
          new_cell_parameters[2,2] = poscar.cell_parameters[2,2] + d

          # copys all the extra files and defines the name of the folder
          folder_name = 'interlayer_' + str(d)
          if not os.path.exists(os.path.join(outdir,folder_name)):
             os.makedirs(os.path.join(outdir,folder_name))
             shutil.copy(input_name_and_dir.replace('POSCAR','INCAR'), os.path.join(outdir,folder_name,'INCAR') )
             shutil.copy(input_name_and_dir.replace('POSCAR','KPOINTS'), os.path.join(outdir,folder_name,'KPOINTS') )
             shutil.copy(input_name_and_dir.replace('POSCAR','POTCAR'), os.path.join(outdir,folder_name,'POTCAR') )
             shutil.copy(run, os.path.join(outdir,folder_name, os.path.basename(run)) )
          else:
             print(f"Folder '{os.path.join(outdir,folder_name)}' already exists.")
      
         
         
          # Finds the line where the coordinates start
          for line_number, line in enumerate(poscar.poscar_file):
              if line.split() == ['Cartesian'] or line.split() == ['Direct']:
                 starting_line = line_number
          # Substitutes the coordinates
          new_file =  np.copy(poscar.poscar_file)
          for atom in range(poscar.nat):
              new_file[atom + starting_line + 1] = f"{new_coordinates[atom,0]:.8f} {new_coordinates[atom,1]:.8f} {new_coordinates[atom,2]:.8f}\n"

          # Substitutes the cell parameters
              new_file[starting_line -5] = f"{new_cell_parameters[0,0]:.8f} {new_cell_parameters[0,1]:.8f} {new_cell_parameters[0,2]:.8f}\n"
              new_file[starting_line -4] = f"{new_cell_parameters[1,0]:.8f} {new_cell_parameters[1,1]:.8f} {new_cell_parameters[1,2]:.8f}\n"
              new_file[starting_line -3] = f"{new_cell_parameters[2,0]:.8f} {new_cell_parameters[2,1]:.8f} {new_cell_parameters[2,2]:.8f}\n"
          # Write them in the new file
          with open(os.path.join(outdir,folder_name, 'POSCAR'),'w') as output_file:
               for line in new_file:
                   output_file.write(line)
       
   else:
      # This part will be done one day in the future
      print('QE calculation')