import numpy as np
from argparse import ArgumentParser

# TO DO LIST
"""
    
"""
def parser():
    parser = ArgumentParser(description="Script to fix the matrices of Gaussian")
    parser.add_argument("-input", "--input",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the exchange file
                        """)
    parser.add_argument("-out", "--out",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the output file
                        """)     
    args = parser.parse_args()
    return args.input,args.out,

def manage_input_files(input_file):
    counter = 0
    read_vector = input_file.readlines()
    for line in read_vector:
        readed_line = line.replace(';', '')
        readed_line = readed_line.split()
        readed_line.append('end')

        if readed_line[0] == 'J1' and readed_line[1] == 'iso':
            J1iso = readed_line[3]
        if readed_line[0] == 'J2' and readed_line[1] == 'iso':
            J2iso = readed_line[3]
        if readed_line[0] == 'J3' and readed_line[1] == 'iso':
            J3iso = readed_line[3]
        if readed_line[0] == 'J1' and readed_line[1] == 'orb': 
            J1_1 = read_vector[counter+1]
            J1_1  = J1_1.split()
            J1_2 = read_vector[counter+2]
            J1_2  = J1_2.split()
            J1_3 = read_vector[counter+3]
            J1_3  = J1_3.split()
            J1_4 = read_vector[counter+4]
            J1_4  = J1_4.split()
            J1_5 = read_vector[counter+5]
            J1_5  = J1_5.split()
            J1_t2g_t2g = float(J1_2[1]) + float(J1_2[2]) + float(J1_2[4]) +  float(J1_3[1]) + float(J1_3[2]) + float(J1_3[4]) + float(J1_5[1]) + float(J1_5[2]) + float(J1_5[4]) 
            J1_t2g_eg = float(J1_1[1]) + float(J1_1[2]) + float(J1_1[4]) + float(J1_2[0]) + float(J1_2[3]) + float(J1_3[0]) + float(J1_3[3]) + float(J1_4[1]) + float(J1_4[2]) + float(J1_4[4]) + float(J1_5[0]) + float(J1_5[3])
            J1_eg_eg = float(J1_1[0]) + float(J1_1[3]) + float(J1_4[0]) + float(J1_4[3])
        if readed_line[0] == 'J2' and readed_line[1] == 'orb': 
            J2_1 = read_vector[counter+1].split()
            J2_2 = read_vector[counter+2].split()
            J2_3 = read_vector[counter+3].split()
            J2_4 = read_vector[counter+4].split()
            J2_5 = read_vector[counter+5].split()
            J2_t2g_t2g = float(J2_2[1]) + float(J2_2[2]) + float(J2_2[4]) +  float(J2_3[1]) + float(J2_3[2]) + float(J2_3[4]) + float(J2_5[1]) + float(J2_5[2]) + float(J2_5[4]) 
            J2_t2g_eg = float(J2_1[1]) + float(J2_1[2]) + float(J2_1[4]) + float(J2_2[0]) + float(J2_2[3]) + float(J2_3[0]) + float(J2_3[3]) + float(J2_4[1]) + float(J2_4[2]) + float(J2_4[4]) + float(J2_5[0]) + float(J2_5[3])
            J2_eg_eg = float(J2_1[0]) + float(J2_1[3]) + float(J2_4[0]) + float(J2_4[3])
        if readed_line[0] == 'J3' and readed_line[1] == 'orb': 
            J3_1 = read_vector[counter+1].split()
            J3_2 = read_vector[counter+2].split()
            J3_3 = read_vector[counter+3].split()
            J3_4 = read_vector[counter+4].split()
            J3_5 = read_vector[counter+5].split()
            J3_t2g_t2g = float(J3_2[1]) + float(J3_2[2]) + float(J3_2[4]) +  float(J3_3[1]) + float(J3_3[2]) + float(J3_3[4]) + float(J3_5[1]) + float(J3_5[2]) + float(J3_5[4]) 
            J3_t2g_eg = float(J3_1[1]) + float(J3_1[2]) + float(J3_1[4]) + float(J3_2[0]) + float(J3_2[3]) + float(J3_3[0]) + float(J3_3[3]) + float(J3_4[1]) + float(J3_4[2]) + float(J3_4[4]) + float(J3_5[0]) + float(J3_5[3])
            J3_eg_eg = float(J3_1[0]) + float(J3_1[3]) + float(J3_4[0]) + float(J3_4[3])
        counter = counter + 1 
    return J1_t2g_t2g, J2_t2g_t2g, J3_t2g_t2g,J1_t2g_eg, J2_t2g_eg, J3_t2g_eg,J1_eg_eg, J2_eg_eg, J3_eg_eg



provided_input_file,provided_output_file = parser()
input_file = open(str(provided_input_file), 'r')
output_file = open(str(provided_output_file), 'w')

for U in range()
manage_input_files(input_file)






