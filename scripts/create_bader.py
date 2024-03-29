#!/usr/bin/python3
import os
from argparse import ArgumentParser
from QuantumTools.qe_tools import QECalculation
from QuantumTools.cluster_tools import initialize_clusters
from QuantumTools.directory_and_files_tools import manage_input_dir

def parser():
    parser = ArgumentParser(description="Script to create inputs for bader calculations")
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

def create_bader_all_input(scf_input_name:str,bader_output_dir:str)-> None: 
    bader_file_name = scf_input_name.replace('scf','all.pp')
    bader_file = open(os.path.join(bader_output_dir,bader_file_name), 'w')
    bader_file.write('&inputpp\n')
    bader_file.write("prefix = '" +str(Scf.prefix)+ "'\n")
    bader_file.write("outdir = '" +str(Scf.outdir)+ "'\n")
    bader_file.write("filplot = '" + str(Scf.prefix) + "_allelec'\n")
    bader_file.write('plot_num=21,\n')
    bader_file.write('/\n')
    bader_file.write('&plot\n')
    bader_file.write('nfile = 1\n')
    bader_file.write('iflag=3,\n')
    bader_file.write('output_format=6,\n')
    bader_file.write("fileout = '" + bader_file_name.replace('pp.in','cube') + ',\n')
    bader_file.write('/')
    bader_file.close()

def create_bader_valence_input(scf_input_name:str,bader_output_dir:str)-> None: 
    bader_file_name = scf_input_name.replace('scf','valence.pp')
    bader_file = open(os.path.join(bader_output_dir,bader_file_name), 'w')
    bader_file.write('&inputpp\n')
    bader_file.write("prefix = '" +str(Scf.prefix)+ "'\n")
    bader_file.write("outdir = '" +str(Scf.outdir)+ "'\n")
    bader_file.write("filplot = '" + str(Scf.prefix) + "_valence'\n")
    bader_file.write('plot_num=0,\n')
    bader_file.write('/\n')
    bader_file.write('&plot\n')
    bader_file.write('nfile = 1\n')
    bader_file.write('iflag=3,\n')
    bader_file.write('output_format=6,\n')
    bader_file.write("fileout = '" + bader_file_name.replace('pp.in','cube') + ',\n')
    bader_file.write('/')
    bader_file.close()

if __name__ == '__main__':   
  provided_scf_input_file, provided_output_dir = parser() 
  Scf = QECalculation()
  Scf.extract_input_information(provided_scf_input_file)
  file_name,file_dir =manage_input_dir(provided_scf_input_file)
  if provided_output_dir == '':
     provided_output_dir = file_dir 
  create_bader_all_input(file_name,provided_output_dir)
  create_bader_valence_input(file_name,provided_output_dir)
  initialize_clusters('bader',provided_output_dir, provided_scf_input_file,'')
