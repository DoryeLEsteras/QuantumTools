import numpy as np
from argparse import ArgumentParser

# TO DO LIST
"""
-import create_run and create runs
-extend the path library
"""

# Extend path library

"""
 if a new path is added there is 2 things to do: 
 -to define the path (below class section)
 -add an option to symmetry manager
"""

class k_path:
    def __init__(self,nk,kpoints):
        self.heading = 'K_POINTS {crystal_b}\n'
        self.nk = nk
        self.kpoints = kpoints
    def write_kpath(self,bands_output_name):
        bands_output_name.write(self.heading)
        bands_output_name.write(self.nk +"\n")  
        bands_output_name.write(self.kpoints) 


hex = k_path('4',
'0     0     0   20 \n' + '0.5   0     0   20 \n' + \
'0.333 0.333 0   20 \n' + '0     0     0   0')
rmc = k_path('6',
    '0     0     0     20 \n' + '1/2   0    -1/2   20 \n' + \
    '1/2   1/2  -1/2   20 \n' + '0     1/2   0     20 \n' + \
    '0     0     0     20 \n' + '1/2   1/2   -1/2   0')
ort = k_path('6',
'0    0   0  20 \n' + '0.5  0   0  20 \n' + '0.5  0.5 0  20 \n' + \
'0    0.5 0  20 \n' + '0    0   0  20 \n' +'0    0   0.5 0')

def sym_manager(selected_sym,bands_file):
    if selected_sym == 'none':
        pass
    if selected_sym == 'hex':
        hex.write_kpath(bands_file)
    if selected_sym == 'rmc':
        rmc.write_kpath(bands_file)
    if selected_sym == 'ort':
        ort.write_kpath(bands_file)

def parser():
    parser = ArgumentParser(description="Script to create band calculation inputs")
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
                        help="output directory ")
    parser.add_argument("-kpath", "--kpath",
                        type=str,
                        required=False,
                        default='none',
                        help="Desired kpath\n actual library:\n hex : hexagonal\n rmc : rectangular monoclinic\n ort : orthorombic ")
    
    args = parser.parse_args()
    return args.input,args.out,args.kpath
def create_bands_input(scf_input_name,scf_input_file,bands_output_dir): 
    bands_output_name = scf_input_name.replace('scf','bands')
    bands_output = str(bands_output_dir) + str(bands_output_name)
    bands_file = open(bands_output , 'w')
    nspin = security_check = '0'
    for line in scf_input_file:
        # removes '=' to isolate the words and reduce all the possibilities like
        # calculation=, 'calculation ='scf', calculation =,  ... 
        line_to_check = line.replace("=", ' ') 
        line_to_check_vector = line_to_check.split()
        # lines with one word are not going to be lists, thus evaluation of
        # line_to_check_vector[0] would crash, append and 'end' pointer at the end
        # of the vector guarantees line_to_check_vector is going to be a list always
        line_to_check_vector.append('end')
        if line_to_check_vector[0] == 'calculation':
           security_check = line_to_check_vector[1]
           line = 'calculation = \'bands\'\n'
        if line_to_check_vector[0] == 'verbosity':
          line = 'verbosity = \'high\'\n'
        if line_to_check_vector[0] == 'k_points' or line_to_check_vector[0] == 'K_POINTS':
          line = ''
          scf_input_file.readline()
        if line_to_check_vector[0] == 'prefix':
          prefix = line
        if line_to_check_vector[0] == 'outdir':
          outdir = line
        if line_to_check_vector[0] == 'nspin': 
            if line_to_check_vector[1] == '2' or line_to_check_vector[1] == '2,':
                nspin = '2'
        bands_file.write(str(line))
    return prefix,outdir,nspin,security_check,bands_file
def create_bs_input(scf_input_name,bs_output_dir,prefix,outdir,nspin):
    # These lines prepare the filband removing strange symbols
    filband = prefix.split("=")
    filband = filband[1]
    filband = filband.replace("'", "") 
    filband = filband.replace("\n", "")
    filband = filband.replace(" ", "") 
    if nspin == '0':
        bs_output_name = scf_input_name.replace('scf','bs')
        bs_file = open(str(bs_output_dir) + str(bs_output_name) , 'w')
        bs_file.write('&BANDS\n')
        bs_file.write(prefix)
        bs_file.write(outdir)
        bs_file.write('filband = \'' + str(filband) + '.bands.dat\'\n')
        bs_file.write('lsym=.true.\n')
        bs_file.write('spin_component=1\n')
        bs_file.write('/')
    if nspin == '2':
        bs1_output_name = scf_input_name.replace('scf','bs1')
        bs2_output_name = scf_input_name.replace('scf','bs2')
        bs1_file = open(str(bs_output_dir) + str(bs1_output_name) , 'w')
        bs2_file = open(str(bs_output_dir) + str(bs2_output_name) , 'w')
        bs1_file.write('&BANDS\n')
        bs1_file.write(prefix)
        bs1_file.write(outdir)
        bs1_file.write('filband = \'' + str(filband) + '.bands1.dat\'\n')
        bs1_file.write('lsym=.true.\n')
        bs1_file.write('spin_component=1\n')
        bs1_file.write('/')
        bs2_file.write('&BANDS\n')
        bs2_file.write(prefix)
        bs2_file.write(outdir)
        bs2_file.write('filband = \'' + str(filband) + '.bands2.dat\'\n')
        bs2_file.write('lsym=.true.\n')
        bs2_file.write('spin_component=2\n')
        bs2_file.write('/')

provided_scf_input_file, provided_output_dir,selected_sym = parser()
scf_file = open(str(provided_scf_input_file), 'r')
# create_bands_input reads the scf, creates bands.in and obtains prefix, outdir,
# for bs files, security check (check provided scf is an scf calculation)
# and the bands file to write the kpath
prefix,outdir,nspin,security_check,bands_file = create_bands_input(provided_scf_input_file,scf_file,provided_output_dir)
create_bs_input(provided_scf_input_file,provided_output_dir,prefix,outdir,nspin)
sym_manager(selected_sym,bands_file)
#create_suggested_run
if security_check != '\'scf\'':
   print('ERROR: provided scf input does not correspond to scf calculation')
