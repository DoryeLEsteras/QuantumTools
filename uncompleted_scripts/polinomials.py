import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from subprocess import run
# To Do List
"""
Prepare inferface with real J inputs

generalize function
"""

def format_input(prefix,strmax,strmin,strnstep,Umax,Umin,Unstep):
    J1iso_vector = np.array([]);J2iso_vector = np.array([]);J3iso_vector = np.array([]);U_vector = np.array([]);strain_vector = np.array([])
    J1x_vector  = np.array([]);J1y_vector  = np.array([]);J1z_vector  = np.array([]);J2x_vector  = np.array([]);J2y_vector  = np.array([]);J2z_vector  = np.array([]);J3x_vector  = np.array([]);J3y_vector  = np.array([]);J3z_vector  = np.array([])
    for strain in np.arange(strmin,strmax+1,strnstep):
        for U in np.arange(Umin,Umax+1,Unstep):
            output_file_strain = open('exchange.' + str(prefix) + '.' + str(strain) + '.' + str(U), 'r')
            read_vector = output_file_strain.readlines()
            U_vector = np.append(U_vector,U)
            strain_vector = np.append(strain_vector,strain)
            counter = 0
            for line in read_vector:
                readed_line = line.replace(';', '')
                readed_line = readed_line.split()
                readed_line.append('end')              
                if readed_line[0] == 'J1' and readed_line[1] == 'iso':
                    J1iso = float(readed_line[3])
                    J1iso_vector = np.append(J1iso_vector,J1iso)
                if readed_line[0] == 'J2' and readed_line[1] == 'iso':
                    J2iso = float(readed_line[3])
                    J2iso_vector = np.append(J2iso_vector,J2iso)
                if readed_line[0] == 'J3' and readed_line[1] == 'iso':
                    J3iso = float(readed_line[3])
                    J3iso_vector = np.append(J3iso_vector,J3iso)
                if readed_line[0] == 'J1' and readed_line[1] == 'ani':
                    J1ani = read_vector[counter+1]
                    J1ani  = J1ani.split()
                    J1x = float(J1ani[0])
                    J1x_vector = np.append(J1x_vector,J1x)
                    J1ani = read_vector[counter+2]
                    J1ani  = J1ani.split()
                    J1y = float(J1ani[1])
                    J1y_vector = np.append(J1y_vector,J1y)
                    J1ani = read_vector[counter+3]
                    J1ani  = J1ani.split()
                    J1z = float(J1ani[2])
                    J1z_vector = np.append(J1z_vector,J1z)
                if readed_line[0] == 'J2' and readed_line[1] == 'ani':
                    J2ani = read_vector[counter+1]
                    J2ani  = J2ani.split()
                    J2x = float(J2ani[0])
                    J2x_vector = np.append(J2x_vector,J2x)
                    J2ani = read_vector[counter+2]
                    J2ani  = J2ani.split()
                    J2y = float(J2ani[1])
                    J2y_vector = np.append(J2y_vector,J2y)
                    J2ani = read_vector[counter+3]
                    J2ani  = J2ani.split()
                    J2z = float(J2ani[2])
                    J2z_vector = np.append(J2z_vector,J2z)
                if readed_line[0] == 'J3' and readed_line[1] == 'ani':
                    J3ani = read_vector[counter+1]
                    J3ani  = J3ani.split()
                    J3x = float(J3ani[0])
                    J3x_vector = np.append(J3x_vector,J3x)
                    J3ani = read_vector[counter+2]
                    J3ani  = J3ani.split()
                    J3y = float(J3ani[1])
                    J3y_vector = np.append(J3y_vector,J3y)
                    J3ani = read_vector[counter+3]
                    J3ani  = J3ani.split()
                    J3z = float(J3ani[2])
                    J3z_vector = np.append(J3z_vector,J3z)
                counter = counter + 1 
    np.savetxt(prefix + '.' + 'J1iso' + '.' + 'poly_data.txt', np.c_[strain_vector,U_vector,J1iso_vector], delimiter=' ')
    np.savetxt(prefix + '.' + 'J2iso' + '.' + 'poly_data.txt', np.c_[strain_vector,U_vector,J2iso_vector], delimiter=' ')
    np.savetxt(prefix + '.' + 'J3iso' + '.' + 'poly_data.txt', np.c_[strain_vector,U_vector,J3iso_vector], delimiter=' ')
    np.savetxt(prefix + '.' + 'J1x' + '.' + 'poly_data.txt', np.c_[strain_vector,U_vector,J1x_vector], delimiter=' ')
    np.savetxt(prefix + '.' + 'J1y' + '.' + 'poly_data.txt', np.c_[strain_vector,U_vector,J1y_vector], delimiter=' ')
    np.savetxt(prefix + '.' + 'J1z' + '.' + 'poly_data.txt', np.c_[strain_vector,U_vector,J1z_vector], delimiter=' ')
    np.savetxt(prefix + '.' + 'J2x' + '.' + 'poly_data.txt', np.c_[strain_vector,U_vector,J2x_vector], delimiter=' ')
    np.savetxt(prefix + '.' + 'J2y' + '.' + 'poly_data.txt', np.c_[strain_vector,U_vector,J2y_vector], delimiter=' ')
    np.savetxt(prefix + '.' + 'J2z' + '.' + 'poly_data.txt', np.c_[strain_vector,U_vector,J2z_vector], delimiter=' ')
    np.savetxt(prefix + '.' + 'J3x' + '.' + 'poly_data.txt', np.c_[strain_vector,U_vector,J3x_vector], delimiter=' ')
    np.savetxt(prefix + '.' + 'J3y' + '.' + 'poly_data.txt', np.c_[strain_vector,U_vector,J3y_vector], delimiter=' ')
    np.savetxt(prefix + '.' + 'J3z' + '.' + 'poly_data.txt', np.c_[strain_vector,U_vector,J3z_vector], delimiter=' ')
