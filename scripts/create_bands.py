#!/usr/bin/python3
from argparse import ArgumentParser
from QuantumTools.cluster_tools import initialize_clusters
from QuantumTools.directory_and_files_tools import manage_input_dir
from QuantumTools.band_tools import DFT_Kpath_dict
from QuantumTools.qe_tools import QECalculation

"""
from QuantumTools.library import initialize_clusters, \
     QECalculation, manage_input_dir,DFT_Kpath_dict
"""

def parser():
    parser = ArgumentParser(description="Script to create band calculation inputs")
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
                        help="Relative or absolute path for the  output directory ")
    parser.add_argument("-kpath", "--kpath",
                        type=str,
                        required=False,
                        default='none',
                        help="Desired kpath. Actual library:\n hex : hexagonal\n" +\
                                "rmc : rectangular monoclinic\n ort : orthorombic\n bcc : bcc " + \
                                "pmc : primitive monoclinic")
    args = parser.parse_args()
    return args.input,args.outdir,args.kpath
    
def create_bands_input(scf_name:str,scf_dir:str,bands_output_dir:str,kpath:str)-> None: 
    bands_file_name = scf_name.replace('scf','bands')
    bands_file = open(bands_output_dir + '/' + bands_file_name , 'w')
    scf_input_file = open(scf_dir + '/' + scf_name, 'r')
    for line in scf_input_file:
        line_to_check = line.replace("=", ' ') 
        line_to_check = line_to_check.replace(",", ' ') 
        line_to_check_vector = line_to_check.split()
        line_to_check_vector.append('end')
        if line_to_check_vector[0] == 'calculation':
           line = 'calculation = \'bands\'\n'
        if line_to_check_vector[0] == 'verbosity':
           line = 'verbosity = \'high\'\n'
        if line_to_check_vector[0] == 'k_points' or line_to_check_vector[0] == 'K_POINTS':
           line = ''
           scf_input_file.readline()
        bands_file.write(str(line))
    bands_file.write(f"K_POINTS (crystal_b)\n")
    if kpath != 'none':  
       bands_file.write(f"{DFT_Kpath_dict[kpath]}")
    elif kpath == 'none': 
       bands_file.write(f"\n")  
    scf_input_file.close()  
    bands_file.close()       
def create_bs_input(scf_name:str,bs_output_dir:str)-> None:
    if Scf.nspin == 1 or Scf.nspin == 4:
        bs_name = scf_name.replace('scf','bs')
        bs_file = open(bs_output_dir + '/' + bs_name , 'w')
        bs_file.write('&BANDS\n')
        bs_file.write("prefix = '" + str(Scf.prefix) + "'\n")
        bs_file.write("outdir = '" + str(Scf.outdir) + "'\n")
        bs_file.write("filband = '" + Scf.prefix + ".bands.dat'\n")
        bs_file.write('lsym=.true.\n')
        bs_file.write('spin_component=1\n')
        bs_file.write('/')
        bs_file.close()
        initialize_clusters('nospin_bands',bs_output_dir,scf_name,'')
    if Scf.nspin == 2:
        bs1_name = scf_name.replace('scf','bs1')
        bs2_name = scf_name.replace('scf','bs2')
        bs1_file = open(bs_output_dir + '/' + bs1_name, 'w')
        bs2_file = open(bs_output_dir + '/' + bs2_name, 'w')
        bs1_file.write('&BANDS\n')
        bs1_file.write("prefix = '" + str(Scf.prefix) + "'\n")
        bs1_file.write("outdir = '" + str(Scf.outdir) + "'\n")
        bs1_file.write("filband = '" + Scf.prefix + ".bands1.dat'\n")
        bs1_file.write('lsym=.true.\n')
        bs1_file.write('spin_component=1\n')
        bs1_file.write('/')
        bs2_file.write('&BANDS\n')
        bs2_file.write("prefix = '" + str(Scf.prefix) + "'\n")
        bs2_file.write("outdir = '" + str(Scf.outdir) + "'\n")
        bs2_file.write("filband = '" + Scf.prefix + ".bands2.dat'\n")
        bs2_file.write('lsym=.true.\n')
        bs2_file.write('spin_component=2\n')
        bs2_file.write('/')
        bs1_file.close()
        bs2_file.close()
        initialize_clusters('spin_bands',bs_output_dir,scf_name,'')


if __name__ == '__main__':
   provided_scf_input_file, provided_output_dir,kpath = parser()
   Scf = QECalculation()
   Scf.extract_input_information(provided_scf_input_file)
   if Scf.calculation_type == 'scf':
      scf_name, scf_dir = manage_input_dir(provided_scf_input_file)
      create_bands_input(scf_name,scf_dir,provided_output_dir,kpath)
      create_bs_input(scf_name,provided_output_dir)
   else:
      print('ERROR: provided scf input does not correspond to scf calculation')
