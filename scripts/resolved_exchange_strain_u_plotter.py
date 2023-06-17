#!/usr/bin/python3
import numpy as np
from argparse import ArgumentParser
import matplotlib.pyplot as plt

# TO DO LIST
"""
- Add more plots according to necessities 
"""
def parser():
    parser = ArgumentParser(description="Script to extract and plot exchange parameters")
    parser.add_argument("-outdir", "--outdir",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the output file
                        """)   
    parser.add_argument("-inputdir", "--inputdir",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the input file
                        """)      
    args = parser.parse_args()
    return args.inputdir,args.outdir
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
            J1_t2g_t2g = float(J1_2[1]) + float(J1_2[2]) + float(J1_2[4]) + \
                + float(J1_3[1]) + float(J1_3[2]) + float(J1_3[4]) + \
                + float(J1_5[1]) + float(J1_5[2]) + float(J1_5[4]) 
            J1_t2g_eg = float(J1_1[1]) + float(J1_1[2]) + float(J1_1[4]) + \
                + float(J1_2[0]) + float(J1_2[3]) + float(J1_3[0]) + \
                + float(J1_3[3]) + float(J1_4[1]) + float(J1_4[2]) + \
                + float(J1_4[4]) + float(J1_5[0]) + float(J1_5[3])
            J1_eg_eg = float(J1_1[0]) + float(J1_1[3]) + \
                + float(J1_4[0]) + float(J1_4[3])
            J1_dz2_dz2 = float(J1_1[0]) 
            J1_x2y2_x2y2 = float(J1_4[3])
            J1_dxz_dxz = float(J1_2[1])
            J1_dyz_dyz = float(J1_3[2])
            J1_dxy_dxy = float(J1_5[4])
            J1_dz2_dxz =  float(J1_1[1]) + float(J1_2[0])
            J1_dz2_dyz = float(J1_1[2]) + float(J1_3[0])
            J1_dz2_dx2y2 = float(J1_4[0]) + float(J1_1[3])
            J1_dz2_dxy = float(J1_1[4]) + float(J1_5[0])
            J1_dxz_dyz =  float(J1_2[2]) + float(J1_3[1])
            J1_dxz_dx2y2 = float(J1_2[3]) + float(J1_4[1])
            J1_dxz_dxy = float(J1_5[1]) + float(J1_2[4])
            J1_dyz_dxy = float(J1_3[4]) + float(J1_5[2]) 
            J1_dyz_dx2y2 = float(J1_4[2]) + float(J1_3[3])
            J1_dxy_dx2y2 = float(J1_5[3]) + float(J1_4[4])
        if readed_line[0] == 'J2' and readed_line[1] == 'orb': 
            J2_1 = read_vector[counter+1].split()
            J2_2 = read_vector[counter+2].split()
            J2_3 = read_vector[counter+3].split()
            J2_4 = read_vector[counter+4].split()
            J2_5 = read_vector[counter+5].split()
            J2_t2g_t2g = float(J2_2[1]) + float(J2_2[2]) + float(J2_2[4]) +  \
                + float(J2_3[1]) + float(J2_3[2]) + float(J2_3[4]) + \
                + float(J2_5[1]) + float(J2_5[2]) + float(J2_5[4]) 
            J2_t2g_eg = float(J2_1[1]) + float(J2_1[2]) + float(J2_1[4]) + \
                + float(J2_2[0]) + float(J2_2[3]) + float(J2_3[0]) + \
                + float(J2_3[3]) + float(J2_4[1]) + float(J2_4[2]) + \
                + float(J2_4[4]) + float(J2_5[0]) + float(J2_5[3])
            J2_eg_eg = float(J2_1[0]) + float(J2_1[3]) + \
                + float(J2_4[0]) + float(J2_4[3])
            J2_dz2_dz2 = float(J2_1[0]) 
            J2_x2y2_x2y2 = float(J2_4[3])
            J2_dxz_dxz = float(J2_2[1])
            J2_dyz_dyz = float(J2_3[2])
            J2_dxy_dxy = float(J2_5[4])
            J2_dz2_dxz =  float(J2_1[1]) + float(J2_2[0])
            J2_dz2_dyz = float(J2_1[2]) + float(J2_3[0])
            J2_dz2_dx2y2 = float(J2_4[0]) + float(J2_1[3])
            J2_dz2_dxy = float(J2_1[4]) + float(J2_5[0])
            J2_dxz_dyz =  float(J2_2[2]) + float(J2_3[1])
            J2_dxz_dx2y2 = float(J2_2[3]) + float(J2_4[1])
            J2_dxz_dxy = float(J2_5[1]) + float(J2_2[4])
            J2_dyz_dxy = float(J2_3[4]) + float(J2_5[2]) 
            J2_dyz_dx2y2 = float(J2_4[2]) + float(J2_3[3])
            J2_dxy_dx2y2 = float(J2_5[3]) + float(J2_4[4])
        if readed_line[0] == 'J3' and readed_line[1] == 'orb': 
            J3_1 = read_vector[counter+1].split()
            J3_2 = read_vector[counter+2].split()
            J3_3 = read_vector[counter+3].split()
            J3_4 = read_vector[counter+4].split()
            J3_5 = read_vector[counter+5].split()
            J3_t2g_t2g = float(J3_2[1]) + float(J3_2[2]) + float(J3_2[4]) +  \
                + float(J3_3[1]) + float(J3_3[2]) + float(J3_3[4]) +  \
                +  float(J3_5[1]) + float(J3_5[2]) + float(J3_5[4]) 
            J3_t2g_eg = float(J3_1[1]) + float(J3_1[2]) + float(J3_1[4]) +  \
                + float(J3_2[0]) + float(J3_2[3]) + float(J3_3[0]) +  \
                + float(J3_3[3]) + float(J3_4[1]) + float(J3_4[2]) +  \
                + float(J3_4[4]) + float(J3_5[0]) + float(J3_5[3])
            J3_eg_eg = float(J3_1[0]) + float(J3_1[3]) +  \
                + float(J3_4[0]) + float(J3_4[3])
            J3_dz2_dz2 = float(J3_1[0]) 
            J3_x2y2_x2y2 = float(J3_4[3])
            J3_dxz_dxz = float(J3_2[1])
            J3_dyz_dyz = float(J3_3[2])
            J3_dxy_dxy = float(J3_5[4])
            J3_dz2_dxz =  float(J3_1[1]) + float(J3_2[0])
            J3_dz2_dyz = float(J3_1[2]) + float(J3_3[0])
            J3_dz2_dx2y2 = float(J3_4[0]) + float(J3_1[3])
            J3_dz2_dxy = float(J3_1[4]) + float(J3_5[0])
            J3_dxz_dyz =  float(J3_2[2]) + float(J3_3[1])
            J3_dxz_dx2y2 = float(J3_2[3]) + float(J3_4[1])
            J3_dxz_dxy = float(J3_5[1]) + float(J3_2[4])
            J3_dyz_dxy = float(J3_3[4]) + float(J3_5[2]) 
            J3_dyz_dx2y2 = float(J3_4[2]) + float(J3_3[3])
            J3_dxy_dx2y2 = float(J3_5[3]) + float(J3_4[4])
        counter = counter + 1 
    return J1iso,J2iso,J3iso,J1_t2g_t2g, J2_t2g_t2g, J3_t2g_t2g,J1_t2g_eg,\
       J2_t2g_eg, J3_t2g_eg,J1_eg_eg, J2_eg_eg, J3_eg_eg,J1_dz2_dz2,\
       J1_x2y2_x2y2, J1_dxz_dxz,J1_dyz_dyz, J1_dxy_dxy, J1_dz2_dxz,\
       J1_dz2_dyz, J1_dz2_dx2y2,J1_dz2_dxy, J1_dxz_dyz, J1_dxz_dx2y2,\
       J1_dxz_dxy, J1_dyz_dxy, J1_dyz_dx2y2, J1_dxy_dx2y2,J2_dz2_dz2,\
       J2_x2y2_x2y2, J2_dxz_dxz,J2_dyz_dyz, J2_dxy_dxy, J2_dz2_dxz,\
       J2_dz2_dyz, J2_dz2_dx2y2,J2_dz2_dxy, J2_dxz_dyz, J2_dxz_dx2y2,\
       J2_dxz_dxy, J2_dyz_dxy, J2_dyz_dx2y2, J2_dxy_dx2y2,J3_dz2_dz2,\
       J3_x2y2_x2y2, J3_dxz_dxz,J3_dyz_dyz, J3_dxy_dxy, J3_dz2_dxz,\
       J3_dz2_dyz, J3_dz2_dx2y2,J3_dz2_dxy, J3_dxz_dyz, J3_dxz_dx2y2,\
       J3_dxz_dxy, J3_dyz_dxy, J3_dyz_dx2y2, J3_dxy_dx2y2