def func(I,x0,a,b,c,d,e):
    x,y = I
    return x0 + a*x + b*y + c*x*y +d*x*x + e*y*y
def poly_magic(file_to_read):
    xdata = np.loadtxt(file_to_read)[:, 0]
    ydata = np.loadtxt(file_to_read)[:, 1]
    zdata = np.loadtxt(file_to_read)[:, 2]
    coef = np.array([0,0,0,0,0,0]);trash = np.array([0,0,0,0,0,0]);trash_matrix = np.zeros((6,3))
    res = curve_fit(func, (xdata,ydata), zdata)
    x0 = res[0][0]; a = res[0][1]; b = res[0][2]; c = res[0][3]; d = res[0][4]; e = res[0][5]
    return x0,a,b,c,d,e
def plotter_vs_U(x0,a,b,c,d,e,strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,J_label):   
    for i in np.arange(strmin,strmax + strnstep,strnstep):
        label = 'strain' + str(i)
        x = np.array([]);y = np.array([]);z = np.array([])
        for j in np.arange(Umin,Umax + Unstep,Unstep):
            x = np.append(x,i)
            y = np.append(y,j)
            z = np.append(z,x0 + a*i + b*j + c*i*j +d*i*i + e*j*j)
        figsimple,ax = plt.subplots() 
        ax.plot(y,z ,'-')
        plt.savefig(prefix + '.' + J_label +'.' + label + '.' + 'vsU' + '.png')
def plotter_vs_strain(x0,a,b,c,d,e,strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,J_label):  
    for j in np.arange(Umin,Umax + Unstep,Unstep):
        label = 'U' + str(j)
        x = np.array([]);y = np.array([]);z = np.array([])
        for i in np.arange(strmin,strmax + strnstep,strnstep):
            x = np.append(x,i)
            y = np.append(y,j)
            z = np.append(z,x0 + a*i + b*j + c*i*j +d*i*i + e*j*j)
        figsimple,ax = plt.subplots() 
        ax.plot(x,z ,'-')
        plt.savefig(prefix + '.' + J_label +'.' + label + '.' + 'vs_strain' + '.png')
def poly_calculator(x0,a,b,c,d,e,strmax,strmin,poly_str_mesh,Umax,Umin,poly_U_mesh,prefix,J_label):
    poly_output_file = open(str(prefix) + '.' + str(J_label) + '.' + 'poly_data.txt', 'w')
    x = np.array([]);y = np.array([]);z = np.array([])
    for j in np.arange(Umin,Umax + poly_U_mesh,poly_U_mesh):     
        for i in np.arange(strmin,strmax + poly_str_mesh,poly_str_mesh):
            x = np.append(x,i)
            y = np.append(y,j)
            z = np.append(z,x0 + a*i + b*j + c*i*j +d*i*i + e*j*j)    
    np.savetxt(prefix + '.' + J_label + '.' + 'poly_data.txt', np.c_[x,y,z], delimiter=' ')
def perform_full_calculation(strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,poly_str_mesh,poly_U_mesh,J_label,exchange_input):
    x0,a,b,c,d,e = poly_magic(exchange_input)
    #plotter_vs_U(x0,a,b,c,d,e,strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,J_label)
    #plotter_vs_strain(x0,a,b,c,d,e,strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,J_label)
    poly_calculator(x0,a,b,c,d,e,strmax,strmin,poly_str_mesh,Umax,Umin,poly_U_mesh,prefix,J_label) 
