import numpy as np
from argparse import ArgumentParser
from QuantumTools.directory_and_files_tools import manage_input_dir
from QuantumTools.cluster_tools import initialize_clusters
from QuantumTools.qe_tools import QECalculation
from QuantumTools.wannier90_tools import WannierCalculation

def parser():
    parser = ArgumentParser(description="Script to create WT file")
    parser.add_argument("-win", "--win",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the Wannier input file
                        """)
    parser.add_argument("-outdir", "--outdir",
                        type=str,
                        required=False,
                        default='./',
                        help="Relative or absolute path for output directory ")   
    args = parser.parse_args()
    return args.win,args.outdir

def create_wt():
 with open ('wt.in','w') as file:
   file.write("""
&TB_FILE
Hrfile = '""" + hr_file + "'" + """
Package = 'QE'
/
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! CONTROL SECTION !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
&CONTROL
SlabSS_calc  = T
SlabArc_calc = T
/
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!VARIABLES TO SELECT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
PROJECTORS
""")
   for i in range(0,Win.nat,1):
       file.write('9 ')
   file.write('\n')
   for i in range(0,Win.nat,1):
       file.write(str(Win.atomic_matrix[i][0]) + ' dz2 dxz dyz dx2-y2 dxy px py pz s\n') 
   file.write("""
SURFACE
1  0  0
0  1  0

&SYSTEM
NSLAB = 10
NumOccupied = 0
SOC = 0
E_FERMI = 0
/

&PARAMETERS
E_arc = 0.0
Eta_Arc = 0.001     
Nk2 = 101   
Nk1 = 101         
Nk3= 101
NP = 2              
OmegaNum = 1101 
OmegaMin = -7 
OmegaMax = 0.5 
/

KPATH_SLAB
3        
Z  0.5000000000  0.5000000000   Γ  0.0000000000  0.0000000000
Γ  0.0000000000  0.0000000000   X  0.5000000000  0.0000000000
X  0.5000000000  0.0000000000   Z  0.5000000000  0.5000000000

KPLANE_SLAB
  0.0  0.0      
  2.0  0.0      
  0.0  2.0      

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!FIXED FLAGS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

LATTICE
Angstrom
""") 
   file.write(str(Win.cell_matrix_angstrom).replace('[','').replace(']','') + '\n')
   file.write('ATOM_POSITIONS\n')
   file.write(str(Win.nat) + '\n')
   
   if Win.atomic_positions_units == 'crystal':
      file.write('Direct\n')
   elif Win.atomic_positions_units == 'cartesian':
      file.write('Cartesian\n')
   for i in range(0,Win.nat,1):
       file.write(str(Win.atomic_matrix[i]).replace('[','').replace(']','').replace("'","")+'\n') 

if __name__ == '__main__': 
    file_dir_and_name,outdir = parser()
    file_name,file_dir = manage_input_dir(file_dir_and_name)
    hr_file = file_name.replace('.win', '_hr.dat')
    Win = WannierCalculation()
    Win.extract_input_information(file_dir_and_name)
    create_wt()
    initialize_clusters('wt',outdir,'','')