import numpy as np
from dataclasses import dataclass
from QuantumTools.directory_and_files_tools import handle_comments, clean_uncommented_file
from QuantumTools.structure_tools import transform_lattice_parameters

@dataclass
class QECalculation:
      nat: int = 0
      ntyp: int = 0
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
      celldm1: float = 0.0
      celldm2: float = 0.0
      celldm3: float = 0.0
      celldm4: float = 0.0
      celldm5: float = 0.0
      celldm6: float = 0.0
      cell_matrix: np.ndarray = np.array([[]])
      cell_matrix_cartesian: np.ndarray = np.array([[]])
      atomic_positions_units: str = ''
      atomic_matrix: np.ndarray = np.array([[]])
      kpoints: np.ndarray = np.array([])
      cell_dofree: str = ''
      def extract_input_information(self,file_name: str) -> None:
          # extract a,b,c will fail if someone uses A,B,C. However if I include
          #A,B,C in the conditionals Carbon and Boron atomic coordinates will
          # be interpreted as lattice parameters
          self.nspin = 1
          uncommented_file = handle_comments(file_name)
          clean_file = clean_uncommented_file(uncommented_file)
          for line_number, line in enumerate(clean_file):
              splitted_line = line.split(); splitted_line.append('end')  
              for word_number, word in enumerate(splitted_line):
                  if word == 'nat':
                    self.nat = int(splitted_line[word_number + 1])
                  if word == 'ntyp':
                    self.ntyp = int(splitted_line[word_number + 1])
                  if word == 'calculation':
                    self.calculation_type = splitted_line[word_number + 1].replace("\'","")
                  if word == 'prefix':
                    self.prefix = splitted_line[word_number + 1].replace("\'","")
                  if word == 'outdir':
                    self.outdir = splitted_line[word_number + 1].replace("\'","")
                  if word == 'ibrav':
                     self.ibrav = int(splitted_line[word_number + 1])
                  if word == 'nspin': 
                      if splitted_line[word_number + 1] == '2':
                         self.nspin = 2       
                  if word == 'cell_dofree': 
                         self.cell_dofree = splitted_line[word_number + 1].replace("'","")                           
                  if word == 'noncolin':    
                         self.nspin = 4  
                  if word == 'a': 
                         self.cell_parameters_units = 'angstrom'
                         self.a = float(splitted_line[word_number + 1])
                  if word == 'b': 
                         self.b = float(splitted_line[word_number + 1])
                  if word == 'c': 
                         self.c = float(splitted_line[word_number + 1])
                  if word == 'cosac' or word == 'COSAC': 
                         self.cosac = float(splitted_line[word_number + 1])
                  if word == 'cosab' or word == 'COSAB': 
                         self.cosab = float(splitted_line[word_number + 1])
                  if word == 'cosbc' or word == 'COSBC': 
                         self.cosbc = float(splitted_line[word_number + 1]) 
                  if word == 'celldm':
                         if splitted_line[word_number + 1] == '1':
                            self.cell_parameters_units = 'bohr'
                            self.celldm1 = float(splitted_line[word_number + 2])
                         if splitted_line[word_number + 1] == '2':
                            self.celldm2 = float(splitted_line[word_number + 2])
                         if splitted_line[word_number + 1] == '3':
                            self.celldm3 = float(splitted_line[word_number + 2])
                         if splitted_line[word_number + 1] == '4':
                            self.celldm4 = float(splitted_line[word_number + 2])
                         if splitted_line[word_number + 1] == '5':
                            self.celldm5 = float(splitted_line[word_number + 2])
                         if splitted_line[word_number + 1] == '6':
                            self.celldm6 = float(splitted_line[word_number + 2])
                  if word == 'CELL_PARAMETERS':
                          splitted_line = str(splitted_line).replace('}','').replace('{','').replace(')','').replace('(','').split()
                          self.cell_parameters_units = splitted_line[1]
                          v1 = clean_file[line_number + 1].split()
                          v2 = clean_file[line_number + 2].split()
                          v3 = clean_file[line_number + 3].split()
                          self.cell_matrix = np.array([[float(v1[0]),float(v1[1]),float(v1[2])]
                                      ,[float(v2[0]),float(v2[1]),float(v2[2])],
                                      [float(v3[0]),float(v3[1]),float(v3[2])]])
                  if word == 'ATOMIC_POSITIONS': 
                          splitted_line = line.replace('}','').replace('{','').replace(')','').replace('(','').split()
                          self.atomic_positions_units = splitted_line[1]
                          self.atomic_matrix = np.chararray((self.nat, 7),itemsize=12)         
                          if clean_file[line_number + 1] == '\n':
                             line_number = line_number + 1
                          for i in range(0,self.nat,1):
                              atomic_coord  = clean_file[line_number + 1 + i].split()    
                              self.atomic_matrix[i][0] = atomic_coord[0]
                              self.atomic_matrix[i][1] = atomic_coord[1]
                              self.atomic_matrix[i][2] = atomic_coord[2]
                              self.atomic_matrix[i][3] = atomic_coord[3]
                              self.atomic_matrix[i][4] = ''
                              self.atomic_matrix[i][5] = ''
                              self.atomic_matrix[i][6] = ''
                              if len(atomic_coord) == 7:
                                 self.atomic_matrix[i][4] = atomic_coord[4]
                                 self.atomic_matrix[i][5] = atomic_coord[5]
                                 self.atomic_matrix[i][6] = atomic_coord[6]                          
                          self.atomic_matrix = self.atomic_matrix.decode("utf-8")       
                  if word == 'K_POINTS' or word == 'k_points':
                          self.kpoints = np.array(clean_file[line_number + 1].split())
          self.cell_matrix_cartesian = transform_lattice_parameters(self.cell_matrix, \
                        self.ibrav,self.cell_parameters_units,self.a,self.b, \
                        self.c,self.cosac,self.cosab,self.cosbc, \
                        self.celldm1,self.celldm2,self.celldm3,self.celldm4, \
                        self.celldm5,self.celldm6)