def create_J_vs_U_file(prefix,Umax,Umin,Unstep,strmax,strmin,strnstep,output_dir):
    for strain in np.arange(strmin,strmax+strnstep,strnstep):
        strain_file_name = str(output_dir) + '/' + prefix + '.resolved_exchange_' + \
                           str(strain) + '_strain' + '_vsU.txt'
        strain_output_file = open(strain_file_name, 'w')
        strain_output_file.write('U' + ' ' + 'J1iso' + ' ' + 'J2iso' + ' ' + 'J3iso' + ' ' + \
            'J1_t2g_t2g' + ' ' +  'J2_t2g_t2g' + ' ' +  'J3_t2g_t2g' + ' '     + \
            'J1_t2g_eg' + ' ' + 'J2_t2g_eg' + ' ' +  'J3_t2g_eg' + ' '         + \
            'J1_eg_eg' + ' ' +  'J2_eg_eg' + ' ' +  'J3_eg_eg' + ' ' + \
            'J1_dz2_dz2' + ' ' + 'J1_x2y2_x2y2' + ' ' +  'J1_dxz_dxz' + ' ' + \
            'J1_dyz_dyz' + ' ' +  'J1_dxy_dxy' + ' ' +  'J1_dz2_dxz' + ' ' + \
            'J1_dz2_dyz' + ' ' +  'J1_dz2_dx2y2' + ' ' + 'J1_dz2_dxy' + ' ' + \
            'J1_dxz_dyz' + ' ' +  'J1_dxz_dx2y2' + ' ' + 'J1_dxz_dxy' + ' ' +  \
            'J1_dyz_dxy' + ' ' +  'J1_dyz_dx2y2' + ' ' +  'J1_dxy_dx2y2' + ' ' + \
            'J2_dz2_dz2' + ' ' + 'J2_x2y2_x2y2' + ' ' +  'J2_dxz_dxz' + ' ' + \
            'J2_dyz_dyz' + ' ' +  'J2_dxy_dxy' + ' ' +  'J2_dz2_dxz' + ' ' + \
            'J2_dz2_dyz' + ' ' +  'J2_dz2_dx2y2' + ' ' + 'J2_dz2_dxy' + ' ' + \
            'J2_dxz_dyz' + ' ' +  'J2_dxz_dx2y2' + ' ' + 'J2_dxz_dxy' + ' ' + \
            'J2_dyz_dxy' + ' ' +  'J2_dyz_dx2y2' + ' ' +  'J2_dxy_dx2y2' + ' ' + \
            'J3_dz2_dz2' + ' ' + 'J3_x2y2_x2y2' + ' ' +  'J3_dxz_dxz' + ' ' + \
            'J3_dyz_dyz' + ' ' +  'J3_dxy_dxy' + ' ' +  'J3_dz2_dxz' + ' ' + \
           'J3_dz2_dyz' + ' ' +  'J3_dz2_dx2y2' + ' ' + 'J3_dz2_dxy' + ' ' +  \
           'J3_dxz_dyz' + ' ' +  'J3_dxz_dx2y2' + ' ' + 'J3_dxz_dxy' + ' ' + \
           'J3_dyz_dxy' + ' ' +  'J3_dyz_dx2y2' + ' ' +  'J3_dxy_dx2y2' + '\n')
        for U in np.arange(Umin,Umax+Unstep,Unstep):
            input_name = 'exchange.' + str(prefix) + '.' + str(strain) + '.' + str(U)
            input_file = open(input_dir+ '/' +input_name, 'r')
            J1iso,J2iso,J3iso,J1_t2g_t2g, J2_t2g_t2g, J3_t2g_t2g,J1_t2g_eg,\
                J2_t2g_eg, J3_t2g_eg,J1_eg_eg, J2_eg_eg, J3_eg_eg,J1_dz2_dz2,\
                J1_x2y2_x2y2, J1_dxz_dxz,J1_dyz_dyz, J1_dxy_dxy, J1_dz2_dxz,\
                J1_dz2_dyz, J1_dz2_dx2y2,J1_dz2_dxy, J1_dxz_dyz, J1_dxz_dx2y2,\
                J1_dxz_dxy, J1_dyz_dxy, J1_dyz_dx2y2, J1_dxy_dx2y2,J2_dz2_dz2,\
                J2_x2y2_x2y2, J2_dxz_dxz,J2_dyz_dyz, J2_dxy_dxy, J2_dz2_dxz,\
                J2_dz2_dyz, J2_dz2_dx2y2,J2_dz2_dxy, J2_dxz_dyz, J2_dxz_dx2y2,\
                J2_dxz_dxy, J2_dyz_dxy, J2_dyz_dx2y2, J2_dxy_dx2y2,J3_dz2_dz2,\
                J3_x2y2_x2y2, J3_dxz_dxz,J3_dyz_dyz, J3_dxy_dxy, J3_dz2_dxz,\
                J3_dz2_dyz, J3_dz2_dx2y2,J3_dz2_dxy, J3_dxz_dyz, J3_dxz_dx2y2,\
                J3_dxz_dxy, J3_dyz_dxy, J3_dyz_dx2y2, J3_dxy_dx2y2 \
                = manage_input_files(input_file)   
            input_file.close()
            strain_output_file.write(str(U) + ' ' + str(J1iso) + ' ' + str(J2iso) + ' ' + \
                 str(J3iso) + ' ' + str(J1_t2g_t2g) + ' ' +  str(J2_t2g_t2g) + \
                 ' ' +  str(J3_t2g_t2g) + ' ' + str(J1_t2g_eg) + ' ' + \
                 str(J2_t2g_eg) + ' ' +  str(J3_t2g_eg) + ' ' + str(J1_eg_eg) +\
                 ' ' +  str(J2_eg_eg) + ' ' +  str(J3_eg_eg) + ' ' + \
                 str(J1_dz2_dz2) + ' ' + str(J1_x2y2_x2y2) + ' ' +  \
                 str(J1_dxz_dxz) + ' ' + str(J1_dyz_dyz) + ' ' +  \
                 str(J1_dxy_dxy) + ' ' +  str(J1_dz2_dxz) + ' ' + \
                 str(J1_dz2_dyz) + ' ' +  str(J1_dz2_dx2y2) + ' ' + \
                 str(J1_dz2_dxy) + ' ' +  str(J1_dxz_dyz) + ' ' +  \
                 str(J1_dxz_dx2y2) + ' ' + str(J1_dxz_dxy) + ' ' +  \
                 str(J1_dyz_dxy) + ' ' +  str(J1_dyz_dx2y2) + ' ' + \
                 str(J1_dxy_dx2y2) + ' ' + str(J2_dz2_dz2) + ' ' + \
                 str(J2_x2y2_x2y2) + ' ' +  str(J2_dxz_dxz) + ' ' + \
                 str(J2_dyz_dyz) + ' ' +  str(J2_dxy_dxy) + ' ' + \
                 str(J2_dz2_dxz) + ' ' + str(J2_dz2_dyz) + ' ' +  \
                 str(J2_dz2_dx2y2) + ' ' + str(J2_dz2_dxy) + ' ' +  \
                 str(J2_dxz_dyz) + ' ' +  str(J2_dxz_dx2y2) + ' ' + \
                 str(J2_dxz_dxy) + ' ' +  str(J2_dyz_dxy) + ' ' +  \
                 str(J2_dyz_dx2y2) + ' ' +  str(J2_dxy_dx2y2) + ' ' + \
                 str(J3_dz2_dz2) + ' ' + str(J3_x2y2_x2y2) + ' ' +  \
                 str(J3_dxz_dxz) + ' ' + str(J3_dyz_dyz) + ' ' +  \
                 str(J3_dxy_dxy) + ' ' +  str(J3_dz2_dxz) + ' ' + \
                 str(J3_dz2_dyz) + ' ' +  str(J3_dz2_dx2y2) + ' ' + \
                 str(J3_dz2_dxy) + ' ' +  str(J3_dxz_dyz) + ' ' +  \
                 str(J3_dxz_dx2y2) + ' ' + str(J3_dxz_dxy) + ' ' +  \
                 str(J3_dyz_dxy) + ' ' +  str(J3_dyz_dx2y2) + ' ' +  \
                 str(J3_dxy_dx2y2)+ '\n') 
        strain_output_file.close()
        plot_total(strain_file_name,output_dir,'strain')
        plotter(strain_file_name,output_dir,'U')
