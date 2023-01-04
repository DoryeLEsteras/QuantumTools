import numpy as np
from argparse import ArgumentParser
import re
from subprocess import run
# TO DO LIST
"""
extend the path library and correct
import suggested runs
Finish the script!!
arreglar formato files
completar opciones parser
arreglar formato bonito con exclamaciones
añadir que para plotear las WF tienes que activar el unk en el pw2
"""


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
def create_nscf_input(scf_input_name,scf_input_file,nscf_output_dir,k):  
    nscf_output_long_name = scf_input_name.replace('scf','nscf')
    nscf_output_long_name = nscf_output_long_name.split('/')
    nscf_output_name = nscf_output_long_name[-1]
    seed = nscf_output_name.replace('.nscf.in', '') 
    nscf_output = str(nscf_output_dir) + str(nscf_output_name)
    nscf_file = open(nscf_output , 'w')
    read_vector = scf_input_file.readlines()
    nspin = security_check = '0'

    for component in range(0, len(read_vector), 1):
        line_to_check = read_vector[component].replace("=", ' ') 
        line_to_check = line_to_check.replace(",", ' ') 
        line_to_check = line_to_check.replace(")", ' ') 
        line_to_check = line_to_check.replace("(", ' ') 
        line_to_check_vector = line_to_check.split()
        line_to_check_vector.append('end')
        counter = 0
        for word in line_to_check_vector:
            if word == 'nat':
               nat = int(line_to_check_vector[counter + 1])
            if word == 'calculation':
               security_check = line_to_check_vector[counter + 1]
               read_vector[component] = 'calculation = \'nscf\'\n'
            if word == 'verbosity':
              read_vector[component] = 'verbosity = \'high\'\n'
            if word == '&system' or word == '&SYSTEM':
              read_vector[component] = '&SYSTEM\n' + 'nosym=.true.\n' + 'noinv=.true.\n' + 'nbnd = ' + str(nbands) + ' \n'
            if word == '&electrons' or word == '&ELECTRONS':
              read_vector[component] = '&ELECTRONS\n' + 'diago_full_acc=.true.\n'
            if word == 'k_points' or line_to_check_vector[0] == 'K_POINTS':
              read_vector[component] = ''
              read_vector[component+1] =''
            if word == 'prefix':
              prefix = read_vector[component]
            if word == 'outdir':
              outdir = read_vector[component]
            if word == 'nspin': 
                if line_to_check_vector[counter + 1] == '2':
                    nspin = '2'
            if word == 'lspinorb': 
                    nspin = '4'    
            else:
                    nspin = '1'
            if word == 'CELL_PARAMETERS':
                cell_parameters_type = line_to_check_vector[counter + 1]
                v1 = read_vector[component +1] 
                v2 = read_vector[component +2] 
                v3 =  read_vector[component +3]
                v1 = v1.split();v2 = v2.split();v3 = v3.split()
                cell_matrix = np.array([[float(v1[0]),float(v1[1]),float(v1[2])],[float(v2[0]),float(v2[1]),float(v2[2])],[float(v3[0]),float(v3[1]),float(v3[2])]])
                if cell_parameters_type == 'crystal':
                    for line in range(0,len(read_vector), 1):
                        check = read_vector[line].replace('=', ' ')
                        check = check.replace(',', ' ')
                        check = check.split()
                        counter2 = 0
                        for word in check:
                            if word == 'a':
                                a =  float(check[counter2 + 1])               
                            counter2 = counter2 +1
                    cell_matrix = np.dot(cell_matrix,a)
            if word == 'ATOMIC_POSITIONS':  
                atomic_positions_type = line_to_check_vector[counter + 1]
                atomic_matrix = np.chararray((nat, 4),itemsize=9)
                for i in range(0,nat,1):
                    atomic_coord  = read_vector[component + 1 + i].split()
                    atomic_matrix[i][0] = atomic_coord[0];atomic_matrix[i][1] = atomic_coord[1];atomic_matrix[i][2] = atomic_coord[2];atomic_matrix[i][3] = atomic_coord[3]
                atomic_matrix = atomic_matrix.decode("utf-8")
        counter = counter + 1
        nscf_file.write(str(read_vector[component]))  
    kmesh = run(['../QuantumTools/kmesh.pl', str(k[0]), str(k[1]), str(k[2])],capture_output=True) 
    output = kmesh.stdout
    kmesh = output.decode("utf-8")
    nscf_file.write(str(kmesh))
    nscf_file.close()
    return prefix,outdir,nspin,security_check,nscf_file,seed,cell_matrix,atomic_matrix,nat,atomic_positions_type
