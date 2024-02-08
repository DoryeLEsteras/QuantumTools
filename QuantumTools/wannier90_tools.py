import numpy as np
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict, Field
from QuantumTools.directory_and_files_tools import handle_comments,clean_uncommented_file

@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class WannierCalculation:
      nbands: int = 0
      nwan: int = 0
      nat: int = 0
      cell_matrix_angstrom: np.ndarray = Field(default_factory=lambda:np.array([[]]))
      atomic_positions_units: str = ''
      atomic_matrix: np.ndarray = Field(default_factory=lambda:np.array([['0','0','0','0']]))
      def extract_input_information(self,file_name: str) -> None:
          uncommented_file = handle_comments(file_name)
          clean_file = clean_uncommented_file(uncommented_file)
          for line_number, line in enumerate(clean_file): 
              splitted_line = line.split(); splitted_line.append('end')  
              if splitted_line[0] == 'num_bands':
                 self.nbands = int(splitted_line[1])
              if splitted_line[0] == 'num_wann':
                 self.nwan = int(splitted_line[1])
              if splitted_line[0].lower() == 'begin' and splitted_line[1].lower() == 'unit_cell_cart':
                 v1 = clean_file[line_number + 1].split()
                 v2 = clean_file[line_number + 2].split()
                 v3 = clean_file[line_number + 3].split()
                 self.cell_matrix_angstrom = np.array([[float(v1[0]),float(v1[1]),float(v1[2])]
                                      ,[float(v2[0]),float(v2[1]),float(v2[2])],
                                      [float(v3[0]),float(v3[1]),float(v3[2])]])
              if line.lower() == 'begin atoms_cart\n' or line.lower() == 'begin atoms_frac\n':
                 if splitted_line[1].lower() == 'atoms_frac':
                    self.atomic_positions_units = 'crystal'
                 if splitted_line[1].lower() == 'atoms_cart':
                    self.atomic_positions_units = 'cartesian'
                 
                 i=0
                 while line.lower() != 'this loop is infinite':
                     atomic_coord  = np.array(clean_file[line_number + 1 + i].split())      
                     if atomic_coord.size == 2:
                        break
                     self.atomic_matrix = np.vstack((self.atomic_matrix,atomic_coord))
                     i = i + 1

          self.atomic_matrix = np.delete(self.atomic_matrix,[0],axis=0)
          self.nat = int(self.atomic_matrix.size/4)

Wan_Kpath_dict = {
"hex": "\
Γ 0.000 0.000 0.000 M 0.500 0.000 0.000\n\
M 0.500 0.000 0.000 K 0.333 0.333 0.000\n\
K 0.333 0.333 0.000 Γ 0.000 0.000 0.000\n",

"ort": "\
Γ 0.000 0.000  0.000 X 0.500 0.000  0.000\n\
X 0.500 0.000  0.000 S 0.500 0.500  0.000\n\
S 0.500 0.500  0.000 Y 0.000 0.500  0.000\n\
Y 0.000 0.500  0.000 Γ 0.000 0.000  0.000\n",

"bcc": "\
Γ 0.000  0.000 0.000 H 0.500 -0.500 0.500\n\
H 0.500 -0.500 0.500 P 0.250  0.250 0.250\n\
P 0.250  0.250 0.250 Γ 0.000  0.000 0.000\n\
Γ 0.000  0.000 0.000 N 0.000  0.000 0.500\n\
N 0.000  0.000 0.500 P 0.250  0.250 0.250\n\
P 0.250  0.250 0.250 N 0.000  0.000 0.500\n\
N 0.000  0.000 0.500 H 0.500 -0.500 0.500\n",

"pmc": "\
Γ 0.000 0.000 0.000  Y  0.500 0.500 0.000\n\
Y 0.500 0.500 0.000  M  0.500 0.500 0.500\n\
M 0.500 0.500 0.500  A  0.000 0.000 0.500\n\
A 0.000 0.000 0.500  Γ  0.000 0.000 0.000\n\
Γ 0.000 0.000 0.000  L2 0.000 0.500 0.500\n\
L2 0.000 0.500 0.500 Γ  0.000 0.000 0.000\n\
Γ 0.000 0.000 0.000  V2 0.000 0.500 0.000\n"
}