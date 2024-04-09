import numpy as np

def orient_magnetic_moment(scalar_magnetic_moments,direction):
    magnetic_moment_vector = []
    if direction == 'x':
       for i in scalar_magnetic_moments:
           magnetic_moment_vector.append([i,0,0])
    if direction == 'y':
       for i in scalar_magnetic_moments:
           magnetic_moment_vector.append([0,i,0])
    if direction == 'z':
       for i in scalar_magnetic_moments:
           magnetic_moment_vector.append([0,0,i])
    magnetic_moment_vector = np.array(magnetic_moment_vector)
    return magnetic_moment_vector