def create_pw2wan_input(pw2wan_output_dir,nspin,outdir,prefix,seed): 
    if nspin == '1':
        pw2wan_output_name = str(seed + '.pw2wan.in')
        pw2wan_output = str(pw2wan_output_dir) + str(pw2wan_output_name)
        pw2wan_file = open(pw2wan_output , 'w')    

        pw2wan_file.write('seedname = \'' + seed + '\'\n')  
        pw2wan_file.write(outdir + '\n')  
        pw2wan_file.write(prefix + '\n')  
        pw2wan_file.write('spin_component = \'none\'\n')  
        pw2wan_file.write('write_mmn = .true.\n')  
        pw2wan_file.write('write_amn = .true.\n')  
        pw2wan_file.write('write_unk = .false.\n')  
        pw2wan_file.write('wan_mode = \'standalone\'\n') 
        pw2wan_file.write('/') 
        pw2wan_file.close()
        
    if nspin == '2':
        pw2wan_up_output_name = str(seed + '.up.pw2wan.in')
        pw2wan_down_output_name = str(seed + '.down.pw2wan.in')
        pw2wan_up_output = str(pw2wan_output_dir) + str(pw2wan_up_output_name)
        pw2wan_down_output = str(pw2wan_output_dir) + str(pw2wan_down_output_name)
        pw2wan_up_file = open(pw2wan_up_output , 'w')    
        pw2wan_down_file = open(pw2wan_down_output , 'w')    

        pw2wan_up_file.write('seedname = \'' + seed + '.up\'\n')  
        pw2wan_up_file.write(outdir + '\n')  
        pw2wan_up_file.write(prefix + '\n')  
        pw2wan_up_file.write('spin_component = \'up\'\n')  
        pw2wan_up_file.write('write_mmn = .true.\n')  
        pw2wan_up_file.write('write_amn = .true.\n')  
        pw2wan_up_file.write('write_unk = .false.\n')  
        pw2wan_up_file.write('wan_mode = \'standalone\'\n') 
        pw2wan_up_file.write('/')  
        pw2wan_up_file.close()

        pw2wan_down_file.write('seedname = \'' + seed + '.down\'\n')  
        pw2wan_down_file.write(outdir + '\n')  
        pw2wan_down_file.write(prefix + '\n')  
        pw2wan_down_file.write('spin_component = \'up\'\n')  
        pw2wan_down_file.write('write_mmn = .true.\n')  
        pw2wan_down_file.write('write_amn = .true.\n')  
        pw2wan_down_file.write('write_unk = .false.\n')  
        pw2wan_down_file.write('wan_mode = \'standalone\'\n') 
        pw2wan_down_file.write('/')  
        pw2wan_down_file.close()     
    if nspin == '4':
        pw2wan_output_name = str(seed + '.pw2wan.in')
        pw2wan_output = str(pw2wan_output_dir) + str(pw2wan_output_name)
        pw2wan_file = open(pw2wan_output , 'w')    
        pw2wan_file.write('seedname = \'' + seed + '\'\n')  
        pw2wan_file.write(outdir)  
        pw2wan_file.write(prefix)  
        pw2wan_file.write('spin_component = \'none\'\n')  
        pw2wan_file.write('write_mmn = .true.\n')  
        pw2wan_file.write('write_amn = .true.\n')  
        pw2wan_file.write('write_unk = .false.\n') 
        pw2wan_file.write('write_spn=.true.\n')
        pw2wan_file.write('wan_mode = \'standalone\'\n') 
        pw2wan_file.write('/\n') 
        pw2wan_file.close()