def calculate_curie_J_converter(prefix,spin):
    Tc_file = open(prefix + '.Curie_temperature_results.txt', 'w')
    strain = np.loadtxt(prefix + '.' + 'J1iso' + '.' + 'poly_data.txt')[:, 0]
    U = np.loadtxt(prefix + '.' + 'J1iso' + '.' + 'poly_data.txt')[:, 1]
    J1iso = np.loadtxt(prefix + '.' + 'J1iso' + '.' + 'poly_data.txt')[:, 2]
    J1x = np.loadtxt(prefix + '.' + 'J1x' + '.' + 'poly_data.txt')[:, 2]
    J1y = np.loadtxt(prefix + '.' + 'J1y' + '.' + 'poly_data.txt')[:, 2]
    J1z = np.loadtxt(prefix + '.' + 'J1z' + '.' + 'poly_data.txt')[:, 2]
    J2iso = np.loadtxt(prefix + '.' + 'J2iso' + '.' + 'poly_data.txt')[:, 2]
    J2x = np.loadtxt(prefix + '.' + 'J2x' + '.' + 'poly_data.txt')[:, 2]
    J2y = np.loadtxt(prefix + '.' + 'J2y' + '.' + 'poly_data.txt')[:, 2]
    J2z = np.loadtxt(prefix + '.' + 'J2z' + '.' + 'poly_data.txt')[:, 2]
    J3iso = np.loadtxt(prefix + '.' + 'J3iso' + '.' + 'poly_data.txt')[:, 2]
    J3x = np.loadtxt(prefix + '.' + 'J3x' + '.' + 'poly_data.txt')[:, 2]
    J3y = np.loadtxt(prefix + '.' + 'J3y' + '.' + 'poly_data.txt')[:, 2]
    J3z = np.loadtxt(prefix + '.' + 'J3z' + '.' + 'poly_data.txt')[:, 2]
    Belgic_J1_vector = np.array([]);Belgic_J2_vector = np.array([]);Belgic_J3_vector = np.array([]);
    Belgic_Delta1_vector = np.array([]);Belgic_Delta2_vector = np.array([]);Belgic_Delta3_vector = np.array([])
    Tc_vector = np.array([])
    for i in np.arange(0,len(J1iso),1):
       Belgic_J1 = 4*(2*J1iso[i] + J1z[i] +0.5*J1x[i] +0.5*J1y[i])/9
       Belgic_J1_vector = np.append(Belgic_J1_vector,Belgic_J1)
       Belgic_Delta1 = 1- (8*(J1iso[i] +0.5*J1x[i] +0.5*J1y[i])/(9*Belgic_J1_vector[i]))
       Belgic_Delta1_vector = np.append(Belgic_Delta1_vector,Belgic_Delta1)
       Belgic_J2 = 4*(2*J2iso[i] + J2z[i] +0.5*J2x[i] +0.5*J2y[i])/9
       Belgic_J2_vector = np.append(Belgic_J2_vector,Belgic_J2)
       Belgic_Delta2 = 1- (8*(J2iso[i] +0.5*J2x[i] +0.5*J2y[i])/(9*Belgic_J2_vector[i]))
       Belgic_Delta2_vector = np.append(Belgic_Delta2_vector,Belgic_Delta2)  
       Belgic_J3 = 4*(2*J3iso[i] + J3z[i] +0.5*J3x[i] +0.5*J3y[i])/9
       Belgic_J3_vector = np.append(Belgic_J3_vector,Belgic_J3)
       Belgic_Delta3 = 1- (8*(J3iso[i] +0.5*J3x[i] +0.5*J3y[i])/(9*Belgic_J3_vector[i]))
       Belgic_Delta3_vector = np.append(Belgic_Delta3_vector,Belgic_Delta3)
       Tc = run(['python3', '../QuantumTools/strain_and_U_calculate_curie.py','-l', 'hon','-out', './curie.txt','-S',str(spin),'-st','1','-u','1','-D', str(Belgic_Delta1),str(Belgic_Delta2),str(1),'-J',str(Belgic_Delta3),str(Belgic_J2),str(Belgic_J3)],capture_output=True)
       output = Tc.stdout
       Tc = output.decode("utf-8")
       Tc = Tc.split()
       Tc = Tc[4]
       Tc_vector = np.append(Tc_vector,float(Tc))
    Tc_file.close()
    np.savetxt(prefix + 'belgium_exchange_and_Curie.txt', np.c_[strain,U,Belgic_J1_vector,Belgic_J2_vector,Belgic_J3_vector,Belgic_Delta1_vector,Belgic_Delta2_vector,Belgic_Delta3_vector,Tc_vector], delimiter=' ')
    #return Tc_vector
    map_file = open(prefix + '.Curie_map.txt', 'w')
    counter = int(0)
    Tc_matrix = np.array([[]])
    new_str_len = int((strmax-strmin)/strnstep)
    new_U_len = int((Umax-Umin)/Unstep)
    #print(new_str_len,new_U_len, counter )
    for strindex in np.arange(0,new_str_len + 1,1): 
        for Uindex in np.arange(0,new_U_len + 1,1):
            #print(strindex,Uindex,counter)
            #print(Tc_vector[counter])
            #print(Tc_matrix[[strindex,Uindex]])
            #Tc_matrix = np.insert(Tc_matrix, Uindex, Tc_vector[counter], axis = strindex)
            #Tc_matrix[strindex][Uindex] = Tc_vector[counter]
            #print(strindex,Uindex)
            counter = counter + 1 
    print(Tc_matrix)
    map_file.close()

    #    for Uindex in np.arange(Umin,Umax + poly_U_mesh,poly_U_mesh):     
    #for strindex in np.arange(strmin,strmax + poly_str_mesh,poly_str_mesh): 
    #    for Uindex in np.arange(Umin,Umax + poly_U_mesh,poly_U_mesh):  
            




    #return Belgic_J1_vector,Belgic_J2_vector,Belgic_J3_vector,Belgic_Delta1_vector,Belgic_Delta2_vector,Belgic_Delta3_vector
