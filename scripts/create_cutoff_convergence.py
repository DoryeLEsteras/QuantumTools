#!/usr/bin/python3
import os
import sys
from argparse import ArgumentParser
from typing import List
import numpy as np
from QuantumTools.directory_and_files_tools import manage_input_dir,substitute_pattern
from QuantumTools.cluster_tools import initialize_clusters
from QuantumTools.qe_tools import QECalculation

def parser():
    parser = ArgumentParser(description="Script to converge the cutoffs")
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
                        help="output directory ")
    parser.add_argument("-wfcmax", "--wfcmax",
                        type=int,
                        required=False,
                        default='0',
                        help="Top limit for ecutwfc scanning")
    parser.add_argument("-wfcmin", "--wfcmin",
                        type=int,
                        required=False,
                        default='0',
                        help="Starting value for ecutwfc scanning")
    parser.add_argument("-wfcstep", "--wfcstep",
                        type=int,
                        required=False,
                        default='10',
                        help=" Step for ecutwfc scanning")
    parser.add_argument("-rhomax", "--rhomax",
                        type=int,
                        required=False,
                        default='0',
                        help="Top limit for ecutrho scanning")
    parser.add_argument("-rhomin", "--rhomin",
                        type=int,
                        required=False,
                        default='0',
                        help="Starting value for ecutrho scanning")
    parser.add_argument("-rhostep", "--rhostep",
                        type=int,
                        required=False,
                        default='10',
                        help=" Step for ecutrho scanning")
    args = parser.parse_args()
    return args.input,args.outdir,args.wfcmin,args.wfcmax,args.wfcstep,args.rhomin,args.rhomax,args.rhostep

def create_total_scan(): 
    Scf = QECalculation()
    Scf.extract_input_information(file_dir_and_name)
    with open(file_dir_and_name,'r') as file:
        readed_file = file.read()
    for wfc in np.arange(wfcmin,wfcmax + wfcstep,wfcstep):
        for rho in np.arange(rhomin,rhomax + rhostep,rhostep):
            new_file_name = file_name
            if wfc != 0:
                readed_file = substitute_pattern(readed_file,'ecutwfc', wfc)
                new_file_name = new_file_name.replace('.scf','.wfc.' + str(wfc) + '.scf')
            if rho != 0:
                readed_file = substitute_pattern(readed_file,'ecutrho', rho)
                new_file_name = new_file_name.replace('.scf','.rho.'+ str(rho) + '.scf')
            readed_file = readed_file.replace(Scf.prefix,Scf.prefix + '_wfc_' + str(wfc) + '_rho_' + str(rho))
            with open(os.path.join(outdir,new_file_name),'w') as new_file:
                 new_file.write(readed_file)    
            if wfc != 0 and rho != 0:
              cluster_name_list = initialize_clusters('basic_scf',outdir,new_file_name,'.wfc.' + str(wfc) + '.rho.' + str(rho))   
            elif wfc != 0 and rho == 0:
              cluster_name_list = initialize_clusters('basic_scf',outdir,new_file_name,'.wfc.' + str(wfc))
            elif wfc == 0 and rho != 0:
              cluster_name_list = initialize_clusters('basic_scf',outdir,new_file_name,'.rho.' + str(rho)) 
    return cluster_name_list

def create_launcher(cluster_name_list:List):
    for cluster_name in cluster_name_list:
        with open(os.path.join(outdir,cluster_name.lower() +'.launcher_for_cutoff_convergence.sh') ,'w') as file:
             file.write('for rho in $(seq ' + str(rhomin) + ' ' + str(rhostep) + ' ' + str(rhomax) + ')\n' )
             file.write('do\n')
             file.write('for wfc in $(seq ' + str(wfcmin) + ' ' + str(wfcstep) + ' ' + str(wfcmax) + ')\n' )
             file.write('do\n')
             file.write('sbatch ' + cluster_name.lower() + '.run_for_basic_scf.wfc.$wfc.rho.$rho.sh\n')
             file.write('done\n')
             file.write('done\n')

if __name__ == '__main__':    
   file_dir_and_name,outdir,wfcmin,wfcmax,wfcstep,rhomin,rhomax,rhostep = parser()
   if wfcmin == 0 and wfcmax == 0 and rhomax == 0 and rhomin == 0:
      print('!!!NO CUTOFF RANGE PROVIDED!!! --> ABORT')
      sys.exit()
   file_name,file_dir = manage_input_dir(file_dir_and_name)
   cluster_name_list = create_total_scan()
   print(cluster_name_list)
   create_launcher(cluster_name_list)
