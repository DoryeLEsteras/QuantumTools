#!/usr/bin/python3
from argparse import ArgumentParser
from QuantumTools.cluster_tools import initialize_clusters
from QuantumTools.qe_tools import QECalculation
from QuantumTools.directory_and_files_tools import manage_input_dir



def parser():
    parser = ArgumentParser(description="Script to create inputs for projected DOS calculations")
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
    parser.add_argument("-k", "--k",
                        type=str,
                        required=True,
                        nargs='+',
                        help="kx ky kz for nscf calculation ")
    args = parser.parse_args()
    return args.input,args.outdir,args.k

def create_nscf_input(scf_input_name:str,scf_dir:str,nscf_output_dir:str)-> None: 
    nscf_name = scf_input_name.replace('scf','nscf')
    nscf_file = open(nscf_output_dir + '/' + nscf_name , 'w')
    scf_input_file = open(scf_dir + '/' + scf_input_name , 'r')
    for line in scf_input_file:
        line_to_check = line.replace("=", ' ') 
        line_to_check = line_to_check.replace(",", ' ') 
        line_to_check_vector = line_to_check.split()
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
        nscf_file.write(str(line))
    scf_input_file.close()
    nscf_file.close()
def create_projwfc_input(scf_input_name:str,projwfc_output_dir:str)-> None:
    projwfc_name = scf_input_name.replace('scf','proj')
    projwfc_file = open(projwfc_output_dir + '/' + projwfc_name , 'w')
    projwfc_file.write('&PROJWFC\n')
    projwfc_file.write("prefix = '" +str(Scf.prefix)+ "'\n")
    projwfc_file.write("outdir = '" +str(Scf.outdir)+ "'\n")
    projwfc_file.write('degauss = 0.001\n')
    projwfc_file.write("filpdos = '" + str(Scf.prefix) + ".pdos_tot'\n")
    projwfc_file.write("filproj = '" + str(Scf.prefix) + ".proj.dos'\n")
    projwfc_file.write('DeltaE = 0.01\n')
    projwfc_file.write('/')
    projwfc_file.close()
    initialize_clusters('projected',projwfc_output_dir,scf_input_name,'')


if __name__ == '__main__':   
  provided_scf_input_file, provided_output_dir,k = parser()
  Scf = QECalculation()
  Scf.extract_input_information(provided_scf_input_file)
  if Scf.calculation_type != 'scf':
     print('ERROR: provided scf input does not correspond to scf calculation')
  else:  
     file_name,file_dir = manage_input_dir(provided_scf_input_file)
     create_nscf_input(file_name,file_dir,provided_output_dir)
     create_projwfc_input(file_name,provided_output_dir)
     # Security check doesnt stop input creation because someone can want to do SOC PDOS
     if Scf.nspin == 4:
        print('ERROR: noncolinear calculation for PDOS')

