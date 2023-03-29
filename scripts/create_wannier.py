#!/usr/bin/python3.6
import numpy as np
from argparse import ArgumentParser
from typing import List
from subprocess import run
from QuantumTools.library import manage_input_dir, \
     clean_uncommented_file, QECalculation, Wan_Kpath_dict


# TO DO LIST
"""
import suggested runs
"""



def parser():
    parser = ArgumentParser(description="Script to create wannier90 calculation inputs")
    parser.add_argument("-scf", "--scf",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the scf input file
                        """)
    parser.add_argument("-outdir", "--outdir",
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
                        type=int,
                        required=True,
                        nargs='+',
                        help="kx ky kz for nscf calculation ")
    parser.add_argument("-nbands", "--nbands",
                        type=int,
                        required=False,
                        default='',
                        help=" number of bands for Wannier90 calculation")
    parser.add_argument("-nwan", "--nwan",
                        type=int,
                        required=False,
                        default='',
                        help=" number of Wannier functions for Wannier90 calculation")
    parser.add_argument("-Mo", "--Mo",
                        type=float,
                        required=False,
                        default='',
                        help="Maximum for outer window")
    parser.add_argument("-mo", "--mo",
                        type=float,
                        required=False,
                        default='',
                        help="Minimum for outer window")
    parser.add_argument("-Mi", "--Mi",
                        type=float,
                        required=False,
                        default='',
                        help="Maximum for inner window")
    parser.add_argument("-mi", "--mi",
                        type=float,
                        required=False,
                        default='',
                        help="Minimum for inner window")
    parser.add_argument("-orb", "--orb",
                        type=str,
                        required=False,
                        default='',
                        help="""Set projectors for Wannier90 \n
                                use ':' to separate atoms from orbitals \n 
                                use ',' to separate {atom:orb} \n
                                Sintaxis: atom:orb,atom:orb,atom:orb
                                ex : ex: Fe:d,I:pz
                             """)
    args = parser.parse_args()
    return args.scf,args.outdir,args.kpath,args.k,args.nbands,args.nwan, \
           args.Mo,args.mo,args.Mi,args.mi,args.orb
def create_nscf(file_name:str, file_dir:str, nbands:int, k:List[int]) -> None:
    nscf_file_name = file_name.replace('scf','nscf')
    nscf_output = str(file_dir) + str(nscf_file_name)
    with open(file_dir + file_name, 'r') as file:
        lines = file.readlines() 
    original_file = lines   
    clean_file = clean_uncommented_file(lines)
    for line_number, line in enumerate(clean_file):   
        splitted_line = line.split(); splitted_line.append('end')  
        for word_number, word in enumerate(splitted_line):
            if word == 'calculation':
               original_file[line_number] = 'calculation = \'nscf\'\n'
            if word == 'verbosity':
              original_file[line_number] = 'verbosity = \'high\'\n'
            if word == '&system' or word == '&SYSTEM':
              original_file[line_number] = '&SYSTEM\n' + 'nosym=.true.\n' + \
               'noinv=.true.\n' + 'nbnd = ' + str(nbands) + '\nibrav = 0\n'
            if word == '&electrons' or word == '&ELECTRONS':
              original_file[line_number] = '&ELECTRONS\n' + 'diago_full_acc=.true.\n'
            if word == 'k_points' or word == 'K_POINTS':
              original_file[line_number] = ''    
              original_file[line_number + 1] = ''     
            if word == 'ibrav':
              original_file[line_number] = ''           
            if word == 'a':
              original_file[line_number] = ''
            if word == 'b':
              original_file[line_number] = ''
            if word == 'c':
              original_file[line_number] = ''
            if word == 'cosac' or word == 'COSAC':
              original_file[line_number] = ''
            if word == 'cosbc'or word == 'COSBC':
              original_file[line_number] = ''   
            if word == 'cosab'or word == 'COSAB':
              original_file[line_number] = '' 
            kmesh = run(['kmesh.pl', \
                    str(k[0]), str(k[1]), str(k[2])],capture_output=True) 
            output = kmesh.stdout; kmesh = output.decode("utf-8")
    with open(nscf_output, 'w') as nscf_file:   
        for line in original_file: 
            nscf_file.write(str(line))  
        nscf_file.write('CELL_PARAMETERS ( ' + SCF.cell_parameters_units + ' )\n')  
        for i in range(0,3,1):
            for j in range(0,3,1):
                cell_matrix_angstrom = str(SCF.cell_matrix_angstrom[i][j]).replace('[','').replace(']','') 
                nscf_file.write(f"{float(cell_matrix_angstrom):.9f} ")
            nscf_file.write(f"\n")
        nscf_file.write(kmesh)  
def create_pw2wan_input(file_dir:str,seed:str) -> None: 
    if SCF.nspin == 1:
       pw2wan_output_name = str(seed + '.pw2wan.in')
       with open(file_dir + pw2wan_output_name, 'w') as pw2wan_file:
            pw2wan_file.write('&inputpp\n')  
            pw2wan_file.write('seedname = \'' + seed + '\'\n')  
            pw2wan_file.write('outdir = ' + SCF.outdir + '\n')  
            pw2wan_file.write('prefix = ' + SCF.prefix + '\n')  
            pw2wan_file.write('spin_component = \'none\'\n')  
            pw2wan_file.write('write_mmn = .true.\n')  
            pw2wan_file.write('write_amn = .true.\n')  
            pw2wan_file.write('write_unk = .false.\n')  
            pw2wan_file.write('wan_mode = \'standalone\'\n') 
            pw2wan_file.write('/')        
    if SCF.nspin == 2:
       pw2wan_up_output_name = str(seed + '.up.pw2wan.in')
       with open(file_dir + pw2wan_up_output_name, 'w') as pw2wan_up_file:
            pw2wan_up_file.write('&inputpp\n') 
            pw2wan_up_file.write('seedname = \'' + seed + '.up\'\n')  
            pw2wan_up_file.write('outdir = ' + SCF.outdir + '\n')  
            pw2wan_up_file.write('prefix = ' + SCF.prefix + '\n')  
            pw2wan_up_file.write('spin_component = \'up\'\n')  
            pw2wan_up_file.write('write_mmn = .true.\n')  
            pw2wan_up_file.write('write_amn = .true.\n')  
            pw2wan_up_file.write('write_unk = .false.\n')  
            pw2wan_up_file.write('wan_mode = \'standalone\'\n') 
            pw2wan_up_file.write('/')  
       pw2wan_down_output_name = str(seed + '.down.pw2wan.in')
       with open(file_dir + pw2wan_down_output_name, 'w') as pw2wan_down_file:
        pw2wan_down_file.write('&inputpp\n') 
        pw2wan_down_file.write('seedname = \'' + seed + '.down\'\n')  
        pw2wan_down_file.write('outdir = ' + SCF.outdir + '\n')  
        pw2wan_down_file.write('prefix = ' + SCF.prefix + '\n')  
        pw2wan_down_file.write('spin_component = \'down\'\n')  
        pw2wan_down_file.write('write_mmn = .true.\n')  
        pw2wan_down_file.write('write_amn = .true.\n')  
        pw2wan_down_file.write('write_unk = .false.\n')  
        pw2wan_down_file.write('wan_mode = \'standalone\'\n') 
        pw2wan_down_file.write('/')  
    if SCF.nspin == 4:
        pw2wan_output_name = str(seed + '.pw2wan.in')
        with open(file_dir + pw2wan_output_name, 'w') as pw2wan_file:
             pw2wan_file.write('&inputpp\n')  
             pw2wan_file.write('seedname = \'' + seed + '\'\n')  
             pw2wan_file.write('outdir = ' + SCF.outdir + '\n')   
             pw2wan_file.write('prefix = ' + SCF.prefix + '\n') 
             pw2wan_file.write('spin_component = \'none\'\n')  
             pw2wan_file.write('write_mmn = .true.\n')  
             pw2wan_file.write('write_amn = .true.\n')  
             pw2wan_file.write('write_unk = .false.\n') 
             pw2wan_file.write('write_spn=.true.\n')
             pw2wan_file.write('wan_mode = \'standalone\'\n') 
             pw2wan_file.write('/\n') 
def create_win_input(file_dir:str, seed:str, nbands:int, nwan:int, Mo:float, \
                     mo:float, Mi:float, mi:float, projectors:str,k:List[int]) -> None: 
    win_output_name = seed + '.win'
    projectors = projectors.split(',')
    with open(file_dir + win_output_name, 'w') as win_file:
         win_file.write(f"{'!'*80}\n")
         win_file.write(f"{'!'*30}VARIABLES TO SELECT{'!'*31}\n")
         win_file.write(f"{'!'*80}\n")
         win_file.write(f"\n")
         win_file.write(f"num_bands = {str(nbands)}\n")  
         win_file.write(f"num_wann = {str(nwan)}\n")     
         win_file.write(f"dis_win_max = {str(Mo)}\n")               
         win_file.write(f"dis_win_min = {str(mo)}\n")        
         win_file.write(f"dis_froz_max = {str(Mi)}\n")      
         win_file.write(f"dis_froz_min = {str(mi)}\n")   
         win_file.write(f"dis_num_iter = 4000 \n")    
         win_file.write(f"num_iter = 500 \n")        
         win_file.write(f"num_print_cycles = 50 \n")    
         win_file.write(f"\n")

         win_file.write(f"Begin Projections \n")  
         for i in range(0,len(projectors),1):
            win_file.write(f"{projectors[i]}\n")  
         win_file.write(f"End Projections \n")  
         win_file.write(f"\n")

         win_file.write(f"!!! KPATH !!!\n")    
         win_file.write(f"begin kpoint_path \n")  
         if kpath != 'none':  
            win_file.write(f"{Wan_Kpath_dict[kpath]}")
         elif kpath == 'none': 
            win_file.write(f"\n")               
         win_file.write(f"end kpoint_path \n")  
         win_file.write(f"\n")

         win_file.write(f"{'!'*80}\n")
         win_file.write(f"{'!'*25}!!!FLAGS TO PLOT AND DEBUG!!!{'!'*26}\n")
         win_file.write(f"{'!'*80}\n")
         win_file.write(f"\n")

         win_file.write(f"write_xyz = true \n")   
         win_file.write(f"write_hr = true \n")   
         win_file.write(f"bands_plot = true \n")   
         win_file.write(f"iprint = 3\n")   
         win_file.write(f"!restart = plot\n")   
         win_file.write(f"!restart = wannierise\n")   
         win_file.write(f"\n")

         win_file.write(f"!!! for fatbands !!!\n")
         win_file.write(f"!bands_plot_project = i-j \n") 
         win_file.write(f"\n")

         win_file.write(f"!!! for WF plot !!!\n")   
         win_file.write(f"!REMEMBER TO ACTIVATE write_unk = .true. in pw2wan file\n")   
         win_file.write(f"!wannier_plot_format = xcrysden \n")   
         win_file.write(f"!wannier_plot_supercell = 3 3 1 \n")   
         win_file.write(f"!wannier_plot =  true \n")   
         win_file.write(f"!wannier_plot_list = i-j\n")   
         win_file.write(f"\n")

         win_file.write(f"!!! for DOS plot !!!\n")   
         win_file.write(f"!dos = true  \n")   
         win_file.write(f"!dos_kmesh = 25\n")   
         win_file.write(f"!dos_project = i,j,k\n")   
         win_file.write(f"\n")

         win_file.write(f"{'!'*80}\n")
         win_file.write(f"{'!'*34}FIXED FLAGS{'!'*35}\n")
         win_file.write(f"{'!'*80}\n")
         win_file.write(f"\n")

         if SCF.nspin == 4:
            win_file.write(f"spinors = true\n")  
         win_file.write(f"guiding_centres = T \n")   
         win_file.write(f"\n") 

         win_file.write(f"Begin Unit_Cell_Cart\n")   
         for i in range(0,3,1):
            for j in range(0,3,1):
                cell_matrix_angstrom = str(SCF.cell_matrix_angstrom[i][j]).replace('[','').replace(']','') 
                win_file.write(f"{float(cell_matrix_angstrom):.9f} ")
            win_file.write(f"\n")
         win_file.write(f"End Unit_Cell_Cart\n")  
         win_file.write(f"\n")

         if SCF.atomic_positions_units == 'crystal':
             win_file.write(f"Begin Atoms_Frac\n") 
             for i in range(0,SCF.nat,1):
                 atomic_matrix = str(SCF.atomic_matrix[i][0]).replace('[','').replace(']','')
                 atomic_matrix = atomic_matrix.replace("\'", "")
                 win_file.write(f"{atomic_matrix} ")
                 for j in range(1,4,1):
                    atomic_matrix = str(SCF.atomic_matrix[i][j]).replace('[','').replace(']','')
                    atomic_matrix = atomic_matrix.replace("\'", "")
                    win_file.write(f"{float(atomic_matrix):.9f} ")
                 win_file.write(f"\n")                
             win_file.write(f"End Atoms_Frac\n")                  
         if SCF.atomic_positions_units == 'angstrom':
             win_file.write(f"Begin Atoms_Cart\n")     
             for i in range(0,SCF.nat,1):
                 atomic_matrix = str(SCF.atomic_matrix[i]).replace('[','').replace(']','')
                 atomic_matrix = atomic_matrix.replace("\'", "")
                 win_file.write(f"{atomic_matrix}\n")
             win_file.write(f"End Atoms_Cart\n")   
         win_file.write(f"\n")

         win_file.write(f"mp_grid = {str(k[0]):3}{str(k[1]):3}{str(k[2]):3}\n")     

         win_file.write(f"begin kpoints \n")    
         kmesh = run(['kmesh.pl', str(k[0]), str(k[1]), str(k[2]), 'wan'],capture_output=True)
         output = kmesh.stdout; kmesh = output.decode("utf-8")
         win_file.write(f"{kmesh}")   
         win_file.write(f"end kpoints \n")    
         win_file.write(f"{'!'*34}END OF FILE{'!'*35}\n")

    if SCF.nspin == 2:
        win_up_name = seed + '.up' + '.win'
        win_down_name = seed + '.down' + '.win'  
        win_template_output = file_dir + win_output_name          
        win_up_output = file_dir + win_up_name
        win_down_output = file_dir + win_down_name
        run(['cp',win_template_output ,win_up_output])
        run(['mv',win_template_output ,win_down_output])


if __name__ == "__main__":
   #python3.8 manage_comments.py -scf ./feps3.a.a.scf.in -outdir ./ -kpath hex -k 1 1 1 -nbands 12 -nwan 1 -Mo 1 -mo -1 -Mi 0.1 -mi -0.1 -orb Fe:d,I:pz
   file_dir_and_name,outdir,kpath,k,nbands,nwan,Mo,mo,Mi,mi,projectors = parser()
   file_name, file_dir = manage_input_dir(file_dir_and_name)
   SCF = QECalculation()   

   SCF.extract_input_information(file_dir_and_name) 
   if SCF.calculation_type != 'scf':
        print('ERROR: provided scf input does not correspond to scf calculation')
   elif SCF.calculation_type == 'scf':
         seed = file_name.replace('.scf.in', '') 
         create_nscf(file_name, file_dir, nbands, k)
         create_pw2wan_input(file_dir,seed)
         create_win_input(file_dir,seed,nbands,nwan,Mo,mo,Mi,mi,projectors,k)
