#!/usr/bin/python3
from argparse import ArgumentParser

from QuantumTools.library import initialize_clusters, manage_input_dir


def parser():
    parser = ArgumentParser(description="Script to generate run.sh files")
    parser.add_argument("-input", "--input",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the scf input file
                        """)
    parser.add_argument("-calculation", "--calculation",
                        type=str,
                        required=True,
                        help="""Calculation type for the run, options available:\n
                                -basic_scf \n
                                -spin_bands \n 
                                -nospin_bands \n 
                                -projected \n 
                                -pp \n 
                                -spin_wannier \n 
                                -nospin_wannier \n
                                -force_theorem  \n 
                             """)
    args = parser.parse_args()
    return args.input,args.calculation

if __name__ == '__main__':
   file_dir_and_name,calculation_method = parser()
   file_name, file_dir = manage_input_dir(file_dir_and_name)
   cluster_dict = initialize_clusters(calculation_method,file_dir,file_name,'')
