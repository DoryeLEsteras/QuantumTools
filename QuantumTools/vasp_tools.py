
import numpy as np
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict, Field
from typing import List

@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class Outcar:
      nk: int = 0
      ispin: int = 0
      energy: float = 0.0
      kpoints: np.ndarray = Field(default_factory=lambda:np.array([]))
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
                      if line[0] == 'free' and line[1] == 'energy':
                         self.energy = float(line[-2])

@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class Poscar:
      poscar_file: List = Field(default_factory=lambda:[])
      nat: int = 0
      ntyp: int = 0
      lattice_parameter_scaling_factor: float = 0.0
      units_atomic_coordinates: str = ''
      atom_label_list: List = Field(default_factory=lambda:[])
      cell_parameters: np.ndarray = Field(default_factory=lambda:np.zeros((3,3)))
      atomic_coordinates: np.ndarray = Field(default_factory=lambda:np.array([]))
      def read_data(self,poscar_file_name: str) -> None:
          file = open(poscar_file_name,'r')
          self.poscar_file = file.readlines()
          file.close()
          
          file = open(poscar_file_name,'r')
          file.readline()
          self.lattice_parameter_scaling_factor = float(file.readline())
          self.cell_parameters[0] = file.readline().split()
          self.cell_parameters[1] = file.readline().split()
          self.cell_parameters[2] = file.readline().split()
          labels = file.readline().split()
          self.ntyp = len(labels)
          number_types = file.readline().split()
          self.nat = sum([int(i) for i in number_types])
          for i in range(self.ntyp):
              for j in range(int(number_types[i])):
                  self.atom_label_list.append(labels[i])
          self.units_atomic_coordinates = file.readline().split()[0]
          self.atomic_coordinates = np.zeros((self.nat,3))
          for i in range(self.nat):
              self.atomic_coordinates[i] = file.readline().split()      
          self.cell_parameters = self.cell_parameters * self.lattice_parameter_scaling_factor
          file.close()

@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class Incar:
      incar_file: List = Field(default_factory=lambda:[])
      prec: str = ''
      ismear: int = 0
      sigma: float = 0.0
      encut: float = 0.0
      nelm:  int = 0
      lwave: str = ''
      lcharg: str = ''
      ispin:  int = 0
      ivdw:  int = 0
      ediff: float = 0.0
      nelect: float = 0.0
      magmom: str = ''
      ldau: str = ''
      ldautype:  int = 0
      ldaul: str = ''
      ldauu: str = ''
      ldauj: str = ''
      lmaxmix: str = ''

      def read_data(self,incar_file_name: str) -> None:
          file = open(incar_file_name,'r')
          readed_input = file.readlines()
          file.close()
          self.incar_file = readed_input
                   
          # Space independent flags
          for line in readed_input:
              line = line.replace(' ','')
              #line = line.replace(',',' ')
              #line = line.replace(':',' ')
              line = line.split()
              for prop in line:
                 pair = prop.split('=')
                 if len(pair)> 1:
                    if 'prec' == pair[0].lower():
                        self.prec = pair[1]
                    if 'ismear' == pair[0].lower():
                        self.ismear = int(pair[1])
                    if 'sigma' == pair[0].lower():
                        self.sigma = float(pair[1])
                    if 'encut' == pair[0].lower().replace(' ',''):
                        #print(pair)
                        self.encut = float(pair[1])
                    if 'nelm' == pair[0].lower():
                        self.nelm = int(pair[1])
                    if 'lwave' == pair[0].lower():
                        self.lwave = pair[1]
                    if 'lcharg' == pair[0].lower():
                        self.lcharg = pair[1]
                    if 'ispin' == pair[0].lower():
                        self.ispin = int(pair[1])
                    if 'ivdw' == pair[0].lower():
                        self.ivdw = int(pair[1])
                    if 'ediff' == pair[0].lower():
                        self.ediff = float(pair[1])
                    if 'nelect' == pair[0].lower():
                        self.nelect = float(pair[1])
                    if 'ldau' == pair[0].lower():
                        self.ldau = pair[1]
                    if 'ldautype' == pair[0].lower():
                        self.ldautype = int(pair[1])
                    if 'lmaxmix' == pair[0].lower():
                        self.lmaxmix = int(pair[1])

          # Space dependent flags
          for line in readed_input:
              #line = line.replace(' ','')
              #line = line.replace(',',' ')
              #line = line.replace(':',' ')
              line = line.split()
              if len(line)> 1:
                 if 'magmom' == line[0].lower():
                     self.magmom = line[2:]
                 if 'ldaul' == line[0].lower():
                     self.ldaul = line[2:]
                 if 'ldauu' == line[0].lower():
                     self.ldauu = line[2:]
                 if 'ldauj' == line[0].lower():
                    self.ldauj = line[2:] 

if __name__ == '__main__':
   incar = Outcar()
   incar.extract_information('OUTCAR')
   #print(incar)