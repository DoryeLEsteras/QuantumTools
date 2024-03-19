
import numpy as np
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict, Field
from typing import List

@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class Outcar:
      nk: int = 0
      nat: int = 0
      nmag: int = 0
      ispin: int = 0
      energy: float = 0.0
      kpoints: np.ndarray = Field(default_factory=lambda:np.array([]))
      magmom: np.ndarray = Field(default_factory=lambda:np.array([]))
      metal_magmom: np.ndarray = Field(default_factory=lambda:np.array([]))
      atomic_coordinates: np.ndarray = Field(default_factory=lambda:np.array([]))
      metalic_coordinates: np.ndarray = Field(default_factory=lambda:np.array([]))
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
                      if line[0] == 'ion' and line[1] == 'position':
                         x = ['',''];y=[]
                         while len(x) > 1:
                            x = f.readline().split()
                            if len(x) > 1:
                               y = x
                         self.nat = int(y[0])
                         magmom = np.zeros((self.nat,4))
                      if line[0] == 'magnetization' and line[1] == '(x)':
                         metal_magmomx = np.array([])
                         f.readline();f.readline();f.readline()
                         for i in range(self.nat):
                             x = f.readline().split()
                             magmom[i,0] = float(x[-1])
                             if abs(float(x[3])) > abs(float(x[2])) and abs(float(x[3])) > abs(float(x[1])) and float(x[-1] != 0):
                                metal_magmomx= np.append(metal_magmomx,float(x[-1]))
                                self.nmag = metal_magmomx.shape[0]
                                self.metal_magmom = metal_magmomx
                      if line[0] == 'magnetization' and line[1] == '(y)':
                         metal_magmomy = np.array([])
                         f.readline();f.readline();f.readline()
                         for i in range(self.nat):
                             x = f.readline().split()
                             magmom[i,1] = float(x[-1])
                             if abs(float(x[3])) > abs(float(x[2])) and abs(float(x[3])) > abs(float(x[1])) and float(x[-1] != 0):
                                metal_magmomy = np.append(metal_magmomy,float(x[-1]))
                                if np.sum(abs(metal_magmomy)) > np.sum(abs(self.metal_magmom)):
                                   self.nmag = metal_magmomy.shape[0]
                                   self.metal_magmom = metal_magmomy

                      if line[0] == 'magnetization' and line[1] == '(z)':
                         metal_magmomz = np.array([])
                         f.readline();f.readline();f.readline()
                         for i in range(self.nat):
                             x = f.readline().split()
                             magmom[i,2] = float(x[-1])
                             if abs(float(x[3])) > abs(float(x[2])) and abs(float(x[3])) > abs(float(x[1])) and float(x[-1] != 0):
                                metal_magmomz= np.append(metal_magmomz,float(x[-1]))
                                if np.sum(abs(metal_magmomz)) > np.sum(abs(self.metal_magmom)):
                                   self.nmag = metal_magmomz.shape[0]
                                   self.metal_magmom = metal_magmomz
                      
                      if line[0] == 'POSITION':
                         atomic_coordinates = np.zeros((self.nat,3))
                         f.readline()
                         for i in range(self.nat):
                             atomic_coordinates[i] = f.readline().split()[0:3]
                         self.atomic_coordinates = atomic_coordinates
                         self.metalic_coordinates = atomic_coordinates[0:self.nmag]
                         #no entiendo que unidades tienen estas coordenadas
          
          for i in range(self.nat):
              magmom[i,3] = np.linalg.norm(magmom[i,0:3])
          self.magmom = magmom[:,3]  # in this matrix hay have the moments by components
                                     # however, for now i am not interested in them
          self.metal_magmom = self.magmom[0:self.nmag]
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
   outcar = Outcar()
   outcar.extract_information('OUTCAR')
   #print(incar)