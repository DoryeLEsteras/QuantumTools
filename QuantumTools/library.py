
from typing import List
from dataclasses import dataclass
import numpy as np
#solve ibrav != 0
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
def transform_to_ibrav0(ibrav:int,a:float,b:float,c:float, \
                    cosab:float,cosbc:float,cosac:float) -> np.ndarray:
    if ibrav == 1:
       cell_matrix = np.array([[a, 0, 0 ],[0, a, 0 ],[0, 0, a ]])
    elif ibrav == 2:
       cell_matrix = np.array([[-0.5*a, 0, 0.5*a ],[0, 0.5*a, 0.5*a ],[-0.5*a, 0.5*a, 0 ]])
    elif ibrav == 3:
       cell_matrix = np.array([[0.5*a, 0.5*a, 0.5*a ],[-0.5*a, 0.5*a, 0.5*a ],[-0.5*a, -0.5*a, 0.5*a ]])
    elif ibrav == -3:
       cell_matrix = np.array([[-0.5*a, 0.5*a, 0.5*a ],[0.5*a, -0.5*a, 0.5*a ],[0.5*a, 0.5*a, -0.5*a ]])
    elif ibrav == 4:
       cell_matrix = np.array([[a, 0, 0 ],[-0.5*a, 0.5*a*np.sqrt(3), 0 ],[0, 0, c ]])
    elif ibrav == 1:
       cell_matrix = np.array([[a, 0, 0 ],[0, a, 0 ],[0, 0, a ]])
    elif ibrav == 1:
       cell_matrix = np.array([[a, 0, 0 ],[0, a, 0 ],[0, 0, a ]])
    elif ibrav == 6:
       cell_matrix = np.array([[a, 0, 0 ],[0, a, 0 ],[0, 0, c ]])
    elif ibrav == 7:
       cell_matrix = np.array([[0.5*a, -0.5*a, c/2 ],[0.5*a, 0.5*a, c/2 ],[-0.5*a, -0.5*a, c/2 ]])
    elif ibrav == 8:
       cell_matrix = np.array([[a, 0, 0 ],[0, b, 0 ],[0, 0, c ]])
    elif ibrav == 9:
       cell_matrix = np.array([[0.5*a, 0.5*b, 0 ],[-0.5*a, 0.5*b, 0 ],[0, 0, c ]])
    elif ibrav == -9:
       cell_matrix = np.array([[0.5*a, -0.5*b, 0 ],[0.5*a, 0.5*b, 0 ],[0, 0, c ]])
    elif ibrav == 91:
       cell_matrix = np.array([[a, 0, 0 ],[0, 0.5*b, -0.5*c ],[0, 0.5*b, 0.5*c ]])
    elif ibrav == 10:
       cell_matrix = np.array([[0.5*a, 0, 0.5*c ],[0.5*a, 0.5*b, 0 ],[0, 0.5*b, 0.5*c ]])
    elif ibrav == 11: 
       cell_matrix = np.array([[0.5*a, 0.5*b,0.5*c],[-0.5*a, 0.5*b, 0.5*c ],[-0.5*a, -0.5*b, 0.5*c ]])
    elif ibrav == 1: 
       cell_matrix = np.array([[a, 0, 0 ],[b*cosab,a , 0 ],[0, 0, a ]])
    elif ibrav == 1:
       cell_matrix = np.array([[a, 0, 0 ],[0, a, 0 ],[0, 0, a ]])
    elif ibrav == 1:
       cell_matrix = np.array([[a, 0, 0 ],[0, a, 0 ],[0, 0, a ]])
    elif ibrav == 1:
       cell_matrix = np.array([[a, 0, 0 ],[0, a, 0 ],[0, 0, a ]])
    elif ibrav == 1:
       cell_matrix = np.array([[a, 0, 0 ],[0, a, 0 ],[0, 0, a ]])
    return cell_matrix
def transform_lattice_parameters(cell_matrix:np.ndarray,ibrav:int, \
        cell_parameters_units:np.ndarray,a:float,b:float,c:float, \
        cosac:float,cosab:float,cosbc:float) -> np.ndarray:  
    if ibrav == 0 and cell_parameters_units == 'angstrom':
        return cell_matrix
    if ibrav == 0 and cell_parameters_units == 'crystal':
        return np.dot(cell_matrix,a)
    if ibrav == 0 and cell_parameters_units == 'alat':
        return np.dot(cell_matrix,a)
    if ibrav != 0:
        return transform_to_ibrav0(ibrav,a,b,c,cosab,cosbc,cosac)


