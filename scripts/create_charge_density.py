#!/usr/bin/python3.6
import numpy as np
from argparse import ArgumentParser

# TO DO LIST
"""
-import run
"""

def parser():
    parser = ArgumentParser(description="Script to create inputs for charge density calculations")
    parser.add_argument("-input", "--input",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the scf input file
                        """)
    parser.add_argument("-out", "--out",
                        type=str,
                        required=False,
                        default='./',
                        help="Relative or absolute path for output directory ")   
    args = parser.parse_args()
    return args.input,args.out

def create_charge_density_input(scf_input_name,scf_input_file,charge_density_output_dir): 
    charge_density_output_long_name = scf_input_name.replace('scf','cd.pp')
    charge_density_output_long_name = charge_density_output_long_name.split('/')
    charge_density_output_name = charge_density_output_long_name[-1]
    charge_density_output = str(charge_density_output_dir) + str(charge_density_output_name)
    charge_density_file = open(charge_density_output , 'w')
    for line in scf_input_file:
        line_to_check = line.replace("=", ' ') 
        line_to_check = line_to_check.replace(",", ' ') 
        line_to_check_vector = line_to_check.split()
        line_to_check_vector.append('end')
        if line_to_check_vector[0] == 'prefix':
          prefix = line.replace(" ","")
        if line_to_check_vector[0] == 'outdir':
          outdir = line.replace(" ","")
    filband = prefix.split("=")
    filband = filband[1]
    filband = filband.replace("'", "") 
    filband = filband.replace("\n", "")
    filband = filband.replace(" ", "") 
    charge_density_file.write('&inputPP\n')
    charge_density_file.write(prefix)
    charge_density_file.write(outdir)
    charge_density_file.write('filband = \'' + str(filband) + '.pot\'\n')
    charge_density_file.write('plot_num=11,\n')
    charge_density_file.write('/\n')
    charge_density_file.write('&plot\n')
    charge_density_file.write('iflag=3,\n')
    charge_density_file.write('output_format=5,\n')
    charge_density_file.write('/')
    charge_density_file.close()
provided_scf_input_file, provided_output_dir = parser()
scf_file = open(str(provided_scf_input_file), 'r')
create_charge_density_input(provided_scf_input_file,scf_file,provided_output_dir)
scf_file.close()
