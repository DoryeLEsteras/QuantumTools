import re
from QuantumTools.library import substitute_pattern,manage_input_dir, initialize_clusters, QECalculation
import numpy as np
import os
from typing import List
from argparse import ArgumentParser

# requires an input that already includes a particular value of Hubbard U

def parser():
    parser = ArgumentParser(description="Script to create inputs for Hubbard U scanning")
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
                        type=float,
                        required=True,
                        help="Top limit for Hubbard U scanning")
    parser.add_argument("-min", "--min",
                        type=float,
                        required=True,
                        help="Starting value for Hubbard U scanning")
    parser.add_argument("-step", "--step",
                        type=float,
                        required=True,
                        help=" Step for Hubbard U scanning")
    parser.add_argument("-version", "--version",
                        type=str,
                        required=False,
                        default='old',
                        help="version of QE:\n version < 7.0 -> old\n version >= 7.0 -> new ")
    args = parser.parse_args()
    return args.input,args.outdir,args.min,args.max,args.step,args.version

def create_scan():
    Scf = QECalculation()
    Scf.extract_input_information(file_dir_and_name)
    with open(file_dir_and_name,'r') as file:
        readed_file = file.read()
    for U in np.arange(Umin,Umax + Ustep,Ustep):
        if version == 'old':
            new_text = substitute_pattern(readed_file,'hubbard_under_v7', U)
        elif version == 'new':  # version 7.0 or more
            new_text = substitute_pattern(readed_file,'hubbard_over_v7', U)    
        new_text = new_text.replace(Scf.prefix,Scf.prefix + '_' +str(U))
        new_file_name = file_name.replace('.scf','.U.' + str(U) + '.scf')
        new_file_name = new_file_name.replace('.relax','.U.' + str(U) + '.relax')
        new_file_name = new_file_name.replace('.vcrelax','.U.' + str(U) + '.vcrelax')
        with open(os.path.join(outdir,new_file_name),'w') as new_file:
            new_file.write(new_text)
        cluster_name_list = initialize_clusters('basic_scf',outdir,new_file_name,'.U.' + str(U))  
    return cluster_name_list
def create_launcher(cluster_name_list:List):
    for cluster_name in cluster_name_list:
        with open(os.path.join(outdir,cluster_name.lower() +'.launcher_for_u_scan.sh') ,'w') as file:
             file.write('for U in $(seq ' + str(Umin) + ' ' + str(Ustep) + ' ' + str(Umax) + ')\n' )
             file.write('do\n')
             file.write('sbatch ' + cluster_name.lower() + '.run_for_basic_scf.U.$U.sh\n')
             file.write('done\n')

if __name__ == '__main__':
    file_dir_and_name,outdir,Umin,Umax,Ustep,version = parser()
    file_name,file_dir = manage_input_dir(file_dir_and_name)
    cluster_name_list = create_scan()
    create_launcher(cluster_name_list)