def Calculate_Curie(prefix,Tc_vector,strmax,strmin,Umax,Umin,poly_str_mesh,poly_U_mesh,):  
    Tc_file = open(prefix + '.Curie_map.txt', 'w')
    counter = 0
    Tc_matrix = np.array([[]])
    for strindex in np.arange(strmin,strmax + poly_str_mesh,poly_str_mesh): 
        for Uindex in np.arange(Umin,Umax + poly_U_mesh,poly_U_mesh):  
            Tc = run(['python3', '../QuantumTools/strain_and_U_calculate_curie.py','-l', 'hon','-out', './curie.txt','-S',str(spin),'-st','1','-u','1','-D', str(Belgic_Delta1),str(Belgic_Delta2),str(1),'-J',str(Belgic_Delta3),str(Belgic_J2),str(Belgic_J3)],capture_output=True)
            output = Tc.stdout
            Tc = output.decode("utf-8")
            Tc_file.write(str(Tc) + ' ')
            counter = counter + 1
        Tc_file.write('\n')
    Tc_file.close()




def Plot_3D_map():
    arr = np.loadtxt('curiecalva.txt', usecols=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,))
    arr2= arr - 23.19
    fig, ax = plt.subplots()
    fig = plt.imshow(arr2, cmap='seismic', interpolation='none',origin='lower',vmin=-8,vmax=8)
    plt.xlabel('Strain (%)')
    plt.ylabel('U(eV)')
    plt.colorbar(fig) # adding the colobar on the right


    #x_label_list = ['-5','','','','','','','','','','','','','', '-4','','','','','','','','','', '-3', '','','','','','','','','', '-2', '','','','','','','','','', '-1', '0','1', '2', '3', '4', '5']
    y_label_list = ['2','3','4','5','6',]
    x_label_list = ['-5', '-4', '-3', '-2', '-1', '0','1', '2', '3', '4', '5']
    #y_label_list = ['2','3','4','5','6',]
    #
    #ax.set_xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50])
    #ax.set_xticks([0,1,2,3,4 5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50])
    #ax.set_yticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40])
    #a=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50]
    ax.set_xticks([0, 5, 10,15,20,25,30,35,40,45,50])
    ax.set_yticks([0,10,20,30,40])
    ax.set_xticklabels(x_label_list)
    ax.set_yticklabels(y_label_list)

    plt.xlabel('Strain (%)', fontsize=20)
    plt.ylabel('U (eV)', fontsize=20)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    cb = plt.colorbar(fig, orientation="vertical", pad=0.2)
    cb.set_label(label='Tc (K)', size='x-large', weight='bold')
    cb.ax.tick_params(labelsize='x-large')
    plt.show()

if __name__ == '__main__':
    prefix = 'crcl3'
    spin =1.5
    strmax = 105;strmin = 100;strnstep = 1;Umax = 6.0;Umin = 4.0;Unstep =  1.0; poly_str_mesh = 1 ; poly_U_mesh = 1.0
    format_input(prefix,strmax,strmin,strnstep,Umax,Umin,Unstep)
    perform_full_calculation(strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,poly_str_mesh,poly_U_mesh,'J1',prefix  + '.J1iso.poly_data.txt')
    perform_full_calculation(strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,poly_str_mesh,poly_U_mesh,'J1x',prefix  + '.J1x.poly_data.txt')
    perform_full_calculation(strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,poly_str_mesh,poly_U_mesh,'J1y',prefix  + '.J1y.poly_data.txt')
    perform_full_calculation(strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,poly_str_mesh,poly_U_mesh,'J1z',prefix  + '.J1z.poly_data.txt') 
    Belgic_J1_vector,Belgic_J2_vector,Belgic_J3_vector,Belgic_Delta1_vector,Belgic_Delta2_vector,Belgic_Delta3_vector = calculate_curie_J_converter(prefix,spin) 
   