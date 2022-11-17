import numpy as np
from argparse import ArgumentParser

# TO DO LIST
"""
-import run
"""


def parser():
    parser = ArgumentParser(description="Script to create projected DOS calculation inputs")
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
    parser.add_argument("-k", "--k",
                        type=str,
                        required=True,
                        nargs='+',
                        help="kx ky kz for nscf calculation ")
    args = parser.parse_args()
    return args.input,args.out,args.k

def create_nscf_input(scf_input_name,scf_input_file,nscf_output_dir): 
    nscf_output_name = scf_input_name.replace('scf','nscf')
    nscf_output = str(nscf_output_dir) + str(nscf_output_name)
    nscf_file = open(nscf_output , 'w')
    noncolin = security_check = '0'
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
        if line_to_check_vector[0] == 'occupations': 
           line = 'occupations = \'tetrahedra\'\n'
        if line_to_check_vector[0] == 'smearing': 
           line = ''
        if line_to_check_vector[0] == 'degauss': 
           line = ''
        if line_to_check_vector[0] == 'k_points' or line_to_check_vector[0] == 'K_POINTS':
          line = 'K_POINTS automatic\n' + str(k[0]) + " " + str(k[1]) + " " + str(k[2]) + ' 0 0 0\n'
          scf_input_file.readline()
        if line_to_check_vector[0] == 'prefix':
          prefix = line.replace(' ','')
        if line_to_check_vector[0] == 'outdir':
          outdir = line.replace(' ','')
        if line_to_check_vector[0] == 'noncolin': 
            noncolin = '1' 
        nscf_file.write(str(line))
    return prefix,outdir,noncolin,security_check,nscf_file
def create_projwfc_input(scf_input_name,projwfc_output_dir,prefix,outdir):
    # These lines prepare the filband removing strange symbols
    filband = prefix.split("=")
    filband = filband[1]
    filband = filband.replace("'", "") 
    filband = filband.replace("\n", "")
    filband = filband.replace(" ", "") 
    projwfc_output_name = scf_input_name.replace('scf','proj')
    projwfc_file = open(str(projwfc_output_dir) + str(projwfc_output_name) , 'w')
    projwfc_file.write('&PROJWFC\n')
    projwfc_file.write(prefix)
    projwfc_file.write(outdir)
    projwfc_file.write('degauss=0.001\n')
    projwfc_file.write('filpdos = \'' + str(filband) + '.pdos_tot\'\n')
    projwfc_file.write('filproj = \'' + str(filband) + '.proj.dos\'\n')
    projwfc_file.write('DeltaE=0.01\n')
    projwfc_file.write('/')

provided_scf_input_file, provided_output_dir,k = parser()
scf_file = open(str(provided_scf_input_file), 'r')
# create_bands_input reads the scf, creates bands.in and obtains prefix, outdir,
# for bs files, security check (check provided scf is an scf calculation)
# and the bands file to write the kpath
prefix,outdir,noncolin,security_check,nscf_file = create_nscf_input(provided_scf_input_file,scf_file,provided_output_dir)
create_projwfc_input(provided_scf_input_file,provided_output_dir,prefix,outdir)

#create_suggested_run
if security_check != '\'scf\'':
   print('ERROR: provided scf input does not correspond to scf calculation')
if noncolin == '1':
   print('ERROR: noncolinear calculation for PDOS')
