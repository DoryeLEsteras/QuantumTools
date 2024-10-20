#!/usr/bin/python3
import os
from argparse import ArgumentParser
from typing import List

import QuantumTools
from QuantumTools.cluster_tools import Cluster, initialize_clusters
from QuantumTools.directory_and_files_tools import manage_input_dir
from QuantumTools.qe_tools import QECalculation


def parser():
    parser = ArgumentParser(description="Script to converge the kpoints")
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
    parser.add_argument("-max", "--max",
                        type=int,
                        required=True,
                        help="Top limit for kpoint scanning")
    parser.add_argument("-min", "--min",
                        type=int,
                        required=True,
                        help="Starting value for kpoint scanning")
    parser.add_argument("-step", "--step",
                        type=int,
                        required=False,
                        default='1',
                        help=" Step for kpoint scanning")
    args = parser.parse_args()
    return args.input,args.outdir,args.min,args.max,args.step

def extract_info():
    with open(file_dir_and_name,'r') as file:
         readed_vector = file.readlines() 
    for line_number, line in enumerate(readed_vector):
        line_to_check = line.replace('(','').replace('{','').split()
        if len(line_to_check)>1:
           if line_to_check[0].lower() == 'k_points':
              line_to_be_modified = line_number + 1
           if line_to_check[0].lower() == 'prefix':
              prefix_line_number = line_number
    return line_to_be_modified,prefix_line_number, readed_vector

def create_scan(line_to_be_modified:int, prefix_line_number:int,readed_vector:List) -> None:
    original_kp = Scf.kpoints
    if str(Scf.kpoints[2]) == '1':
        for i in range(kpmin,kpmax + kpstep,kpstep):
            new_file_name = file_name.replace('scf.in', 'kx' + str(i) + '.ky'  + str(i) + '.kz' + '1' + '.scf.in')  
            readed_vector[line_to_be_modified] = str(i) + " " + str(i) + " " + '1 ' + str(Scf.kpoints[3]) +\
                 " " +  str(Scf.kpoints[4]) + " " + str(Scf.kpoints[5])
            readed_vector[prefix_line_number] = "prefix = '" + Scf.prefix + '_k_' + str(i) +"'\n"
            initialize_clusters('basic_scf',outdir,new_file_name,'.kx' + str(i) + '.ky' + str(i) +'.kz1') 
            with open(os.path.join(outdir,new_file_name),'w') as file:
                for line in readed_vector:
                    file.write(line) 
    if str(Scf.kpoints[2]) != '1':
        for i in range(kpmin,kpmax + kpstep,kpstep): 
            new_file_name = file_name.replace('scf.in', 'kx' + str(i) + '.ky'  + str(i) + '.kz' + str(i) + '.scf.in')  
            readed_vector[line_to_be_modified] = str(i) + " " + str(i) + " " + str(i) + " "  + str(Scf.kpoints[3]) +\
                   " " +  str(Scf.kpoints[4]) + " " + str(Scf.kpoints[5])
            initialize_clusters('basic_scf',outdir,new_file_name,'.kx' + str(i) + '.ky' + str(i) + '.kz' + str(i)) 
            with open(os.path.join(outdir,new_file_name),'w') as file:
                for line in readed_vector:
                    file.write(line)

def create_launcher(): 
    QT_directory = QuantumTools.__file__.replace('__init__.py','')
    with open(QT_directory + 'Cluster.config','r') as f:
         cluster_name_list = f.read().replace('.cluster','').split()
    cluster_name_list.append('local')
    cluster_dict = dict.fromkeys(cluster_name_list)
    initialize_clusters('massive',outdir,'','') 
    for cluster_name in cluster_name_list:
        cluster_dict[cluster_name] = Cluster(cluster_name)
        if cluster_name != 'local':
           cluster_dict[cluster_name].extract_input_information() 
           cluster_dict[cluster_name].launch_command = 'srun ' 

        launcher_file = open(os.path.join(outdir,cluster_name.lower() + '.serial.launcher.sh'),'a')
        launcher_file.write('for kp in $(seq ' + str(kpmin) + ' ' + str(kpstep) + ' ' + str(kpmax) + ')\n' )
        launcher_file.write('do\n')
        if str(Scf.kpoints[2]) == '1':
           launcher_file.write(cluster_dict[cluster_name].launch_command + cluster_dict[cluster_name].qepath + 'pw.x -i ' + file_name.replace('scf.in','kx$kp.ky$kp.kz1.scf.in')  + ' > ' + file_name.replace('.scf.in','kx$kp.ky$kp.kz1.scf.out')  + '\n')  
        if str(Scf.kpoints[2]) != '1':
           launcher_file.write(cluster_dict[cluster_name].launch_command + cluster_dict[cluster_name].qepath + 'pw.x -i ' + file_name.replace('scf.in','kx$kp.ky$kp.kz$kp.scf.in')  + ' > ' + file_name.replace('.scf.in','kx$kp.ky$kp.kz$kp.scf.out')  + '\n')  
        launcher_file.write('done\n')
        launcher_file.close()

    for cluster_name in cluster_name_list:
        if cluster_name != 'local':
           with open(os.path.join(outdir,cluster_name.lower() +'.parallel.launcher.sh') ,'w') as file:
                file.write('for kp in $(seq ' + str(kpmin) + ' ' + str(kpstep) + ' ' + str(kpmax) + ')\n' )
                file.write('do\n')
                if str(Scf.kpoints[2]) == '1':
                   file.write('sbatch ' + cluster_name.lower() + '.run_for_basic_scf.kx$kp.ky$kp.kz1.sh\n')
                if str(Scf.kpoints[2]) != '1':
                   file.write('sbatch ' + cluster_name.lower() + '.run_for_basic_scf.kx$kp.ky$kp.kz$kp.sh\n')
                file.write('done\n')

if __name__ == '__main__':
    file_dir_and_name,outdir,kpmin,kpmax,kpstep = parser()
    file_name,file_dir = manage_input_dir(file_dir_and_name)
    if outdir == '':
       outdir = file_dir
    Scf = QECalculation()
    Scf.extract_input_information(file_dir_and_name)
    line_to_be_modified,prefix_line_number,readed_vector = extract_info()
    create_scan(line_to_be_modified,prefix_line_number,readed_vector)
    create_launcher()
