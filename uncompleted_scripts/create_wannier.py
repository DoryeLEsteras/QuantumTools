import numpy as np
from argparse import ArgumentParser
# To do list

# extend the path library and correct
#import suggested runs

class k_path:
    def __init__(self,kpoints):
        self.heading = \
        ' !!!!KPATH!!!!\n' + \
        'begin kpoint_path\n'
        self.kpoints = kpoints
        self.ending = \
        '\nend kpoint_path'
    def write_kpath(self,win_output_name):
        win_output_name.write(self.heading) 
        win_output_name.write(self.kpoints)
        win_output_name.write(self.ending)  

"""
G 0      0      0   G 1/2   0    -1/2
G 1/2   0    -1/2   G 1/2   1/2  -1/2
G 1/2   1/2  -1/2   G 0     1/2   0
G 0     1/2   0     G 0     0     0
G 0     0     0     G 1/2   1/2   -1/2


K_POINTS {crystal_b}
6
G 0    0   0 X 0.5  0   0 
X 0.5  0   0 S 0.5  0.5 0
S 0.5  0.5 0 Y 0   0.5 0 
Y 0   0.5 0  G 0    0   0
G 0    0   0 Z 0    0    0.5 
"""

# if a new path is added there is 2 things to do: 
# to define here the path, and add an option to symmetry manager
hex = k_path(\
'G 0      0      0   K 0.5   0      0 \n' + \
'K 0.5    0      0   M 0.333 0.333  0\n' + \
'M 0.333  0.333  0   G 0     0      0\n')
rmc = k_path(\
    '0     0     0     20 \n' + '1/2   0    -1/2   20 \n' + \
    '1/2   1/2  -1/2   20 \n' + '0     1/2   0     20 \n' + \
    '0     0     0     20 \n' + '1/2   1/2   -1/2   0')
ort = k_path(\
'0    0   0  20 \n' + '0.5  0   0  20 \n' + '0.5  0.5 0  20 \n' + \
'0    0.5 0  20 \n' + '0    0   0  20 \n' +'0    0   0.5 0')

def sym_manager(selected_sym,win_file):
    if selected_sym == 'none':
        pass
    if selected_sym == 'hex':
        hex.write_kpath(win_file)
    if selected_sym == 'rmc':
        rmc.write_kpath(win_file)
    if selected_sym == 'ort':
        ort.write_kpath(win_file)

def parser():
    parser = ArgumentParser(description="Script to create wannier90 calculation inputs")
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
    parser.add_argument("-k", "--k",
                        type=str,
                        required=True,
                        nargs='+',
                        help="kx ky kz for nscf calculation ")
    parser.add_argument("-nbands", "--nbands",
                        type=str,
                        required=False,
                        default='',
                        help=" number of bands for Wannier90 calculation")
    parser.add_argument("-nwan", "--nwan",
                        type=str,
                        required=False,
                        default='',
                        help=" number of Wannier functions for Wannier90 calculation")
    args = parser.parse_args()
    return args.input,args.out,args.kpath,args.k,args.nbands,args.nwan

def create_nscf_input(scf_input_name,scf_input_file,nscf_output_dir): 
    nscf_output_name = scf_input_name.replace('scf','nscf')
    nscf_output = str(nscf_output_dir) + str(nscf_output_name)
    nscf_file = open(nscf_output , 'w')
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
           line = 'calculation = \'nscf\'\n'
        if line_to_check_vector[0] == 'verbosity':
          line = 'verbosity = \'high\'\n'
        if line_to_check_vector[0] == '&system' or line_to_check_vector[0] == '&SYSTEM':
          line = '&SYSTEM\n' + 'nosym=.true.\n' + 'noinv=.true.\n' + 'nbnd = ' + str(nbands) + ' \n'
        if line_to_check_vector[0] == '&electrons' or line_to_check_vector[0] == '&ELECTRONS':
          line = '&ELECTRONS\n' + 'diago_full_acc=.true.\n'
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
        nscf_file.write(str(line))
    return prefix,outdir,nspin,security_check,nscf_file

"""
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
"""

provided_scf_input_file, provided_output_dir,selected_sym,k,nbands,nwan = parser()
scf_file = open(str(provided_scf_input_file), 'r')
# create_bands_input reads the scf, creates bands.in and obtains prefix, outdir,
# for bs files, security check (check provided scf is an scf calculation)
# and the bands file to write the kpath
prefix,outdir,nspin,security_check,nscf_file = create_nscf_input(provided_scf_input_file,scf_file,provided_output_dir)
#create_bs_input(provided_scf_input_file,provided_output_dir,prefix,outdir,nspin)
#sym_manager(selected_sym,win_file)
#create_suggested_run
if security_check != '\'scf\'':
   print('ERROR: provided scf input does not correspond to scf calculation')
