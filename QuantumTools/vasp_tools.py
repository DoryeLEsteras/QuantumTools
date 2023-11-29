
import numpy as np
from dataclasses import dataclass

class Outcar:
      nk: int = 0
      ispin: int = 0
      kpoints: np.ndarray = np.array([])
      
      def vasp_extract_nk(self,file_name:str) -> int:
          with open (file_name,'r') as f:
               for line in f:
                   line = line.split()
                   if len(line)>1: 
                      if line[0] == 'Generated' and line[-1] == 'k-points:':
                         self.nk = int(line[-2])
  
      def vasp_extract_ispin(self,file_name:str) -> int:
          with open (file_name,'r') as f:
               for line in f:
                   line = line.split()
                   if len(line)>1: 
                      if line[0] == 'ISPIN':
                         self.ispin = int(line[2])
