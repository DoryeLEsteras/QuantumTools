import numpy as np
from argparse import ArgumentParser
import matplotlib.pyplot as plt
# TO DO LIST
"""
- Add more plots according to necessities 
"""
def parser():
    parser = ArgumentParser(description="Script to fix the matrices of Gaussian")
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
    return J1iso,J2iso,J3iso,J1_t2g_t2g, J2_t2g_t2g, J3_t2g_t2g,J1_t2g_eg, J2_t2g_eg, J3_t2g_eg,J1_eg_eg, J2_eg_eg, J3_eg_eg
def create_JvsU_file(prefix,Umax,Umin,Unstep,output_file_to_write,input_dir):
    strain = '100'
    output_file_U.write('U' + '  ' + 'J1 iso' + '  ' + 'J2 iso' + '  ' + 'J3 iso' + '  ' + 'J1_t2g_t2g' + '  ' + 'J2_t2g_t2g' + '  ' + 'J3_t2g_t2g' + '  ' + 'J1_t2g_eg' + '  ' + 'J2_t2g_eg' + '  ' + 'J3_t2g_eg' + '  ' + 'J1_eg_eg' + '  ' + 'J2_eg_eg' + '  ' + 'J3_eg_eg' + '\n')
    for U in np.arange(Umin,Umax+1,Unstep):
        file_name = 'exchange.' + prefix + '.' + str(strain) + '.' + str(U)
        input_file = open(input_dir + file_name,'r')
        J1iso,J2iso,J3iso,J1_t2g_t2g, J2_t2g_t2g, J3_t2g_t2g,J1_t2g_eg, J2_t2g_eg, J3_t2g_eg,J1_eg_eg, J2_eg_eg, J3_eg_eg = manage_input_files(input_file)
        input_file.close()
        output_file_U.write(str(U) + '  ' + str(J1iso) + '  ' + str(J2iso) + '  ' + str(J3iso) + '  ' + str(J1_t2g_t2g) + '  ' + str(J2_t2g_t2g) + '  ' + str(J3_t2g_t2g) + '  ' + str(J1_t2g_eg) + '  ' + str(J2_t2g_eg) + '  ' + str(J3_t2g_eg) + '  ' + str(J1_eg_eg) + '  ' + str(J2_eg_eg) + '  ' + str(J3_eg_eg ) + '\n')
    output_file_U.close()
def create_Jvsstrain_file(prefix,strmax,strmin,strnstep,output_file_to_write,input_dir):
    U = Uscf
    output_file_strain.write('strain' + '  ' + 'J1 iso' + '  ' + 'J2 iso' + '  ' + 'J3 iso' + '  ' + 'J1_t2g_t2g' + '  ' + 'J2_t2g_t2g' + '  ' + 'J3_t2g_t2g' + '  ' + 'J1_t2g_eg' + '  ' + 'J2_t2g_eg' + '  ' + 'J3_t2g_eg' + '  ' + 'J1_eg_eg' + '  ' + 'J2_eg_eg' + '  ' + 'J3_eg_eg' + '\n')
    for strain in np.arange(strmin,strmax+1,strnstep):
        file_name = 'exchange.' + prefix + '.' + str(strain) + '.' + str(U)
        input_file = open(input_dir + file_name,'r')
        J1iso,J2iso,J3iso,J1_t2g_t2g, J2_t2g_t2g, J3_t2g_t2g,J1_t2g_eg, J2_t2g_eg, J3_t2g_eg,J1_eg_eg, J2_eg_eg, J3_eg_eg = manage_input_files(input_file)
        input_file.close()
        output_file_strain.write(str(strain) + '  ' + str(J1iso) + '  ' + str(J2iso) + '  ' + str(J3iso) + '  ' + str(J1_t2g_t2g) + '  ' + str(J2_t2g_t2g) + '  ' + str(J3_t2g_t2g) + '  ' + str(J1_t2g_eg) + '  ' + str(J2_t2g_eg) + '  ' + str(J3_t2g_eg) + '  ' + str(J1_eg_eg) + '  ' + str(J2_eg_eg) + '  ' + str(J3_eg_eg ) + '\n')
    output_file_strain.close()
def plotter(data_file,output_dir,xaxis_name):
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



prefix = 'crbr3'
Uscf = 2.0; Umin =2.0; Umax =6.0; Unstep =1.0
strmin =95; strmax =105; strnstep =1
input_dir,output_dir = parser()
strain_file = output_dir + 'out' + '_strain' + '.txt'
U_file = output_dir + 'out' + '_u' + '.txt'
output_file_strain = open(strain_file, 'w')
output_file_U = open(U_file, 'w')

create_JvsU_file(prefix,Umax,Umin,Unstep,output_file_U,input_dir)
create_Jvsstrain_file(prefix,strmax,strmin,strnstep,output_file_strain,input_dir)
plotter(strain_file,output_dir,'strain')
plotter(U_file,output_dir,'U')




  