def create_win_input(win_output_dir,nspin,outdir,prefix,seed,k,cell_matrix,atomic_matrix,nat,atomic_positions_type): 
    win_output = str(win_output_dir) + str(seed + '.win')
    win_file = open(win_output , 'w')    
    win_file.write('!!!!!VARIABLES TO SELECT!!!!!\n')
    win_file.write('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
    win_file.write('						    !	\n')
    win_file.write('num_bands         =   ' + nbands + ' !\n')
    win_file.write('num_wann          =  ' + nwan + '   !\n')
    win_file.write('dis_win_max       =         !\n')
    win_file.write('dis_win_min       =         !\n')
    win_file.write('dis_froz_min      =         !\n')
    win_file.write('dis_froz_max      =         !\n')
    win_file.write('dis_num_iter      = 4000    !\n')
    win_file.write('num_iter          = 500     !\n')
    win_file.write('num_print_cycles  = 50      !\n')
    win_file.write('                            !\n')
    win_file.write('Begin Projections           !\n')
    win_file.write('                            !\n')
    win_file.write('End Projections             !\n')
    win_file.write('                            !\n')
    win_file.write('!KPATH                      !\n')
    win_file.write('                            !\n')
    win_file.write('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
    win_file.write('\n')
    win_file.write('\n')
    win_file.write('!!!FLAGS TO PLOT AND DEBUG!!!\n')
    win_file.write('                            !\n')
    win_file.write('write_xyz= true             !\n')
    win_file.write('write_hr=true               !\n')
    win_file.write('bands_plot = true           !\n')
    win_file.write('iprint=3                    !\n')
    win_file.write('!restart=plot               !\n')
    win_file.write('!restart=wannierise         !\n')
    win_file.write('                            !\n')
    win_file.write('! for fatbands              !\n')
    win_file.write('                            !\n')
    win_file.write('! for WF plot               !\n')
    win_file.write('!wannier_plot_format= xcrysden                            !\n')
    win_file.write('!wannier_plot_supercell= 3 3 1                            !\n')
    win_file.write('!wannier_plot           =  true                            !\n')
    win_file.write('!wannier_plot_list = x-y                            !\n')
    win_file.write('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
    win_file.write('\n')
    win_file.write('\n')
    win_file.write('!!!!!!!!!FIXED FLAGS!!!!!!!!!\n')
    win_file.write('                            !\n')
    if nspin == '4':
        win_file.write('spinors = true                !\n')
    win_file.write('guiding_centres = T         !\n')
    win_file.write('Begin Unit_Cell_Cart        !\n')
    cell_matrix = str(cell_matrix).replace('[','')
    cell_matrix = cell_matrix.replace(']','') 
    win_file.write(cell_matrix + '\n')
    win_file.write('End Unit_Cell_Cart          !\n')
    for i in range(0,nat,1):      
        for j in range(10):
            atomic_matrix[i][0] = atomic_matrix[i][0].replace(str(j),'')
    atomic_matrix = str(atomic_matrix).replace('[','')
    atomic_matrix = str(atomic_matrix).replace(']','')
    atomic_matrix = str(atomic_matrix).replace('\'','') 
    win_file.write('\n')
    if atomic_positions_type == 'crystal':
        win_file.write('Begin Atoms_Frac                            \n')
        win_file.write(str(atomic_matrix) + '\n')
        win_file.write('End Atoms_Frac                            \n') 
    if atomic_positions_type == 'angstrom':
        win_file.write('Begin Atoms_Cart                            \n')
        win_file.write(str(atomic_matrix) + '\n')
        win_file.write('End Atoms_Cart                            \n')     
    win_file.write('\n')   
    win_file.write('mp_grid   = ' + str(k[0]) + str(k[1]) + str(k[2]) + '        !\n')     
    win_file.write('begin kpoints                            \n')
    kmesh = run(['../QuantumTools/kmesh.pl', str(k[0]), str(k[1]), str(k[2]), 'wan'],capture_output=True) 
    output = kmesh.stdout
    kmesh = output.decode("utf-8")
    win_file.write(kmesh)
    win_file.write('end kpoints                            \n')    
    win_file.write('                            !\n')
    win_file.write('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
    win_file.close()   

        # task 5 usar subprocees con cp para crear el segundo archivo
            #if nspin == '2':
    #    kmesh = run(['cp', win_output, str(k[1])]) 
       #win_down_file.close()
    # task 6 se returna dependiendo del nspin, el nombre del win para que despues
    # el symetry manager meta el camino
#task 6 meter fatbands 



provided_scf_input_file, provided_output_dir, selected_sym, k, nbands, nwan = parser()
scf_file = open(str(provided_scf_input_file), 'r')

prefix,outdir,nspin,security_check,nscf_file,seed,cell_matrix,atomic_matrix,nat,atomic_positions_type = create_nscf_input(provided_scf_input_file,scf_file,provided_output_dir,k)
create_pw2wan_input(provided_output_dir,nspin,outdir,prefix,seed)
create_win_input(provided_output_dir,nspin,outdir,prefix,seed,k,cell_matrix,atomic_matrix,nat,atomic_positions_type)
#sym_manager(selected_sym,win_file)
#create_suggested_run
scf_file.close()

if security_check != '\'scf\'':
   print('ERROR: provided scf input does not correspond to scf calculation')
