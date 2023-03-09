import numpy as np

def count_nbands(bands_file_name:str) -> int:
    nbands = 0
    with open(bands_file_name,'r') as f:
        for line in f:
            read_line = line.split()
            read_line.append('end')
            if read_line[0] == 'end':
               nbands = nbands + 1
    return nbands

def count_nk(bands_file_name:str) -> int:
    nk = 0; counter = 0
    with open(bands_file_name,'r') as f:
        while nk == 0 :
            line = f.readline()
            read_line = line.split()
            read_line.append('end')
            if read_line[0] == 'end':
                nk = counter
            counter = counter + 1
    return nk

def count_occ_bands(bands_file_name:str, fermi:float, file_column:int) -> int:
    nocc_bands = 0
    nk = count_nk(bands_file_name)
    nbands = count_nbands(bands_file_name)
    bands_file = open(bands_file_name,'r')
    for i in range(0,nbands):
        for j in range(0,nk,1):  
            energy = float(bands_file.readline().split()[file_column-1])
            if fermi > energy:
               nocc_bands = i + 1
        bands_file.readline() # to remove \n at the end of each band 
    return nocc_bands

#------------------------

def manage_input_dir(input_dir_and_name:str): 
    file_name = input_dir_and_name.split('/')[-1]
    file_dir = input_dir_and_name.replace(file_name, '')
    return file_name, file_dir
def handle_comments(file_name:str):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        new_line = ''; uncommented_file = []
        for line in lines:
            for character in line:
                if character != '!':
                   new_line = new_line + character
                if character == '!':
                    new_line = new_line + '\n'
                    break 
            uncommented_file.append(new_line)
            new_line = ''
    return uncommented_file
def clean_uncommented_file(file_list):
    clean_file = []
    symbol_colection = '=()[],'
    for line in file_list:
        for symbol in symbol_colection:
            line= line.replace(symbol,' ')
        clean_file.append(line)   
    return clean_file
def extract_input_information(clean_uncommented_file):
    nspin = 1
    cell_matrix = np.array([]); a = 0.0; b = 0.0; c = 0.0
    cosab = 0.0; cosac = 0.0; cosbc = 0.0; cell_parameters_units = ''
    for line_number, line in enumerate(clean_uncommented_file):   
        splitted_line = line.split(); splitted_line.append('end')  
        for word_number, word in enumerate(splitted_line):
            if word == 'nat':
              nat = int(splitted_line[word_number + 1])
            if word == 'calculation':
              calculation_type = splitted_line[word_number + 1]
            if word == 'prefix':
              prefix = splitted_line[word_number + 1]
            if word == 'outdir':
              outdir = splitted_line[word_number + 1]
            if word == 'ibrav':
               ibrav = splitted_line[word_number + 1]
            if word == 'nspin': 
                if splitted_line[word_number + 1] == '2':
                   nspin = '2'                             
                else:
                    print('Unknown nspin flag')
            if word == 'noncolin':    
                   nspin = '4'  
            if word == 'a' or word == 'A': 
                   a = float(splitted_line[word_number + 1])
            if word == 'b' or word == 'B': 
                   b = float(splitted_line[word_number + 1])
            if word == 'c' or word == 'C': 
                   c = float(splitted_line[word_number + 1])
            if word == 'cosac' or word == 'COSAC': 
                   cosac = float(splitted_line[word_number + 1])
            if word == 'cosab' or word == 'COSAB': 
                   cosab = float(splitted_line[word_number + 1])
            if word == 'cosbc' or word == 'COSBC': 
                   cosbc = float(splitted_line[word_number + 1])
            if word == 'CELL_PARAMETERS':
                    cell_parameters_units = splitted_line[word_number + 1]
                    v1 = clean_uncommented_file[line_number + 1].split()
                    v2 = clean_uncommented_file[line_number + 2].split()
                    v3 = clean_uncommented_file[line_number + 3].split()
                    cell_matrix = np.array([[float(v1[0]),float(v1[1]),float(v1[2])]
                                ,[float(v2[0]),float(v2[1]),float(v2[2])],
                                [float(v3[0]),float(v3[1]),float(v3[2])]])
            if word == 'ATOMIC_POSITIONS':  
                    atomic_positions_units = splitted_line[word_number + 1]
                    atomic_matrix = np.chararray((nat, 4),itemsize=9)
                    for i in range(0,nat,1):
                        atomic_coord  = clean_uncommented_file[line_number + 1 + i].split()             
                        atomic_matrix[i][0] = atomic_coord[0]
                        atomic_matrix[i][1] = atomic_coord[1]
                        atomic_matrix[i][2] = atomic_coord[2]
                        atomic_matrix[i][3] = atomic_coord[3]
                    atomic_matrix = atomic_matrix.decode("utf-8")
            if word == 'K_POINTS' or word == 'k_points':
                    kpoints = np.array(clean_uncommented_file[line_number + 1].split())
    return nat, calculation_type, prefix, outdir, ibrav, nspin, \
           cell_parameters_units, a, b, c, cosac, cosab, cosbc, \
           cell_matrix,atomic_positions_units, atomic_matrix, kpoints
def transform_lattice_parameters(cell_matrix,ibrav,cell_parameters_units,
                                 a,b,c,cosac,cosab,cosbc):
    if ibrav == '0' and cell_parameters_units == 'angstrom':
        return cell_matrix
    if ibrav == '0' and cell_parameters_units == 'crystal':
        return np.dot(cell_matrix,a)
    if ibrav != '0':
        print('CRASH ibrav is not 0')   


def grep(read_vector,key_word,position): 
    """
    read_vector is the a vector of strings that contains the input file obtained as:
    text = file1.read(); text_list = text.split() position is the number of sites 
    where the desired word is present respect to the key_word 
    """
    position_of_word = int(read_vector.index(key_word)) + int(position)
    return read_vector[position_of_word] 

if __name__ == '__main__':
    file1 = open('/Users/Dorye/Downloads/crcl3.100.z.5.0.scf.in', "r")
    text = file1.read()
    text_list = text.split()
    file1.close()
    print(grep(text_list,'-0.0250908',3))