@dataclass
class QEoutput:
  calculation_finished: bool = 0
  nat: int = 0
  a: float = 0.0
  total_energy: float = 0.0
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
                      splitted_line = line.replace('}','').replace('{','').replace(')','').replace('(','').split()
                      self.cell_parameters_units = splitted_line[1]
                      v1 = clean_file[line_number + 1].split()
                      v2 = clean_file[line_number + 2].split()
                      v3 = clean_file[line_number + 3].split()
                      self.cell_matrix = np.array([[float(v1[0]),float(v1[1]),float(v1[2])]
                                  ,[float(v2[0]),float(v2[1]),float(v2[2])],
                                  [float(v3[0]),float(v3[1]),float(v3[2])]])
                      self.cell_matrix_angstrom = self.cell_matrix * self.a                
              if word == 'ATOMIC_POSITIONS':  
                      splitted_line = line.replace('}','').replace('{','').replace(')','').replace('(','').split()
                      self.atomic_matrix_units = splitted_line[1]
                      self.atomic_matrix = np.chararray((self.nat, 7),itemsize=12)         
                      for i in range(0,self.nat,1):
                          atomic_coord  = clean_file[line_number + 1 + i].split()           
                          self.atomic_matrix[i][0] = atomic_coord[0]
                          self.atomic_matrix[i][1] = atomic_coord[1]
                          self.atomic_matrix[i][2] = atomic_coord[2]
                          self.atomic_matrix[i][3] = atomic_coord[3]
                          self.atomic_matrix[i][4] = ''
                          self.atomic_matrix[i][5] = ''
                          self.atomic_matrix[i][6] = ''
                          if len(atomic_coord) == 7:
                             self.atomic_matrix[i][4] = atomic_coord[4]
                             self.atomic_matrix[i][5] = atomic_coord[5]
                             self.atomic_matrix[i][6] = atomic_coord[6]                          
                      self.atomic_matrix = self.atomic_matrix.decode("utf-8")        
              if word == '!':
                      self.total_energy = float(splitted_line[word_number + 3])
