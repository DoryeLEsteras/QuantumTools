import numpy as np
from argparse import ArgumentParser

# TO DO LIST
"""
-import run
"""
def parser():
    parser = ArgumentParser(description="Script to create inputs for spin density calculations")
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

def create_spin_density_input(scf_input_name,scf_input_file,spin_density_output_dir): 
    spin_density_output_long_name = scf_input_name.replace('scf','sd.pp')
    spin_density_output_long_name = spin_density_output_long_name.split('/')
    spin_density_output_name = spin_density_output_long_name[-1]
    spin_density_output = str(spin_density_output_dir) + str(spin_density_output_name)
    spin_density_file = open(spin_density_output , 'w')
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
    filband = filband.replace(",", "") 
    filband = filband.replace("\n", "")
    filband = filband.replace(" ", "") 
    spin_density_file.write('&inputPP\n')
    spin_density_file.write(prefix)
    spin_density_file.write(outdir)
    spin_density_file.write('filband = \'' + str(filband) + '.chgxsf\'\n')
    spin_density_file.write('plot_num=6,\n')
    spin_density_file.write('/\n')
    spin_density_file.write('&plot\n')
    spin_density_file.write('nfile = 1,\n')
    spin_density_file.write('iflag=3,\n')
    spin_density_file.write('output_format=5,\n')
    spin_density_file.write('fileout = \'' + str(filband) + '.xsf\'\n')
    spin_density_file.write('/')
    spin_density_file.close()
provided_scf_input_file, provided_output_dir = parser()
scf_file = open(str(provided_scf_input_file), 'r')
create_spin_density_input(provided_scf_input_file,scf_file,provided_output_dir)
scf_file.close()


