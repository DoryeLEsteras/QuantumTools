import numpy as np

#solve ibrav != 0
# Where to put transform_lattice_parameters?
# Is used inside of the QEcalculation class
# maybe i should remove the cell_matrix properties
# complete transform to ibrav 0

def transform_to_ibrav0(ibrav:int,a:float,b:float,c:float, \
                    cosab:float,cosbc:float,cosac:float) -> np.ndarray:
    cell_matrix = np.array([])
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
        cosac:float,cosab:float,cosbc:float,celldm1:float,\
        celldm2:float,celldm3:float,celldm4:float,celldm5:float, \
        celldm6:float) -> np.ndarray: 
    if ibrav == 0 and cell_parameters_units == 'angstrom':
        return cell_matrix
    if ibrav == 0 and cell_parameters_units == 'crystal':
        return np.dot(cell_matrix,a)
    if ibrav == 0 and cell_parameters_units == 'alat':
        return np.dot(cell_matrix,a)
    if ibrav == 0 and cell_parameters_units == 'bohr':
        return np.dot(cell_matrix,celldm1)
    if ibrav != 0:
       if cell_parameters_units == 'bohr':
          a = celldm1
          b = celldm2*celldm1
          c = celldm3*celldm1
          cosac = celldm5
          cosab = celldm6
          cosbc = celldm4
    return transform_to_ibrav0(ibrav,a,b,c,cosab,cosbc,cosac)