def create_J_vs_strain_file(prefix,Umax,Umin,Unstep,strmax,strmin,strnstep,output_dir):
    matrix_to_plot_tablesJ1 = np.zeros((int((strmax+1-strmin)/strnstep),5,5))
    matrix_to_plot_tablesJ2 = np.zeros((int((strmax+1-strmin)/strnstep),5,5))
    matrix_to_plot_tablesJ3 = np.zeros((int((strmax+1-strmin)/strnstep),5,5))
    for U in np.arange(Umin,Umax+Unstep,Unstep):
        U_file_name = str(output_dir) + '/' + prefix + '.resolved_exchange_' + \
                           str(U) + '_U' + '_vs_strain.txt'
        U_output_file = open(U_file_name, 'w')
        U_output_file.write('strain' + 'J1iso' + ' ' + 'J2iso' + ' ' + 'J3iso' + ' ' + \
            'J1_t2g_t2g' + ' ' +  'J2_t2g_t2g' + ' ' +  'J3_t2g_t2g' + ' '     + \
            'J1_t2g_eg' + ' ' + 'J2_t2g_eg' + ' ' +  'J3_t2g_eg' + ' '         + \
            'J1_eg_eg' + ' ' +  'J2_eg_eg' + ' ' +  'J3_eg_eg' + ' ' + \
            'J1_dz2_dz2' + ' ' + 'J1_x2y2_x2y2' + ' ' +  'J1_dxz_dxz' + ' ' + \
            'J1_dyz_dyz' + ' ' +  'J1_dxy_dxy' + ' ' +  'J1_dz2_dxz' + ' ' + \
            'J1_dz2_dyz' + ' ' +  'J1_dz2_dx2y2' + ' ' + 'J1_dz2_dxy' + ' ' + \
            'J1_dxz_dyz' + ' ' +  'J1_dxz_dx2y2' + ' ' + 'J1_dxz_dxy' + ' ' +  \
            'J1_dyz_dxy' + ' ' +  'J1_dyz_dx2y2' + ' ' +  'J1_dxy_dx2y2' + ' ' + \
            'J2_dz2_dz2' + ' ' + 'J2_x2y2_x2y2' + ' ' +  'J2_dxz_dxz' + ' ' + \
            'J2_dyz_dyz' + ' ' +  'J2_dxy_dxy' + ' ' +  'J2_dz2_dxz' + ' ' + \
            'J2_dz2_dyz' + ' ' +  'J2_dz2_dx2y2' + ' ' + 'J2_dz2_dxy' + ' ' + \
            'J2_dxz_dyz' + ' ' +  'J2_dxz_dx2y2' + ' ' + 'J2_dxz_dxy' + ' ' + \
            'J2_dyz_dxy' + ' ' +  'J2_dyz_dx2y2' + ' ' +  'J2_dxy_dx2y2' + ' ' + \
            'J3_dz2_dz2' + ' ' + 'J3_x2y2_x2y2' + ' ' +  'J3_dxz_dxz' + ' ' + \
            'J3_dyz_dyz' + ' ' +  'J3_dxy_dxy' + ' ' +  'J3_dz2_dxz' + ' ' + \
           'J3_dz2_dyz' + ' ' +  'J3_dz2_dx2y2' + ' ' + 'J3_dz2_dxy' + ' ' +  \
           'J3_dxz_dyz' + ' ' +  'J3_dxz_dx2y2' + ' ' + 'J3_dxz_dxy' + ' ' + \
           'J3_dyz_dxy' + ' ' +  'J3_dyz_dx2y2' + ' ' +  'J3_dxy_dx2y2' + '\n')
        counter = 0
        for strain in np.arange(strmin,strmax+strnstep,strnstep):   
            input_name = 'exchange.' + str(prefix) + '.' + str(strain) + '.' + str(U)
            input_file = open(input_dir+ '/' +input_name, 'r')
            J1iso,J2iso,J3iso,J1_t2g_t2g, J2_t2g_t2g, J3_t2g_t2g,J1_t2g_eg,\
                J2_t2g_eg, J3_t2g_eg,J1_eg_eg, J2_eg_eg, J3_eg_eg,J1_dz2_dz2,\
                J1_x2y2_x2y2, J1_dxz_dxz,J1_dyz_dyz, J1_dxy_dxy, J1_dz2_dxz,\
                J1_dz2_dyz, J1_dz2_dx2y2,J1_dz2_dxy, J1_dxz_dyz, J1_dxz_dx2y2,\
                J1_dxz_dxy, J1_dyz_dxy, J1_dyz_dx2y2, J1_dxy_dx2y2,J2_dz2_dz2,\
                J2_x2y2_x2y2, J2_dxz_dxz,J2_dyz_dyz, J2_dxy_dxy, J2_dz2_dxz,\
                J2_dz2_dyz, J2_dz2_dx2y2,J2_dz2_dxy, J2_dxz_dyz, J2_dxz_dx2y2,\
                J2_dxz_dxy, J2_dyz_dxy, J2_dyz_dx2y2, J2_dxy_dx2y2,J3_dz2_dz2,\
                J3_x2y2_x2y2, J3_dxz_dxz,J3_dyz_dyz, J3_dxy_dxy, J3_dz2_dxz,\
                J3_dz2_dyz, J3_dz2_dx2y2,J3_dz2_dxy, J3_dxz_dyz, J3_dxz_dx2y2,\
                J3_dxz_dxy, J3_dyz_dxy, J3_dyz_dx2y2, J3_dxy_dx2y2 \
                = manage_input_files(input_file)  
            
            matrix_to_plot_tablesJ1[counter,:,:] = [\
                [J1_dz2_dz2,J1_dz2_dxz,J1_dz2_dyz,J1_dz2_dx2y2,J1_dz2_dxy], \
                [J1_dz2_dxz,J1_dxz_dxz,J1_dxz_dyz,J1_dxz_dx2y2,J1_dxz_dxy],\
                [J1_dz2_dyz,J1_dxz_dyz,J1_dyz_dyz,J1_dyz_dx2y2,J1_dyz_dxy],\
                [J1_dz2_dx2y2,J1_dxz_dx2y2,J1_dyz_dx2y2,J1_x2y2_x2y2,J1_dxy_dx2y2],\
                [J1_dz2_dxy,J1_dxz_dxy,J1_dyz_dxy,J1_dxy_dx2y2,J1_dxy_dxy]
            ]
            matrix_to_plot_tablesJ2[counter,:,:] = [
                [J2_dz2_dz2,J2_dz2_dxz,J2_dz2_dyz,J2_dz2_dx2y2,J2_dz2_dxy],
                [J2_dz2_dxz,J2_dxz_dxz,J2_dxz_dyz,J2_dxz_dx2y2,J2_dxz_dxy],
                [J2_dz2_dyz,J2_dxz_dyz,J2_dyz_dyz,J2_dyz_dx2y2,J2_dyz_dxy],
                [J2_dz2_dx2y2,J2_dxz_dx2y2,J2_dyz_dx2y2,J2_x2y2_x2y2,J2_dxy_dx2y2],
                [J2_dz2_dxy,J2_dxz_dxy,J2_dyz_dxy,J2_dxy_dx2y2,J2_dxy_dxy]
            ]
            matrix_to_plot_tablesJ3[counter,:,:] = [
                [J3_dz2_dz2,J3_dz2_dxz,J3_dz2_dyz,J3_dz2_dx2y2,J3_dz2_dxy],
                [J3_dz2_dxz,J3_dxz_dxz,J3_dxz_dyz,J3_dxz_dx2y2,J3_dxz_dxy],
                [J3_dz2_dyz,J3_dxz_dyz,J3_dyz_dyz,J3_dyz_dx2y2,J3_dyz_dxy],
                [J3_dz2_dx2y2,J3_dxz_dx2y2,J3_dyz_dx2y2,J3_x2y2_x2y2,J3_dxy_dx2y2],
                [J3_dz2_dxy,J3_dxz_dxy,J3_dyz_dxy,J3_dxy_dx2y2,J3_dxy_dxy]
            ]
            input_file.close()
            U_output_file.write(str(strain) + ' ' + str(J1iso) + ' ' + str(J2iso) +\
                 ' ' + str(J3iso) + ' ' + str(J1_t2g_t2g) + ' ' +  str(J2_t2g_t2g) + \
                 ' ' +  str(J3_t2g_t2g) + ' ' + str(J1_t2g_eg) + ' ' + \
                 str(J2_t2g_eg) + ' ' +  str(J3_t2g_eg) + ' ' + str(J1_eg_eg) +\
                 ' ' +  str(J2_eg_eg) + ' ' +  str(J3_eg_eg) + ' ' + \
                 str(J1_dz2_dz2) + ' ' + str(J1_x2y2_x2y2) + ' ' +  \
                 str(J1_dxz_dxz) + ' ' + str(J1_dyz_dyz) + ' ' +  \
                 str(J1_dxy_dxy) + ' ' +  str(J1_dz2_dxz) + ' ' + \
                 str(J1_dz2_dyz) + ' ' +  str(J1_dz2_dx2y2) + ' ' + \
                 str(J1_dz2_dxy) + ' ' +  str(J1_dxz_dyz) + ' ' +  \
                 str(J1_dxz_dx2y2) + ' ' + str(J1_dxz_dxy) + ' ' +  \
                 str(J1_dyz_dxy) + ' ' +  str(J1_dyz_dx2y2) + ' ' + \
                 str(J1_dxy_dx2y2) + ' ' + str(J2_dz2_dz2) + ' ' + \
                 str(J2_x2y2_x2y2) + ' ' +  str(J2_dxz_dxz) + ' ' + \
                 str(J2_dyz_dyz) + ' ' +  str(J2_dxy_dxy) + ' ' + \
                 str(J2_dz2_dxz) + ' ' + str(J2_dz2_dyz) + ' ' +  \
                 str(J2_dz2_dx2y2) + ' ' + str(J2_dz2_dxy) + ' ' +  \
                 str(J2_dxz_dyz) + ' ' +  str(J2_dxz_dx2y2) + ' ' + \
                 str(J2_dxz_dxy) + ' ' +  str(J2_dyz_dxy) + ' ' +  \
                 str(J2_dyz_dx2y2) + ' ' +  str(J2_dxy_dx2y2) + ' ' + \
                 str(J3_dz2_dz2) + ' ' + str(J3_x2y2_x2y2) + ' ' +  \
                 str(J3_dxz_dxz) + ' ' + str(J3_dyz_dyz) + ' ' +  \
                 str(J3_dxy_dxy) + ' ' +  str(J3_dz2_dxz) + ' ' + \
                 str(J3_dz2_dyz) + ' ' +  str(J3_dz2_dx2y2) + ' ' + \
                 str(J3_dz2_dxy) + ' ' +  str(J3_dxz_dyz) + ' ' +  \
                 str(J3_dxz_dx2y2) + ' ' + str(J3_dxz_dxy) + ' ' +  \
                 str(J3_dyz_dxy) + ' ' +  str(J3_dyz_dx2y2) + ' ' +  \
                 str(J3_dxy_dx2y2)+ '\n') 
            counter = counter + 1
        for index1 in range(0,counter,1):
            for index2 in range(0,5,1):
                for index3 in range(0,5,1):
                    if index2 != index3:     
                        matrix_to_plot_tablesJ1[index1,index2,index3] \
                            = matrix_to_plot_tablesJ1[index1,index2,index3]/2
                        matrix_to_plot_tablesJ2[index1,index2,index3] \
                            = matrix_to_plot_tablesJ2[index1,index2,index3]/2
                        matrix_to_plot_tablesJ3[index1,index2,index3] \
                            = matrix_to_plot_tablesJ3[index1,index2,index3]/2
        U_output_file.close()
        plot_total(U_file_name,output_dir,'Strain')
        plot_resolved(U_file_name,output_dir,'Strain')
        print(matrix_to_plot_tablesJ1)
    return matrix_to_plot_tablesJ1,matrix_to_plot_tablesJ2,matrix_to_plot_tablesJ3
