#!/usr/bin/python3
import os
from argparse import ArgumentParser

from QuantumTools.qe_tools import QECalculation 
from QuantumTools.cluster_tools import initialize_clusters
from QuantumTools.directory_and_files_tools import manage_input_dir

def parser():
    parser = ArgumentParser(description="Script to create inputs for band alignment calculations")
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

def create_pp(scf_input_name:str,output_dir:str)-> None: 
    ba_file_name = scf_input_name.replace('scf','wf.pp')
    ba_file = open(os.path.join(output_dir,ba_file_name), 'w')
    ba_file.write('&inputpp\n')
    ba_file.write("prefix = '" +str(Scf.prefix)+ "'\n")
    ba_file.write("outdir = '" +str(Scf.outdir)+ "'\n")
    ba_file.write("filplot = '" + str(Scf.prefix) + ".pot'\n")
    ba_file.write('plot_num=11,\n')
    ba_file.write('/\n')
    ba_file.write('&plot\n')
    ba_file.write('iflag=3,\n')
    ba_file.write('output_format=6,\n')
    ba_file.write('/')
    ba_file.close()

def create_avg(scf_input_name:str,output_dir:str)-> None: 
    avg_file_name = scf_input_name.replace('scf','avg')
    avg_file = open(os.path.join(output_dir,avg_file_name), 'w')
    avg_file.write('1\n')
    avg_file.write(str(Scf.prefix) + '.pot\n')
    avg_file.write('1.D0\n')
    avg_file.write('1440\n')
    avg_file.write('3\n')
    avg_file.write('15\n')
    avg_file.close()

if __name__ == '__main__':   
  provided_scf_input_file, provided_output_dir = parser() 
  Scf = QECalculation()
  Scf.extract_input_information(provided_scf_input_file)
  file_name,file_dir =manage_input_dir(provided_scf_input_file)
  if provided_output_dir == '':
     provided_output_dir = file_dir
  create_pp(file_name,provided_output_dir)
  create_avg(file_name,provided_output_dir)
  initialize_clusters('band_alignment',provided_output_dir, provided_scf_input_file,'')
