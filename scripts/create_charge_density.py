#!/usr/bin/python3
import os
from argparse import ArgumentParser

from QuantumTools.library import (QECalculation, initialize_clusters,
                                  manage_input_dir)

def parser():
    parser = ArgumentParser(description="Script to create inputs for charge density calculations")
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
                        help="Relative or absolute path for output directory ")   
    args = parser.parse_args()
    return args.input,args.outdir
def create_charge_density_input(scf_input_name:str,charge_density_output_dir:str)-> None: 
    charge_density_file_name = scf_input_name.replace('scf','cd.pp')
    charge_density_file = open(os.path.join(charge_density_output_dir,charge_density_file_name), 'w')
    charge_density_file.write('&inputpp\n')
    charge_density_file.write("prefix = '" +str(Scf.prefix)+ "'\n")
    charge_density_file.write("outdir = '" +str(Scf.outdir)+ "'\n")
    charge_density_file.write("filplot = '" + str(Scf.prefix) + ".pot'\n")
    charge_density_file.write('plot_num=9,\n')
    charge_density_file.write('/\n')
    charge_density_file.write('&plot\n')
    charge_density_file.write('iflag=3,\n')
    charge_density_file.write('output_format=5,\n')
    charge_density_file.write('/')
    charge_density_file.close()
    initialize_clusters('cd',charge_density_output_dir,scf_input_name,'')
    
if __name__ == '__main__':   
  provided_scf_input_file, provided_output_dir = parser() 
  Scf = QECalculation()
  Scf.extract_input_information(provided_scf_input_file)
  file_name,file_dir =manage_input_dir(provided_scf_input_file)
  if provided_output_dir == '':
     provided_output_dir = file_dir
  create_charge_density_input(file_name,provided_output_dir)

