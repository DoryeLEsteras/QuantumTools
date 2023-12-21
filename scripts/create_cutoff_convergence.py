#!/usr/bin/python3
import os
import sys
from argparse import ArgumentParser
from typing import List
import numpy as np
from QuantumTools.directory_and_files_tools import manage_input_dir,substitute_pattern
from QuantumTools.cluster_tools import initialize_clusters, Cluster
from QuantumTools.qe_tools import QECalculation
import QuantumTools
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
                        default='',
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
            file_to_print = readed_file.replace(Scf.prefix,Scf.prefix + '_wfc_' + str(wfc) + '_rho_' + str(rho))
            with open(os.path.join(outdir,new_file_name),'w') as new_file:
                 new_file.write(file_to_print)    
            if wfc != 0 and rho != 0:
                 initialize_clusters('basic_scf',outdir,new_file_name,'.wfc.' + str(wfc) + '.rho.' + str(rho))   
            elif wfc != 0 and rho == 0:
                 initialize_clusters('basic_scf',outdir,new_file_name,'.wfc.' + str(wfc))
            elif wfc == 0 and rho != 0:
                 initialize_clusters('basic_scf',outdir,new_file_name,'.rho.' + str(rho)) 

def create_launcher(): 
    QT_directory = QuantumTools.__file__.replace('__init__.py','')
    with open(QT_directory + 'Cluster.config','r') as f:
         cluster_name_list = f.read().replace('.cluster','').split()
    cluster_dict = dict.fromkeys(cluster_name_list)
    initialize_clusters('massive',outdir,'','')  
    for cluster_name in cluster_name_list:
        cluster_dict[cluster_name] = Cluster(cluster_name)
        cluster_dict[cluster_name].extract_input_information() 

        launcher_file = open(cluster_name.lower() + '.serial.launcher.sh','a')
        if wfcmin != 0 and  wfcmax != 0 and rhomin != 0 and rhomax !=0:
           launcher_file.write('for rho in $(seq ' + str(rhomin) + ' ' + str(rhostep) + ' ' + str(rhomax) + ')\n' )
           launcher_file.write('do\n')
           launcher_file.write('for wfc in $(seq ' + str(wfcmin) + ' ' + str(wfcstep) + ' ' + str(wfcmax) + ')\n' )
           launcher_file.write('do\n')
           launcher_file.write('srun ' + cluster_dict[cluster_name].qepath + 'pw.x -i ' + file_name.replace('.scf','.wfc.$wfc.rho.$rho.scf')  + ' > ' + file_name.replace('.scf.in','.wfc.$wfc.rho.$rho.scf.out')  + '\n') 
           launcher_file.write('done\n')
           launcher_file.write('done\n')
        if wfcmin == 0 and wfcmax == 0 and rhomin != 0 and rhomax != 0:
           launcher_file.write('for rho in $(seq ' + str(rhomin) + ' ' + str(rhostep) + ' ' + str(rhomax) + ')\n' )
           launcher_file.write('do\n')
           launcher_file.write('srun ' + cluster_dict[cluster_name].qepath + 'pw.x -i ' + file_name.replace('.scf','.rho.$rho.scf')  + ' > ' + file_name.replace('.scf.in','.rho.$rho.scf.out')  + '\n') 
           launcher_file.write('done\n')
        if wfcmin != 0 and wfcmax != 0 and rhomin == 0 and rhomax == 0:
           launcher_file.write('for wfc in $(seq ' + str(wfcmin) + ' ' + str(wfcstep) + ' ' + str(wfcmax) + ')\n' )
           launcher_file.write('do\n')
           launcher_file.write('srun ' + cluster_dict[cluster_name].qepath + 'pw.x -i ' + file_name.replace('.scf','.wfc.$wfc.scf')  + ' > ' + file_name.replace('.scf.in','.wfc.$wfc.scf.out')  + '\n') 
           launcher_file.write('done\n')
    
    for cluster_name in cluster_name_list:
        with open(os.path.join(outdir,cluster_name.lower() +'.parallel.launcher.sh') ,'w') as file:
             if wfcmin != 0 and  wfcmax != 0 and rhomin != 0 and rhomax !=0:
                file.write('for rho in $(seq ' + str(rhomin) + ' ' + str(rhostep) + ' ' + str(rhomax) + ')\n' )
                file.write('do\n')
                file.write('for wfc in $(seq ' + str(wfcmin) + ' ' + str(wfcstep) + ' ' + str(wfcmax) + ')\n' )
                file.write('do\n')
                file.write('sbatch ' + cluster_name.lower() + '.run_for_basic_scf.wfc.$wfc.rho.$rho.sh\n')
                file.write('done\n')
                file.write('done\n')
             if wfcmin == 0 and  wfcmax == 0 and rhomin != 0 and rhomax !=0:
                file.write('for rho in $(seq ' + str(rhomin) + ' ' + str(rhostep) + ' ' + str(rhomax) + ')\n' )
                file.write('do\n')
                file.write('sbatch ' + cluster_name.lower() + '.run_for_basic_scf.rho.$rho.sh\n')
                file.write('done\n')
             if wfcmin != 0 and  wfcmax != 0 and rhomin == 0 and rhomax ==0:
                file.write('for wfc in $(seq ' + str(wfcmin) + ' ' + str(wfcstep) + ' ' + str(wfcmax) + ')\n' )
                file.write('do\n')
                file.write('sbatch ' + cluster_name.lower() + '.run_for_basic_scf.wfc.$wfc.sh\n')
                file.write('done\n')

if __name__ == '__main__':    
   file_dir_and_name,outdir,wfcmin,wfcmax,wfcstep,rhomin,rhomax,rhostep = parser()
   file_name,file_dir =manage_input_dir(file_dir_and_name)
   if outdir == '':
      outdir = file_dir
   if wfcmin == 0 and wfcmax == 0 and rhomax == 0 and rhomin == 0:
      print('!!!NO CUTOFF RANGE PROVIDED!!! --> ABORT')
      sys.exit()
   file_name,file_dir = manage_input_dir(file_dir_and_name)
   Scf = QECalculation()
   Scf.extract_input_information(file_dir_and_name)
   cluster_name_list = create_total_scan()
   create_launcher()
