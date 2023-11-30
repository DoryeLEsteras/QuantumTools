#!/usr/bin/python3
import os
from typing import List
from argparse import ArgumentParser
from QuantumTools.qe_tools import QECalculation
from QuantumTools.directory_and_files_tools import manage_input_dir

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
                        default='./',
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
        if line.startswith('K_POINTS') or line.startswith('k_points'):
           line_to_be_modified = line_number + 1
    return line_to_be_modified, readed_vector

def create_scan(line_to_be_modified:int, readed_vector:List) -> None:
    Scf = QECalculation()
    Scf.extract_input_information(file_dir_and_name)
    original_kp = Scf.kpoints
    if str(original_kp[2]) == '1':
        for i in range(kpmin,kpmax + kpstep,kpstep):
            new_file_name = file_name.replace('scf.in', 'kx' + str(i) + '.ky'  + str(i) + '.kz' + '1' + '.scf.in')  
            readed_vector[line_to_be_modified] = str(i) + " " + str(i) + " " + '1 ' + str(Scf.kpoints[3]) +\
                 " " +  str(Scf.kpoints[4]) + " " + str(Scf.kpoints[5])
            with open(os.path.join(file_dir,new_file_name),'w') as file:
                for line in readed_vector:
                    file.write(line) 
    if str(original_kp[2]) != '1':
        for i in range(kpmin,kpmax + kpstep,kpstep): 
            new_file_name = file_name.replace('scf.in', 'kx' + str(i) + '.ky'  + str(i) + '.kz' + str(i) + '.scf.in')  
            readed_vector[line_to_be_modified] = str(i) + " " + str(i) + " " + str(i) + " "  + str(Scf.kpoints[3]) +\
                   " " +  str(Scf.kpoints[4]) + " " + str(Scf.kpoints[5])
            with open(os.path.join(file_dir,new_file_name),'w') as file:
                for line in readed_vector:
                    file.write(line) 


if __name__ == '__main__':
    file_dir_and_name,outdir,kpmin,kpmax,kpstep = parser()
    file_name,file_dir = manage_input_dir(file_dir_and_name)
    line_to_be_modified,readed_vector = extract_info()
    create_scan(line_to_be_modified,readed_vector)