def plotter_panel_debug(data_file,output_dir,xaxis_name):
    x_axis = np.loadtxt(data_file, skiprows=1)[:, 0]
    J1 = np.loadtxt(data_file, skiprows=1)[:, 1]
    J2 = np.loadtxt(data_file, skiprows=1)[:, 2]
    J3 = np.loadtxt(data_file, skiprows=1)[:, 3]
    J1tt = np.loadtxt(data_file, skiprows=1)[:, 4]
    J2tt= np.loadtxt(data_file, skiprows=1)[:, 5]
    J3tt = np.loadtxt(data_file, skiprows=1)[:, 6]
    J1te= np.loadtxt(data_file, skiprows=1)[:, 7]
    J2te = np.loadtxt(data_file, skiprows=1)[:, 8]
    J3te= np.loadtxt(data_file, skiprows=1)[:, 9]
    J1ee = np.loadtxt(data_file, skiprows=1)[:, 10]
    J2ee= np.loadtxt(data_file, skiprows=1)[:, 11]
    J3ee = np.loadtxt(data_file, skiprows=1)[:, 12]
    figsimple,ax = plt.subplots() 
    ax.plot(x_axis,J1,'bo')
    plt.savefig(output_dir + 'simple_panel_' + xaxis_name + '.png')
    fig,axs = plt.subplots(4,3,figsize=[20,15]) 
    plt.tight_layout() #avoid overlaps
    axs[0,0].plot(x_axis,J1,'bo')
    axs[0,0].set_title('J1 Total')
    axs[0,1].plot(x_axis,J2,'bo')
    axs[0,1].set_title('J2 Total')
    axs[0,2].plot(x_axis,J3,'bo')
    axs[0,2].set_title('J3 Total')
    axs[1,0].plot(x_axis,J1tt,'bo')
    axs[1,0].set_title('J1 t2g-t2g')
    axs[1,1].plot(x_axis,J2tt,'bo')
    axs[1,1].set_title('J2 t2g-t2g')
    axs[1,2].plot(x_axis,J3tt,'bo')
    axs[1,2].set_title('J3 t2g-t2g')
    axs[2,0].plot(x_axis,J1te,'bo')
    axs[2,0].set_title('J1 t2g-eg')
    axs[2,1].plot(x_axis,J2te,'bo')
    axs[2,1].set_title('J2 t2g-eg')
    axs[2,2].plot(x_axis,J3te,'bo')
    axs[2,2].set_title('J3 t2g-eg')
    axs[3,0].plot(x_axis,J1ee,'bo')
    axs[3,0].set_title('J1 eg-eg')
    axs[3,1].plot(x_axis,J2ee,'bo')
    axs[3,1].set_title('J2 eg-eg')
    axs[3,2].plot(x_axis,J3ee,'bo')
    axs[3,2].set_title('J3 eg-eg')
    plt.savefig(output_dir + 'full_panel_' + xaxis_name + '.png')