Wan_Kpath_dict = {
"hex": "\
Γ 0.000 0.000 0.000 M 0.500 0.000 0.000\n\
M 0.500 0.000 0.000 K 0.333 0.333 0.000\n\
K 0.333 0.333 0.000 Γ 0.000 0.000 0.000\n",

"ex1": "\
Γ 0.000 0.000 0.000 M 0.500 0.000 0.000\n\
M 0.500 0.000 0.000 K 0.333 0.333 0.000\n \
K 0.333 0.333 0.000 Γ 0.000 0.000 0.000\n",

"ex2": "\
Γ 0.000 0.000 0.000 M 0.500 0.000 0.000\n\
M 0.500 0.000 0.000 K 0.333 0.333 0.000\n\
K 0.333 0.333 0.000 Γ 0.000 0.000 0.000\n"

}
DFT_Kpath_dict = {
"hex": "\
0.000 0.000 0.000 20 !Γ\n\
0.333 0.333 0.000 20 !K\n\
0.500 0.000 0.000 20 !M\n\
0.000 0.000 0.000  0 !Γ\n",

"ex1": "\
0.000 0.000 0.000 20 !Γ\n\
0.333 0.333 0.000 20 !K\n\
0.500 0.000 0.000 20 !M\n\
0.000 0.000 0.000  0 !Γ\n",

"ex2": "\
0.000 0.000 0.000 20 !Γ\n\
0.333 0.333 0.000 20 !K\n\
0.500 0.000 0.000 20 !M\n\
0.000 0.000 0.000  0 !Γ\n"

}

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
      cell_dofree: str = ''
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
                    self.calculation_type = splitted_line[word_number + 1].replace("\'","")
                  if word == 'prefix':
                    self.prefix = splitted_line[word_number + 1]
                  if word == 'outdir':
                    self.outdir = splitted_line[word_number + 1]
                  if word == 'ibrav':
                     self.ibrav = splitted_line[word_number + 1]
                  if word == 'nspin': 
                      if splitted_line[word_number + 1] == '2':
                         self.nspin = 2       
                  if word == 'cell_dofree': 
                         self.cell_dofree = splitted_line[word_number + 1].replace("'","")                           
                  if word == 'noncolin':    
                         self.nspin = 4  
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
                          self.atomic_matrix = np.chararray((self.nat, 4),itemsize=12)
                          for i in range(0,self.nat,1):
                              atomic_coord  = clean_file[line_number + 1 + i].split()             
                              self.atomic_matrix[i][0] = atomic_coord[0]
                              self.atomic_matrix[i][1] = atomic_coord[1]
                              self.atomic_matrix[i][2] = atomic_coord[2]
                              self.atomic_matrix[i][3] = atomic_coord[3]
                          self.atomic_matrix = self.atomic_matrix.decode("utf-8")
                  if word == 'K_POINTS' or word == 'k_points':
                          self.kpoints = np.array(clean_file[line_number + 1].split())
@dataclass
class QEoutput:
  calculation_finished: bool = 0
  nat: int = 0
  a: float = 0.0
  cell_parameters_units: str = ''
  cell_matrix: np.ndarray = np.array([[]])
  cell_matrix_angstrom: np.ndarray = np.array([[]])
  atomic_positions_units: str = ''
  atomic_matrix: np.ndarray = np.array([[]])
  def extract_output_information(self,file_name: str) -> None:
      with open(file_name, 'r') as file:
        file_vector = file.readlines()
        clean_file = clean_uncommented_file(file_vector)
      for line_number, line in enumerate(clean_file): 
          if line == 'End final coordinates\n':
             self.calculation_finished = 1   
          splitted_line = line.split(); splitted_line.append('end') 
          if splitted_line[0] == 'number' and splitted_line[1] == 'of': 
             if splitted_line[2] == 'atoms/cell' or splitted_line[2] == 'atoms':
                self.nat = int(splitted_line[-2]) 
          if splitted_line[0] == 'lattice' and splitted_line[1] == 'parameter':
              self.a =  float(splitted_line[-3]) * 0.529177
          for word_number, word in enumerate(splitted_line):
              if word == 'CELL_PARAMETERS':
                      self.cell_parameters_units = splitted_line[word_number + 1]                       
                      v1 = clean_file[line_number + 1].split()
                      v2 = clean_file[line_number + 2].split()
                      v3 = clean_file[line_number + 3].split()
                      self.cell_matrix = np.array([[float(v1[0]),float(v1[1]),float(v1[2])]
                                  ,[float(v2[0]),float(v2[1]),float(v2[2])],
                                  [float(v3[0]),float(v3[1]),float(v3[2])]])
                      self.cell_matrix_angstrom = self.cell_matrix * self.a                
              if word == 'ATOMIC_POSITIONS':  
                      self.atomic_positions_units = splitted_line[word_number + 1]
                      self.atomic_matrix = np.chararray((self.nat, 4),itemsize=12)
                      for i in range(0,self.nat,1):
                          atomic_coord  = clean_file[line_number + 1 + i].split()             
                          self.atomic_matrix[i][0] = atomic_coord[0]
                          self.atomic_matrix[i][1] = atomic_coord[1]
                          self.atomic_matrix[i][2] = atomic_coord[2]
                          self.atomic_matrix[i][3] = atomic_coord[3]
                      self.atomic_matrix = self.atomic_matrix.decode("utf-8")                          

if __name__ == '__main__':
   print('hi !')
