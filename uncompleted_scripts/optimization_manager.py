import numpy as np
from argparse import ArgumentParser

# TO DO LIST
"""
Finish vc-relax part
Find a way of improving ibrav != 0 and cell_dofree = ibrav

"""

def parser():
    parser = ArgumentParser(description="")
    parser.add_argument("-input", "--input",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the exchange file
                        """)
    parser.add_argument("-out", "--out",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the output file
                        """)    
    parser.add_argument("-name", "--name",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the output file
                        """)  
    parser.add_argument("-mode", "--mode",
                        type=str,
                        required=True,
                        help="""
                        Restart or scf
                        """)  
    args = parser.parse_args()
    return args.input,args.out,args.name,args.mode

def analyze_input(opt_input):
    ibrav = nat = 0; calculation_type = 'none'; read_vector = []
    for line in inrelax_file:
        readed_line = line.replace('=', ' ')
        readed_line = line.replace(',', ' ')
        readed_line = readed_line.split()
        readed_line.append('end')
        if readed_line[0] == 'calculation':
            calculation_type = readed_line[2]
        if readed_line[0] == 'ibrav':
            ibrav = readed_line[2]
        if readed_line[0] == 'nat':
            nat = int(readed_line[2])
        line_check = line.replace('(','')
        line_check = line_check.replace(')', '')
        line_check = line_check.split()
        line_check.append('end')
        if line_check[0] != 'ATOMIC_POSITIONS' and line_check[0] != 'CELL_PARAMETERS':
            read_vector.append(line)
        if line_check[0] == 'CELL_PARAMETERS':
            for i in range(0, nat+5, 1):
                opt_input.readline()
        if line_check[0] == 'ATOMIC_POSITIONS':
            for i in range(0, nat, 1):
                opt_input.readline()
    return calculation_type, ibrav, nat, read_vector
def extract_coordinates(opt_output, nat, calculation_type):
    coordinates = []; filter = []
    readed_line = '' 
    while readed_line != 'End final coordinates\n':
          readed_line = opt_output.readline()
          filter.append(readed_line)
    if calculation_type.replace("'", "") == 'relax':
        for x in range(0 , nat ,1):
            coordinates.append(filter[len(filter)-1 - nat + x]) 
    if calculation_type.replace("'", "") == 'vc-relax': 
        for x in range(0 , nat + 6 ,1):
            coordinates.append(filter[len(filter)-1 - nat -6 + x])
    return coordinates
def input_generator(calculation_type,mode,ibrav,output_file,coordinates,new_input_vector):
    print(mode,calculation_type.replace("'", ""))
    if mode == 'restart' and calculation_type.replace("'", "") == 'relax':
        for line in new_input_vector:
            output_file.write(str(line))
        output_file.write('\n\n')
        for line in coordinates:        
            output_file.write(str(line))
    if mode == 'scf' and calculation_type.replace("'", "") == 'relax':
        for index in range(0, len(new_input_vector), 1):
            check_line = new_input_vector[index].replace('=', ' ')
            check_line = check_line.replace(',', ' ')
            check_line = check_line.split()
            check_line.append('end')
            if check_line[0] == 'calculation':
                new_input_vector[index] = ''
                output_file.write("calculation = 'scf'\n")
            if  check_line[0] == 'etot_conv_thr': 
                new_input_vector[index] = ''
            if  check_line[0] == 'forc_conv_thr': 
                new_input_vector[index] = ''
            if  check_line[0] == 'nstep': 
                new_input_vector[index] = ''
            if  check_line[0] == 'tstress': 
                new_input_vector[index] = ''
                output_file.write("tstress = .false.\n ")
                print('Warning: pressure deactivated to avoid problems')
            if  check_line[0] == 'tprnfor': 
                new_input_vector[index] = ''
                output_file.write("tprnfor = .false.\n ")
                print('Warning: forces deactivated to avoid problems')
            if  check_line[0] == '&CELL': 
                new_input_vector[index] = ''
                check = new_input_vector[index+1]
                check = check.split('=')
                check.append('end')
                if check[0] == '/':
                    new_input_vector[index+1] = ''
                if check[0] == '/n':
                    new_input_vector[index+1] = ''
                if check[0] == 'cell_dofree':
                    new_input_vector[index+1] = ''
                    new_input_vector[index+2] = ''
            if  check_line[0] == '&IONS': 
                new_input_vector[index+1] = ''
            else:
                output_file.write(new_input_vector[index])
        output_file.write('\n\n')    
        for line in coordinates:    
            output_file.write(str(line))
    #if mode == 'restart' and calculation_type.replace("'", "") == 'vc-relax':
    """
    inside of these two modes we should consider four options:
    - ibrav = 0 and there is no a -> cell parameters are in A, is direct
    - ibrav = 0 and there is  a -> cell parameters are in crystal, is direct (is better 
    to put express cell parameters as cell*a to avoid problems with possible wannier and remove
    the a in the input)
    -ibrav != 0 and cell_dofree != ibrav -> change ibrav line to 0 and put cell parameters
    in A
    -ibrav != 0 and cell_dofree = ibrav -> we are fucked, warning to user
    """
    #if mode == 'scf' and calculation_type.replace("'", "") == 'vc-relax':

provided_input_file, provided_output_file, name, mode = parser()
inrelax_file = open(str(provided_input_file), 'r')
outrelax_file = open(str(provided_output_file), 'r')
output_file = open(str(name), 'w')


if mode == 'scf' or  mode == 'restart':
    calculation_type, ibrav, nat , new_input_vector= analyze_input(inrelax_file)
    coordinates = extract_coordinates(outrelax_file,nat,calculation_type)
    input_generator(calculation_type,mode,ibrav,output_file,coordinates,new_input_vector)

else:   
    print('ERROR: invalid mode, please choose between mode scf or restart')