def plot_resolved(data_file,output_dir,label):
    x_axis = np.loadtxt(data_file, skiprows=1)[:, 0]
    J1iso= np.loadtxt(data_file, skiprows=1)[:, 1]
    J2iso= np.loadtxt(data_file, skiprows=1)[:, 2]
    J3iso= np.loadtxt(data_file, skiprows=1)[:, 3]
    J1tt = np.loadtxt(data_file, skiprows=1)[:, 4]
    J2tt= np.loadtxt(data_file, skiprows=1)[:, 5]
    J3tt = np.loadtxt(data_file, skiprows=1)[:, 6]
    J1te= np.loadtxt(data_file, skiprows=1)[:, 7]
    J2te = np.loadtxt(data_file, skiprows=1)[:, 8]
    J3te= np.loadtxt(data_file, skiprows=1)[:, 9]
    J1ee = np.loadtxt(data_file, skiprows=1)[:, 10]
    J2ee= np.loadtxt(data_file, skiprows=1)[:, 11]
    J3ee = np.loadtxt(data_file, skiprows=1)[:, 12]
    J1_dz2_dz2 = np.loadtxt(data_file, skiprows=1)[:, 13]
    J1_x2y2_x2y2 = np.loadtxt(data_file, skiprows=1)[:, 14]
    J1_dxz_dxz = np.loadtxt(data_file, skiprows=1)[:, 15]
    J1_dyz_dyz = np.loadtxt(data_file, skiprows=1)[:, 16]
    J1_dxy_dxy = np.loadtxt(data_file, skiprows=1)[:, 17]
    J1_dz2_dxz = np.loadtxt(data_file, skiprows=1)[:, 18]
    J1_dz2_dyz = np.loadtxt(data_file, skiprows=1)[:, 19]
    J1_dz2_dx2y2 = np.loadtxt(data_file, skiprows=1)[:, 20]
    J1_dz2_dxy = np.loadtxt(data_file, skiprows=1)[:, 21]
    J1_dxz_dyz = np.loadtxt(data_file, skiprows=1)[:, 22]
    J1_dxz_dx2y2 = np.loadtxt(data_file, skiprows=1)[:, 23]
    J1_dxz_dxy = np.loadtxt(data_file, skiprows=1)[:, 24]
    J1_dyz_dxy = np.loadtxt(data_file, skiprows=1)[:, 25]
    J1_dyz_dx2y2 = np.loadtxt(data_file, skiprows=1)[:, 26]
    J1_dxy_dx2y2 = np.loadtxt(data_file, skiprows=1)[:, 27]
    J2_dz2_dz2 = np.loadtxt(data_file, skiprows=1)[:, 28]
    J2_x2y2_x2y2 = np.loadtxt(data_file, skiprows=1)[:, 29]
    J2_dxz_dxz = np.loadtxt(data_file, skiprows=1)[:, 30]
    J2_dyz_dyz = np.loadtxt(data_file, skiprows=1)[:, 31]
    J2_dxy_dxy = np.loadtxt(data_file, skiprows=1)[:, 32]
    J2_dz2_dxz = np.loadtxt(data_file, skiprows=1)[:, 33]
    J2_dz2_dyz = np.loadtxt(data_file, skiprows=1)[:, 34]
    J2_dz2_dx2y2 = np.loadtxt(data_file, skiprows=1)[:, 35]
    J2_dz2_dxy = np.loadtxt(data_file, skiprows=1)[:, 36]
    J2_dxz_dyz = np.loadtxt(data_file, skiprows=1)[:, 37]
    J2_dxz_dx2y2 = np.loadtxt(data_file, skiprows=1)[:, 38]
    J2_dxz_dxy = np.loadtxt(data_file, skiprows=1)[:, 39]
    J2_dyz_dxy = np.loadtxt(data_file, skiprows=1)[:, 40]
    J2_dyz_dx2y2 = np.loadtxt(data_file, skiprows=1)[:, 41]
    J2_dxy_dx2y2 = np.loadtxt(data_file, skiprows=1)[:, 42]
    J3_dz2_dz2 = np.loadtxt(data_file, skiprows=1)[:, 43]
    J3_x2y2_x2y2 = np.loadtxt(data_file, skiprows=1)[:, 44]
    J3_dxz_dxz = np.loadtxt(data_file, skiprows=1)[:, 45]
    J3_dyz_dyz = np.loadtxt(data_file, skiprows=1)[:, 46]
    J3_dxy_dxy = np.loadtxt(data_file, skiprows=1)[:, 47]
    J3_dz2_dxz = np.loadtxt(data_file, skiprows=1)[:, 48]
    J3_dz2_dyz = np.loadtxt(data_file, skiprows=1)[:, 49]
    J3_dz2_dx2y2 = np.loadtxt(data_file, skiprows=1)[:, 50]
    J3_dz2_dxy = np.loadtxt(data_file, skiprows=1)[:, 51]
    J3_dxz_dyz = np.loadtxt(data_file, skiprows=1)[:, 52]
    J3_dxz_dx2y2 = np.loadtxt(data_file, skiprows=1)[:, 53]
    J3_dxz_dxy = np.loadtxt(data_file, skiprows=1)[:, 54]
    J3_dyz_dxy = np.loadtxt(data_file, skiprows=1)[:, 55]
    J3_dyz_dx2y2 = np.loadtxt(data_file, skiprows=1)[:, 56]
    J3_dxy_dx2y2 = np.loadtxt(data_file, skiprows=1)[:, 57]
    x_axis = x_axis - 100
    figresolved1,ax1 = plt.subplots(2,2,figsize=[9,9])   

    ax1[0][0].plot(x_axis,J1tt,'-ok', color='black' )
    ax1[0][0].plot(x_axis,J1_dxz_dxz ,'-ok' , color='pink'  )
    ax1[0][0].plot(x_axis,J1_dyz_dyz ,'-ok' , color='blue')
    ax1[0][0].plot(x_axis,J1_dxy_dxy ,'-ok', color='cyan' )   
    ax1[0][0].plot(x_axis,J1_dxz_dyz ,'-ok', color='green' )  
    ax1[0][0].plot(x_axis,J1_dxz_dxy ,'-ok', color='yellow' )  
    ax1[0][0].plot(x_axis,J1_dyz_dxy ,'-ok', color='red' )  
    ax1[0][0].set_ylabel(r'$J_1$ (t$_{2g}$-t$_{2g}$), meV',fontsize = 20)
    ax1[0][0].set_xlabel(r'$\epsilon$, %',fontsize = 20)
    
    ax1[0][1].plot(x_axis, J1te ,'-ok', color='black' )  
    ax1[0][1].plot(x_axis, J1_dz2_dxz ,'-ok', color='pink' )  
    ax1[0][1].plot(x_axis, J1_dz2_dyz ,'-ok', color='blue' )  
    ax1[0][1].plot(x_axis, J1_dz2_dxy ,'-ok', color='cyan' )  
    ax1[0][1].plot(x_axis, J1_dxz_dx2y2 ,'-ok', color='green' )  
    ax1[0][1].plot(x_axis, J1_dyz_dx2y2 ,'-ok', color='yellow' )  
    ax1[0][1].plot(x_axis, J1_dxy_dx2y2 ,'-ok', color='red' )  
    ax1[0][1].set_ylabel(r'$J_1$ (t$_{2g}$-e$_{g}$), meV',fontsize = 20)
    ax1[0][1].set_xlabel(r'$\epsilon$, %',fontsize = 20)

    ax1[1][0].plot(x_axis,J1ee,'-ok', color='black' )
    ax1[1][0].plot(x_axis,J1_x2y2_x2y2,'-ok' , color='green'  )
    ax1[1][0].plot(x_axis,J1_dz2_dx2y2,'-ok' , color='red')
    ax1[1][0].plot(x_axis,J1_dz2_dz2,'-ok', color='blue' )   
    ax1[1][0].set_ylabel(r'$J_1$ (e$_{g}$-e$_{g}$), meV',fontsize = 20)
    ax1[1][0].set_xlabel(r'$\epsilon$, %',fontsize = 20)
    ax1[0][0].tick_params(axis='both', which='major', labelsize=15)
    ax1[1][0].tick_params(axis='both', which='major', labelsize=15)
    ax1[0][1].tick_params(axis='both', which='major', labelsize=15)
    ax1[1][1].tick_params(axis='both', which='major', labelsize=15)
    ax1[0][0].set_xticks([-5,-2.5,0,2.5,5])
    ax1[0][1].set_xticks([-5,-2.5,0,2.5,5])
    ax1[1][0].set_xticks([-5,-2.5,0,2.5,5])
    ax1[1][1].set_xticks([-5,-2.5,0,2.5,5])
    figresolved1.subplots_adjust(bottom=0.1)
    figresolved1.subplots_adjust(left=0.2)
    figresolved1.tight_layout()
    #plt.show()
    plt.savefig(output_dir + '/' + prefix + '.resolved_J1_vs' + label  + '.png')
    # ax[0].axhline(y=0.0, color='black', linestyle='--')
    # ax[1].axhline(y=0.0, color='black', linestyle='--')
    # ax[2].axhline(y=0.0, color='black', linestyle='--')
    #plt.savefig(output_dir + '/' + prefix + '.Total_J_vs' + label  + '.png')
    figresolved2,ax2 = plt.subplots(2,2,figsize=[9,9])   

    ax2[0][0].set_ylim(-0.1, 0.1)
    ax2[0][0].plot(x_axis,J2tt,'-ok', color='black' )
    ax2[0][0].plot(x_axis,J2_dxz_dxz ,'-ok' , color='pink'  )
    ax2[0][0].plot(x_axis,J2_dyz_dyz ,'-ok' , color='blue')
    ax2[0][0].plot(x_axis,J2_dxy_dxy ,'-ok', color='cyan' )   
    ax2[0][0].plot(x_axis,J2_dxz_dyz ,'-ok', color='green' )  
    ax2[0][0].plot(x_axis,J2_dxz_dxy ,'-ok', color='yellow' )  
    ax2[0][0].plot(x_axis,J2_dyz_dxy ,'-ok', color='red' )  
    ax2[0][0].set_ylabel(r'$J_2$ (t$_{2g}$-t$_{2g}$), meV',fontsize = 20)
    ax2[0][0].set_xlabel(r'$\epsilon$, %',fontsize = 20)
    ax2[0][1].plot(x_axis, J2te ,'-ok', color='black' )  
    ax2[0][1].plot(x_axis, J2_dz2_dxz ,'-ok', color='pink' )  
    ax2[0][1].plot(x_axis, J2_dz2_dyz ,'-ok', color='blue' )  
    ax2[0][1].plot(x_axis, J2_dz2_dxy ,'-ok', color='cyan' )  
    ax2[0][1].plot(x_axis, J2_dxz_dx2y2 ,'-ok', color='green' )  
    ax2[0][1].plot(x_axis, J2_dyz_dx2y2 ,'-ok', color='yellow' )  
    ax2[0][1].plot(x_axis, J2_dxy_dx2y2 ,'-ok', color='red' )  
    ax2[0][1].set_ylabel(r'$J_2$ (t$_{2g}$-e$_{g}$), meV',fontsize = 20)
    ax2[0][1].set_xlabel(r'$\epsilon$, %',fontsize = 20)
    ax2[0][0].set_xticks([-5,-2.5,0,2.5,5])
    ax2[0][1].set_xticks([-5,-2.5,0,2.5,5])
    ax2[1][0].set_xticks([-5,-2.5,0,2.5,5])
    ax2[1][1].set_xticks([-5,-2.5,0,2.5,5])
    ax2[1][0].plot(x_axis,J2ee,'-ok', color='black' )
    ax2[1][0].plot(x_axis,J2_x2y2_x2y2,'-ok' , color='green'  )
    ax2[1][0].plot(x_axis,J2_dz2_dx2y2,'-ok' , color='red')
    ax2[1][0].plot(x_axis,J2_dz2_dz2,'-ok', color='blue' )   
    ax2[1][0].set_ylabel(r'$J_2$ (e$_{g}$-e$_{g}$), meV',fontsize = 20)
    ax2[1][0].set_xlabel(r'$\epsilon$, %',fontsize = 20)
    ax2[0][0].tick_params(axis='both', which='major', labelsize=15)
    ax2[1][0].tick_params(axis='both', which='major', labelsize=15)
    ax2[0][1].tick_params(axis='both', which='major', labelsize=15)
    ax2[1][1].tick_params(axis='both', which='major', labelsize=15)
    figresolved2.subplots_adjust(bottom=0.1)
    figresolved2.subplots_adjust(left=0.2)
    figresolved2.tight_layout()
    #plt.show()
    plt.savefig(output_dir + '/' + prefix + '.resolved_J2_vs' + label  + '.png')
    figresolved3,ax3 = plt.subplots(2,2,figsize=[9,9])   
 
    ax3[0][0].plot(x_axis,J3tt,'-ok', color='black' )
    ax3[0][0].plot(x_axis,J3_dxz_dxz ,'-ok' , color='pink'  )
    ax3[0][0].plot(x_axis,J3_dyz_dyz ,'-ok' , color='blue')
    ax3[0][0].plot(x_axis,J3_dxy_dxy ,'-ok', color='cyan' )   
    ax3[0][0].plot(x_axis,J3_dxz_dyz ,'-ok', color='green' )  
    ax3[0][0].plot(x_axis,J3_dxz_dxy ,'-ok', color='yellow' )  
    ax3[0][0].plot(x_axis,J3_dyz_dxy ,'-ok', color='red' )  
    ax3[0][0].set_ylabel(r'$J_3$ (t$_{2g}$-t$_{2g}$), meV',fontsize = 20)
    ax3[0][0].set_xlabel(r'$\epsilon$, %',fontsize = 20)

    ax3[0][1].plot(x_axis, J3te ,'-ok', color='black' )  
    ax3[0][1].plot(x_axis, J3_dz2_dxz ,'-ok', color='pink' )  
    ax3[0][1].plot(x_axis, J3_dz2_dyz ,'-ok', color='blue' )  
    ax3[0][1].plot(x_axis, J3_dz2_dxy ,'-ok', color='cyan' )  
    ax3[0][1].plot(x_axis, J3_dxz_dx2y2 ,'-ok', color='green' )  
    ax3[0][1].plot(x_axis, J3_dyz_dx2y2 ,'-ok', color='yellow' )  
    ax3[0][1].plot(x_axis, J3_dxy_dx2y2 ,'-ok', color='red' )  
    ax3[0][1].set_ylabel(r'$J_3$ (t$_{2g}$-e$_{g}$), meV',fontsize = 20)
    ax3[0][1].set_xlabel(r'$\epsilon$, %',fontsize = 20)

    ax3[1][0].plot(x_axis,J3ee,'-ok', color='black' )
    ax3[1][0].plot(x_axis,J3_x2y2_x2y2,'-ok' , color='green'  )
    ax3[1][0].plot(x_axis,J3_dz2_dx2y2,'-ok' , color='red')
    ax3[1][0].plot(x_axis,J3_dz2_dz2,'-ok', color='blue' )   
    ax3[1][0].set_ylabel(r'$J_3$ (e$_{g}$-e$_{g}$), meV',fontsize = 20)
    ax3[1][0].set_xlabel(r'$\epsilon$, %',fontsize = 20)
    ax3[0][0].tick_params(axis='both', labelsize=15)
    ax3[1][0].tick_params(axis='both',  labelsize=15)
    ax3[0][1].tick_params(axis='both', labelsize=15)
    ax3[1][1].tick_params(axis='both', labelsize=15)
    ax3[0][0].set_xticks([-5,-2.5,0,2.5,5])
    ax3[0][1].set_xticks([-5,-2.5,0,2.5,5])
    ax3[1][0].set_xticks([-5,-2.5,0,2.5,5])
    ax3[1][1].set_xticks([-5,-2.5,0,2.5,5])
    figresolved3.subplots_adjust(bottom=0.1)
    figresolved3.subplots_adjust(left=0.2)
    figresolved3.tight_layout()
    #plt.show()
    plt.savefig(output_dir + '/' + prefix + '.resolved_J3_vs' + label  + '.png')
