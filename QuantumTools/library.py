from typing import List, Any
from dataclasses import dataclass
import numpy as np

# Where to put ransform_lattice_parameters?
# Is used inside of the QEcalculation class
# maybe i should remove the cell_matrix propertie
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

def manage_input_dir(input_dir_and_name:str) -> str: 
    file_name = input_dir_and_name.split('/')[-1]
    file_dir = input_dir_and_name.replace(file_name, '')
    return file_name, file_dir
def handle_comments(file_name:str) -> List[str]:
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
def clean_uncommented_file(file_list:List[str]) -> List[str]:
    clean_file = []
    symbol_colection = '=()[],'
    for line in file_list:
        for symbol in symbol_colection:
            line= line.replace(symbol,' ')
        clean_file.append(line)   
    return clean_file
def transform_lattice_parameters(cell_matrix:np.ndarray,ibrav:int, \
        cell_parameters_units:np.ndarray,a:float,b:float,c:float, \
        cosac:float,cosab:float,cosbc:float) -> Any:   # ibrav != 0 will be repaired in the future and this will be np.ndarray
    if ibrav == '0' and cell_parameters_units == 'angstrom':
        return cell_matrix
    if ibrav == '0' and cell_parameters_units == 'crystal':
        return np.dot(cell_matrix,a)
    if ibrav != '0':
        print('CRASH ibrav is not 0') 

@dataclass
class QECalculation:
      nat: int = 0
      calculation_type: str = ''
      prefix: str = ''
      outdir: str = ''
      ibrav: int = 0
      nspin: int = 0
      cell_parameters_units: str = ''
      a: float = 0.0
      b: float = 0.0
      c: float = 0.0
      cosac: float = 0.0
      cosab: float = 0.0
      cosbc: float = 0.0
      cell_matrix: np.ndarray = np.array([[]])
      cell_matrix_angstrom: np.ndarray = np.array([[]])
      atomic_positions_units: str = ''
      atomic_matrix: np.ndarray = np.array([[]])
      kpoints: np.ndarray = np.array([])
      def extract_input_information(self,file_name: str) -> None:
          self.nspin = 1
          uncommented_file = handle_comments(file_name)
          clean_file = clean_uncommented_file(uncommented_file)
          for line_number, line in enumerate(clean_file):   
              splitted_line = line.split(); splitted_line.append('end')  
              for word_number, word in enumerate(splitted_line):
                  if word == 'nat':
                    self.nat = int(splitted_line[word_number + 1])
                  if word == 'calculation':
                    self.calculation_type = splitted_line[word_number + 1]
                  if word == 'prefix':
                    self.prefix = splitted_line[word_number + 1]
                  if word == 'outdir':
                    self.outdir = splitted_line[word_number + 1]
                  if word == 'ibrav':
                     self.ibrav = splitted_line[word_number + 1]
                  if word == 'nspin': 
                      if splitted_line[word_number + 1] == '2':
                         self.nspin = '2'                             
                  if word == 'noncolin':    
                         self.nspin = '4'  
                  if word == 'a' or word == 'A': 
                         self.a = float(splitted_line[word_number + 1])
                  if word == 'b' or word == 'B': 
                         self.b = float(splitted_line[word_number + 1])
                  if word == 'c' or word == 'C': 
                         self.c = float(splitted_line[word_number + 1])
                  if word == 'cosac' or word == 'COSAC': 
                         self.cosac = float(splitted_line[word_number + 1])
                  if word == 'cosab' or word == 'COSAB': 
                         self.cosab = float(splitted_line[word_number + 1])
                  if word == 'cosbc' or word == 'COSBC': 
                         self.cosbc = float(splitted_line[word_number + 1])
                  if word == 'CELL_PARAMETERS':
                          self.cell_parameters_units = splitted_line[word_number + 1]
                          v1 = clean_file[line_number + 1].split()
                          v2 = clean_file[line_number + 2].split()
                          v3 = clean_file[line_number + 3].split()
                          self.cell_matrix = np.array([[float(v1[0]),float(v1[1]),float(v1[2])]
                                      ,[float(v2[0]),float(v2[1]),float(v2[2])],
                                      [float(v3[0]),float(v3[1]),float(v3[2])]])
                          self.cell_matrix_angstrom = transform_lattice_parameters(self.cell_matrix, \
                                self.ibrav,self.cell_parameters_units,self.a,self.b, \
                                self.c,self.cosac,self.cosab,self.cosbc)
                  if word == 'ATOMIC_POSITIONS':  
                          self.atomic_positions_units = splitted_line[word_number + 1]
                          self.atomic_matrix = np.chararray((self.nat, 4),itemsize=9)
                          for i in range(0,self.nat,1):
                              atomic_coord  = clean_file[line_number + 1 + i].split()             
                              self.atomic_matrix[i][0] = atomic_coord[0]
                              self.atomic_matrix[i][1] = atomic_coord[1]
                              self.atomic_matrix[i][2] = atomic_coord[2]
                              self.atomic_matrix[i][3] = atomic_coord[3]
                          self.atomic_matrix = self.atomic_matrix.decode("utf-8")
                  if word == 'K_POINTS' or word == 'k_points':
                          self.kpoints = np.array(clean_file[line_number + 1].split())
                          

if __name__ == '__main__':
    file1 = open('/Users/Dorye/Downloads/crcl3.100.z.5.0.scf.in', "r")
    text = file1.read()
    text_list = text.split()
    file1.close()
    print(grep(text_list,'-0.0250908',3))