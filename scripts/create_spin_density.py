#!/usr/bin/python3
from argparse import ArgumentParser

from QuantumTools.library import (QECalculation, initialize_clusters,
                                  manage_input_dir)


def parser():
    parser = ArgumentParser(description="Script to create inputs for spin density calculations")
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
                        help="Relative or absolute path for output directory ")   
    args = parser.parse_args()
    return args.input,args.outdir
def create_spin_density_input(scf_input_name:str,spin_density_output_dir:str)-> None: 
    spin_density_name = scf_input_name.replace('scf','sd.pp')
    spin_density_file = open(spin_density_output_dir + '/' + spin_density_name , 'w')
    spin_density_file.write('&inputpp\n')
    spin_density_file.write("prefix = '" +str(Scf.prefix)+ "'\n")
    spin_density_file.write("outdir = '" +str(Scf.outdir)+ "'\n")
    spin_density_file.write("filplot = '" +str(Scf.prefix)+ ".chgxsf'\n")
    spin_density_file.write('plot_num=6,\n')
    spin_density_file.write('/\n')
    spin_density_file.write('&plot\n')
    spin_density_file.write('nfile = 1,\n')
    spin_density_file.write('iflag=3,\n')
    spin_density_file.write('output_format=5,\n')
    spin_density_file.write("fileout = '" + str(Scf.prefix) + ".xsf'\n")
    spin_density_file.write('/')
    spin_density_file.close()
    initialize_clusters('sd',spin_density_output_dir,scf_input_name,'')

if __name__ == '__main__':   
  provided_scf_input_file, provided_output_dir = parser()
  Scf = QECalculation()
  Scf.extract_input_information(provided_scf_input_file)
  file_name,file_dir =manage_input_dir(provided_scf_input_file)
  create_spin_density_input(file_name,provided_output_dir)



