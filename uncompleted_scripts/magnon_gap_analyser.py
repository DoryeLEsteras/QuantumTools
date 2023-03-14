import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser

# TO DO LIST
"""

"""

def parser():
    parser = ArgumentParser(description="Script to disentangle the interesting bands after a fatband calculation")
    parser.add_argument("-op", "--op",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the exchange file
                        """)
    parser.add_argument("-ac", "--ac",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the exchange file
                        """)

    args = parser.parse_args()
    return args.op,args.ac

def calculate_gap(acoustic_file,optic_file):
    with open(str(acoustic_file),'r') as f:
        read_vector = np.loadtxt(f)
    max = np.max(read_vector)
    max_pos = read_vector.argmax(axis=0)
    with open(str(optic_file),'r') as f:
        read_vector = np.loadtxt(f)
    min = read_vector[max_pos]
    gap =  min - max
    #print(max,min,gap)
    print(gap)

def poli(mesh):
    with open('magnon_gap_poli.txt','w') as f:
        for x in np.arange(95,105+mesh,mesh):
            strain_label = x - 100
            gap = -0.000266806527*strain_label*strain_label*strain_label*strain_label- 0.000996775447*strain_label*strain_label*strain_label + 0.010554079254*strain_label*strain_label + 0.049538966589*strain_label + 0.625361678322
            f.write(str(strain_label) + " " + str(gap) +'\n') # esto ha reventado al poner el nuevo poli que incluia 95 y 105
mesh = 0.001
optic_file,acoustic_file = parser()
#calculate_gap(acoustic_file,optic_file)
poli(mesh)
 