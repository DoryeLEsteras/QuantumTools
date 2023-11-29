
import numpy as np
from dataclasses import dataclass

@dataclass
class Outcar:
      nk: int = 0
      ispin: int = 0
      kpoints: np.ndarray = np.array([])
      def extract_information(self,file_name:str) -> None:
          with open (file_name,'r') as f:
               for line in f:
                   line = line.split()
                   if len(line)>1: 
                      if line[0] == 'Generated' and line[-1] == 'k-points:':
                         self.nk = int(line[-2]) 
                      if line[0] == 'ISPIN':
                         self.ispin = int(line[2])
                      if line[0] == 'Dimension' and line[2] == 'arrays:':
                         line = f.readline().split()
                         self.nbands = int(line[-1])
          print(self.nbands,self.nk,self.ispin)