def plot_total(data_file,output_dir,label):
    x_axis = np.loadtxt(data_file, skiprows=1)[:, 0]
    J1iso= np.loadtxt(data_file, skiprows=1)[:, 1]
    J2iso= np.loadtxt(data_file, skiprows=1)[:, 2]
    J3iso= np.loadtxt(data_file, skiprows=1)[:, 3]
    J1tt = np.loadtxt(data_file, skiprows=1)[:, 4]
    J2tt= np.loadtxt(data_file, skiprows=1)[:, 5]
    J3tt = np.loadtxt(data_file, skiprows=1)[:, 6]
    J1te= np.loadtxt(data_file, skiprows=1)[:, 7]
    J2te = np.loadtxt(data_file, skiprows=1)[:, 8]
    J3te= np.loadtxt(data_file, skiprows=1)[:, 9]
    J1ee = np.loadtxt(data_file, skiprows=1)[:, 10]
    J2ee= np.loadtxt(data_file, skiprows=1)[:, 11]
    J3ee = np.loadtxt(data_file, skiprows=1)[:, 12]
    figtot,ax = plt.subplots(1,3,figsize=[12,5]) 
    x_axis = x_axis - 100
    ax[0].plot(x_axis,J1iso,'-ok', color='black' )
    ax[0].plot(x_axis,J1tt,'-ok' , color='blue'  )
    ax[0].plot(x_axis,J1te,'-ok' , color='darkorange')
    ax[0].plot(x_axis,J1ee,'-ok' , color='green' )
    ax[1].plot(x_axis,J2iso,'-ok', color='black' )
    ax[1].plot(x_axis,J2tt,'-ok' , color='blue'  )
    ax[1].plot(x_axis,J2te,'-ok' , color='darkorange')
    ax[1].plot(x_axis,J2ee,'-ok' , color='green' )
    ax[2].plot(x_axis,J3iso,'-ok', color='black' )
    ax[2].plot(x_axis,J3tt,'-ok' , color='blue'  )
    ax[2].plot(x_axis,J3te,'-ok' , color='darkorange')
    ax[2].plot(x_axis,J3ee,'-ok' , color='green' )
    ax[0].set_ylabel(r'$J_1$, meV',fontsize = 20)
    ax[1].set_ylabel(r'$J_2$, meV',fontsize = 20)
    ax[2].set_ylabel(r'$J_3$, meV',fontsize = 20)
    ax[0].set_xlabel(r'$\epsilon$, %',fontsize = 20)
    ax[1].set_xlabel(r'$\epsilon$, %',fontsize = 20)
    ax[2].set_xlabel(r'$\epsilon$, %',fontsize = 20)
    ax[0].axhline(y=0.0, color='black', linestyle='--')
    ax[1].axhline(y=0.0, color='black', linestyle='--')
    ax[2].axhline(y=0.0, color='black', linestyle='--')
    ax[0].tick_params(axis='both', labelsize=15)
    ax[1].tick_params(axis='both',  labelsize=15)
    ax[2].tick_params(axis='both',  labelsize=15)
    ax[0].set_xticks([-5,-2.5,0,2.5,5])
    ax[1].set_xticks([-5,-2.5,0,2.5,5])
    ax[2].set_xticks([-5,-2.5,0,2.5,5])
    figtot.subplots_adjust(bottom=0.1)
    figtot.subplots_adjust(left=0.2)
    figtot.tight_layout()
    #plt.show()
    plt.savefig(output_dir + '/' + prefix + '.Total_J_vs' + label  + '.png')
#def plot_tables(matrix_to_plot_tablesJ1,matrix_to_plot_tablesJ2,matrix_to_plot_tablesJ3):

prefix = 'cri3'
Uscf = 4.0; Umin =4.0; Umax =4.0; Unstep =1.0
strmin =95; strmax =105; strnstep =1
input_dir,output_dir = parser() 

plt.rcParams['figure.max_open_warning'] = 0
create_J_vs_strain_file(prefix,Umax,Umin,Unstep,strmax,strmin,strnstep,output_dir)
#create_J_vs_U_file(prefix,Umax,Umin,Unstep,strmax,strmin,strnstep,output_dir)





  
