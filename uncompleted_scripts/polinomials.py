import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from matplotlib import cm
from subprocess import run
# To Do List
"""
generalize number of J
generalize function
add directories for the different outputs (parser?)
"""
def parser():
    parser = ArgumentParser(description="Script for creating SpinW input files")
    parser.add_argument("-inputdir", "--inputdir",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the bands input file
                        """)

    args = parser.parse_args()
    return args.inputdir
def format_input(prefix,strmax,strmin,strnstep,Umax,Umin,Unstep):
    """"
    Takes the filtered exchange file and produces files in the format: str U J
    Each Jiiso and Jix,Jiy,Jiz are saved in different files.
    """
    J1iso_vector = np.array([]);J2iso_vector = np.array([]);J3iso_vector = np.array([]);U_vector = np.array([]);strain_vector = np.array([])
    J1x_vector  = np.array([]);J1y_vector  = np.array([]);J1z_vector  = np.array([]);J2x_vector  = np.array([]);J2y_vector  = np.array([]);J2z_vector  = np.array([]);J3x_vector  = np.array([]);J3y_vector  = np.array([]);J3z_vector  = np.array([])
    for strain in np.arange(strmin,strmax+strnstep,strnstep):
        for U in np.arange(Umin,Umax+ Unstep,Unstep):
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
    """
    Defines the polinomials that are going to be used, this function is used inside of poly_magic
    """
    x,y = I
    return x0 + a*x + b*y + c*x*y +d*x*x + e*y*y
def poly_magic(prefix,J_label):
    """
    Read the data for an exchange file in the format  produced by the format_input function and obtains the coefficients.
    Now two different things can be done:
    - The two plotter functions allow to see the polinomials vs U and strain with the DFT mesh (to test)
    - The poly calculator performs an expensive calculation of using the polinomials to create a high mesh of points (to produce results)
    """
    file_to_read = prefix  + '.' + J_label +  '.poly_data.txt'
    xdata = np.loadtxt(file_to_read)[:, 0]
    ydata = np.loadtxt(file_to_read)[:, 1]
    zdata = np.loadtxt(file_to_read)[:, 2]
    coef = np.array([0,0,0,0,0,0]);trash = np.array([0,0,0,0,0,0]);trash_matrix = np.zeros((6,3))
    res = curve_fit(func, (xdata,ydata), zdata)
    x0 = res[0][0]; a = res[0][1]; b = res[0][2]; c = res[0][3]; d = res[0][4]; e = res[0][5]
    #print(x0,a,b,c,d,e)
    return x0,a,b,c,d,e
def plotter_vs_U(x0,a,b,c,d,e,strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,J_label):   
    """
    For each Jij plots the polinomial with basic mesh vs U. J label is used as a label for the figures.
    """
    file_to_read = prefix  + '.' + J_label +  '.poly_data.txt'
    xdft = np.loadtxt(file_to_read)[:, 0]
    ydft = np.loadtxt(file_to_read)[:, 1]
    zdft = np.loadtxt(file_to_read)[:, 2]
    for i in np.arange(strmin,strmax + strnstep,strnstep):
        label = 'strain' + str(i)
        xaxis = np.array([]);zaxis = np.array([])
        for j in np.arange(0,len(xdft),1):
            if xdft[j] > (i - strnstep) and xdft[j] < (i + strnstep):  
               xaxis = np.append(xaxis,ydft[j])
               zaxis = np.append(zaxis,zdft[j])
        x = np.array([]);y = np.array([]);z = np.array([])
        for j in np.arange(Umin,Umax + Unstep,Unstep):
            x = np.append(x,i)
            y = np.append(y,j)
            z = np.append(z,x0 + a*i + b*j + c*i*j +d*i*i + e*j*j)
        figsimple,ax = plt.subplots() 
        ax.plot(y,z ,'-')
        ax.plot(xaxis,zaxis ,'bo')
        plt.savefig(prefix + '.' + J_label +'.' + label + '.' + 'vsU' + '.png')
def plotter_vs_strain(x0,a,b,c,d,e,strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,J_label):  
    """
    For each Jij plots the polinomial with basic mesh vs strain. J label is used as a label for the figures.
    """
    file_to_read = prefix  + '.' + J_label +  '.poly_data.txt'
    xdft = np.loadtxt(file_to_read)[:, 0]
    ydft = np.loadtxt(file_to_read)[:, 1]
    zdft = np.loadtxt(file_to_read)[:, 2]
    for j in np.arange(Umin,Umax + Unstep,Unstep):
        label = 'U' + str(j)
        xaxis = np.array([]);zaxis = np.array([])
        for i in np.arange(0,len(ydft),1):
            if ydft[i] > (j - Unstep) and ydft[i] < (j + Unstep):  
               xaxis = np.append(xaxis,xdft[i])
               zaxis = np.append(zaxis,zdft[i])        
        x = np.array([]);y = np.array([]);z = np.array([])
        for i in np.arange(strmin,strmax + strnstep,strnstep):
            x = np.append(x,i)
            y = np.append(y,j)
            z = np.append(z,x0 + a*i + b*j + c*i*j +d*i*i + e*j*j)
        figsimple,ax = plt.subplots() 
        #ax.plot(x,z ,'-')
        ax.plot(x,z ,'-')
        ax.plot(xaxis,zaxis ,'bo')
        plt.savefig(prefix + '.' + J_label +'.' + label + '.' + 'vs_strain' + '.png')
def poly_calculator(x0,a,b,c,d,e,strmax,strmin,poly_str_mesh,Umax,Umin,poly_U_mesh,prefix,J_label):
    """
    For each Jij calculates the exchange in a fine mesh poly_U_mesh and poly_str_mesh.
    """
    poly_output_file = open(str(prefix) + '.' + str(J_label) + '.' + 'full_poly_file.txt', 'w')
    new_str_len  = int((strmax-strmin)/poly_str_mesh)
    new_U_len = int((Umax-Umin)/poly_U_mesh)
    x = np.array([]);y = np.array([]);z = np.array([])
    for j in np.arange(Umin,Umax + poly_U_mesh/10000,poly_U_mesh):     
        for i in np.arange(strmin,strmax + poly_str_mesh/10000,poly_str_mesh):
            #i = round(i,5)
            #j = round(j,5)
            x = np.append(x,i)
            y = np.append(y,j)
            #print(x)
            z = np.append(z,x0 + a*i + b*j + c*i*j +d*i*i + e*j*j)    
            #print(z)
    np.savetxt(prefix + '.' + J_label + '.' + 'full_poly_file.txt', np.c_[x,y,z], delimiter=' ')
    poly_output_file.close()
    x_axis = np.arange(strmin,strmax,poly_str_mesh)

    y_axis = np.arange(Umin,Umax+ poly_U_mesh/10000,poly_U_mesh)
    X, Y = np.meshgrid(x_axis, y_axis)
    Z = x0 + a*X + b*Y + c*X*Y +d*X*X + e*Y*Y
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.set_xticks([95,97.5,100,102.5,105])
    ax.set_yticks([2,3,4,5,6])
    surf = ax.plot_surface(X, Y, Z, cmap='viridis',linewidth=2, antialiased=False)
    #y_label_list = ['2','3','4','5','6']
    x_label_list = ['-5', '-2.5', '0', '2.5', '5']
    ax.set_xticklabels(x_label_list)
    #ax.set_yticklabels(y_label_list) 
    #ax.set_zticks([])
    
    plt.ylabel('U, eV', fontsize=12)
    plt.xlabel('Strain, %', fontsize=12)
    plt.title(J_label)
    clb= fig.colorbar(surf, shrink=0.5, aspect=20)
    #clb.ax.set_title('Tc (K)',fontsize=15)
    #plt.colorbar(fig, orientation="vertical", pad=0.2)

    #cb.set_label(label='Tc (K)', size='x-large', weight='bold')
    #cb.ax.tick_params(labelsize='x-large')
    #plt.show()
def calculate_curie(prefix,spin):
    """
    Reads The estended poly files,computes Belgium parameters and Tc. As a results a file with the Heat map data is created in the appropiate format
    """
    Tc_file = open(prefix + '.Curie_temperature_results.txt', 'w')
    strain = np.loadtxt(prefix + '.' + 'J1iso' + '.' + 'full_poly_file.txt')[:, 0]
    U = np.loadtxt(prefix + '.' + 'J1iso' + '.' + 'full_poly_file.txt')[:, 1]
    J1iso = np.loadtxt(prefix + '.' + 'J1iso' + '.' + 'full_poly_file.txt')[:, 2]
    J1x = np.loadtxt(prefix + '.' + 'J1x' + '.' + 'full_poly_file.txt')[:, 2]
    J1y = np.loadtxt(prefix + '.' + 'J1y' + '.' + 'full_poly_file.txt')[:, 2]
    J1z = np.loadtxt(prefix + '.' + 'J1z' + '.' + 'full_poly_file.txt')[:, 2]
    J2iso = np.loadtxt(prefix + '.' + 'J2iso' + '.' + 'full_poly_file.txt')[:, 2]
    J2x = np.loadtxt(prefix + '.' + 'J2x' + '.' + 'full_poly_file.txt')[:, 2]
    J2y = np.loadtxt(prefix + '.' + 'J2y' + '.' + 'full_poly_file.txt')[:, 2]
    J2z = np.loadtxt(prefix + '.' + 'J2z' + '.' + 'full_poly_file.txt')[:, 2]
    J3iso = np.loadtxt(prefix + '.' + 'J3iso' + '.' + 'full_poly_file.txt')[:, 2]
    J3x = np.loadtxt(prefix + '.' + 'J3x' + '.' + 'full_poly_file.txt')[:, 2]
    J3y = np.loadtxt(prefix + '.' + 'J3y' + '.' + 'full_poly_file.txt')[:, 2]
    J3z = np.loadtxt(prefix + '.' + 'J3z' + '.' + 'full_poly_file.txt')[:, 2]
    J1plane = (J1x+J1y)/2
    J2plane = (J2x+J2y)/2
    J3plane = (J3x+J3y)/2
    #print(J1iso)
    
    Belgic_J1_vector = np.array([]);Belgic_J2_vector = np.array([]);Belgic_J3_vector = np.array([])
    Belgic_Delta1_vector = np.array([]);Belgic_Delta2_vector = np.array([]);Belgic_Delta3_vector = np.array([])
    Tc_vector = np.array([])
    counter = 0
    for i in np.arange(0,len(J1iso),1):
       Belgic_J1 = (2*J1iso[i]+ J1plane[i] + J1z[i])/2
       Belgic_J2 = (2*J2iso[i]+ J2plane[i] + J2z[i])/2
       Belgic_J3 = (2*J3iso[i]+ J3plane[i] + J3z[i])/2
       #print(Belgic_J1,J1iso[i],J1plane[i],J1z[i])


       # lets avoid small numbers 
       J1num1 = (J1iso[i] + J1z[i])*1000;J2num1 = (J2iso[i] + J2z[i])*1000;J3num1 = (J3iso[i] + J3z[i])*1000
       J1num2 = (J1iso[i] + J1plane[i])*1000;J2num2 = (J2iso[i] + J2plane[i])*1000;J3num2 = (J3iso[i] + J3plane[i])*1000
       J1den = 2*Belgic_J1*1000;J2den = 2*Belgic_J2*1000;J3den = 2*Belgic_J3*1000
       Belgic_Delta1 = (J1num1-J1num2)/J1den;Belgic_Delta2 = (J2num1-J2num2)/J2den;Belgic_Delta3 = (J3num1-J3num2)/J3den
     #  if Belgic_Delta1 > 1:
     #     Belgic_Delta1 = 1
     #  if Belgic_Delta1 < -1:
     #     Belgic_Delta1 = -1       
     #  if Belgic_Delta2 > 1:
     #     Belgic_Delta2 = 1
     #  if Belgic_Delta2 < -1:
     #     Belgic_Delta2 = -1     
     #  if Belgic_Delta3 > 1:
     #     Belgic_Delta3 = 1
     #  if Belgic_Delta3 < -1:
     #     Belgic_Delta3 = -1 
 
      # if Belgic_Delta1 > 1:
      #    Belgic_Delta1 = 'no conv'
      # if Belgic_Delta1 < -1:
      #    Belgic_Delta1 = 'no conv'       
      # if Belgic_Delta2 > 1:
      #    Belgic_Delta2 = 'no conv'
      # if Belgic_Delta2 < -1:
      #    Belgic_Delta2 = 'no conv'     
      # if Belgic_Delta3 > 1:
      #    Belgic_Delta3 = 'no conv'
      # if Belgic_Delta3 < -1:
      #    Belgic_Delta3 = 'no conv'       
       #Belgic_Delta1 = ((J1iso[i] + J1z[i])-(J1iso[i] + J1plane[i]))/(2*Belgic_J1)
       #Belgic_Delta2 = ((J2iso[i] + J2z[i])-(J2iso[i] + J2plane[i]))/(2*Belgic_J2)
       #Belgic_Delta3 = ((J3iso[i] + J3z[i])-(J3iso[i] + J3plane[i]))/(2*Belgic_J3)
       #print(Belgic_Delta1,(J1z[i]-J1plane[i])/(2*Belgic_J1))
       #print(J1iso[i],J2iso[i],J3iso[i],'/n',J1x[i],J2x[i],J3x[i],'/n',J1y[i],J2y[i],J3y[i],'/n',J1z[i],J2z[i],J3z[i],'/n',J1plane[i],J2plane[i],J3plane[i],'/n',Belgic_J1,Belgic_J2,Belgic_J3,'/n',Belgic_Delta1,Belgic_Delta2,Belgic_Delta3)
       Belgic_Delta1 = (f"{Belgic_Delta1:.16f}")
       Belgic_Delta2 = (f"{Belgic_Delta2:.16f}")
       Belgic_Delta3 = (f"{Belgic_Delta3:.16f}")
       Belgic_J1 = (f"{Belgic_J1:.16f}")
       Belgic_J2 = (f"{Belgic_J2:.16f}")
       Belgic_J3 = (f"{Belgic_J3:.16f}")
       Belgic_J1_vector = np.append(Belgic_J1_vector,Belgic_J1)
       Belgic_J2_vector = np.append(Belgic_J2_vector,Belgic_J2)
       Belgic_J3_vector = np.append(Belgic_J3_vector,Belgic_J3)
       Belgic_Delta1_vector = np.append(Belgic_Delta1_vector,Belgic_Delta1)
       Belgic_Delta2_vector = np.append(Belgic_Delta2_vector,Belgic_Delta2)  
       Belgic_Delta3_vector = np.append(Belgic_Delta3_vector,Belgic_Delta3)
      # for index in np.arange(0,len(Belgic_Delta1_vector),1):
      #      if Belgic_Delta1_vector[index] == 'no conv':
      #          Belgic_Delta1_vector[index] = (Belgic_Delta1_vector[index-1] + Belgic_Delta1_vector[index+1])/2
      # for index in np.arange(0,len(Belgic_Delta2_vector),1):
      #      if Belgic_Delta2_vector[index] == 'no conv':
      #          Belgic_Delta2_vector[index] = (Belgic_Delta2_vector[index-1] + Belgic_Delta2_vector[index+1])/2
      # for index in np.arange(0,len(Belgic_Delta3_vector),1):
      #      if Belgic_Delta3_vector[index] == 'no conv':
      #          Belgic_Delta3_vector[index] = (Belgic_Delta3_vector[index-1] + Belgic_Delta3_vector[index+1])/2

        
       #print(Belgic_Delta1,Belgic_Delta2,Belgic_Delta3,Belgic_J1,Belgic_J2,Belgic_J3,strain[i],U[i])
       Tc = run(['python3', '../QuantumTools/strain_and_U_calculate_curie.py','-l', 'hon','-out', './curie.txt','-S',str(spin),'-st',str(strain[i]),'-u',str(U[i]),'-D', str(Belgic_Delta1),str(Belgic_Delta2),str(Belgic_Delta3),'-J',str(Belgic_J1),str(Belgic_J2),str(Belgic_J3)],capture_output=True)
       
       #Tc = 'phi_C The negative. temperature is 5'
       #print(str(Tc) +'/n')
       output = Tc.stdout
       Tc = output.decode("utf-8")
       Tc = Tc.split()
       #print(Tc)
       if Tc[0] == 'phi_C':
            print('\n' + 'phi case ' + str(Tc) + '\n')
            print(str(Tc) + '\n')
            #print(J1iso[i],J1x[i],J1z[i])
            Tc = np.nan
       elif Tc[1] == 'Curie':
            Tc = float(Tc[4])
       elif Tc[2] == 'negative.':
            print('\n' + 'negative case ' + str(Tc) + '\n')
            print(str(Tc) + '\n')
            
            #print(J1iso[i],J1x[i],J1z[i])
            Tc = np.nan
       else:   
            counter = counter + 1
            #print('python3', '../QuantumTools/strain_and_U_calculate_curie.py','-l', 'hon','-out', './curie.txt','-S',str(spin),'-st',str(strain[i]),'-u',str(U[i]),'-D', str(Belgic_Delta1),str(Belgic_Delta2),str(Belgic_Delta3),'-J',str(Belgic_J1),str(Belgic_J2),str(Belgic_J3))
            print('case out of the model', Belgic_Delta1,Belgic_Delta2,Belgic_Delta3,Belgic_J1,Belgic_J2,Belgic_J3,strain[i],U[i])
            #print(str(Tc) +'/n')
            #print(Belgic_J3,'(2*' + str(J3iso[i]) + '+' + str(J3plane[i])  + '+' + str(J3z[i]) + ')/2')
            #print(Belgic_Delta3,'(' + str(J3iso[i]) + '+' + str(J3z[i])  + ')-(' + str(J3iso[i]) + '+'+ str(J3plane[i]) + ')/(2*' + Belgic_J3 + ')')
            #print(J1iso[i],J1x[i],J1z[i])
            #Tc = np.nan  
            Tc = np.nan         
       #print(str(Tc) )
       Tc_vector = np.append(Tc_vector,Tc)
       #print( Belgic_Delta1,Belgic_Delta2,Belgic_Delta3,Belgic_J1,Belgic_J2,Belgic_J3,strain[i],U[i],Tc)
       print( strain[i],U[i],Tc)
    #print(Tc_vector)
    Tc_file.close()
    #print(len(strain),len(U),len(Belgic_Delta1_vector),len(Belgic_J1_vector),len(Belgic_Delta2_vector),len(Belgic_J2_vector),len(Belgic_Delta3_vector),len(Belgic_J3_vector),len(Tc_vector))
    np.savetxt(prefix + '.belgium_exchange_and_Curie.txt', np.c_[strain,U,Belgic_J1_vector,Belgic_J2_vector,Belgic_J3_vector,Belgic_Delta1_vector,Belgic_Delta2_vector,Belgic_Delta3_vector,Tc_vector], fmt="%s", delimiter=' ')
    map_file = open(prefix + '.Curie_map.txt', 'w')
    Tc_matrix = np.array([[]])
    new_str_len = int((strmax-strmin)/poly_str_mesh)
    new_U_len = int((Umax-Umin)/poly_U_mesh)
    Tc_matrix =Tc_vector.reshape(new_U_len+1, new_str_len+1)
    np.savetxt(map_file,Tc_matrix, fmt="%s", delimiter=' ')
    #print(Tc_matrix)
    map_file.close()
    print('Final countdown:   ' + str(counter))
    return new_str_len
def Plot_3D_map(strmax,strmin,poly_str_mesh,Umax,Umin,poly_U_mesh,T0):
    """
    Plots the heat map
    """
    new_str_len  = int((strmax-strmin)/poly_str_mesh)
    new_U_len = int((Umax-Umin)/poly_U_mesh)
    map_file = open(prefix + '.Curie_map.txt', 'r')
    arr = np.loadtxt(map_file , usecols=np.arange(0,new_str_len + 1))
    #for index1 in np.arange(0,new_str_len,1):
    #   for index2 in np.arange(0,new_U_len,1):
    #       if arr[index1][index2] == 'no conv':
    #          arr[index1][index2] = (arr[index1+1][index2] + arr[index1][index2+1] + arr[index1-1][index2] + arr[index1][index2-1])/4

    arr2 = arr - T0
    print(arr2)
    arr2 = np.ma.masked_where(np.isnan(arr2), arr2)   
    fig, ax = plt.subplots()
    #fig = plt.imshow(arr2, cmap='seismic', interpolation='none',origin='lower',vmin=-10,vmax=10, aspect='auto') #CC
    fig = plt.imshow(arr2, cmap='seismic', interpolation='none',origin='lower',vmin=-23,vmax=13, aspect='auto') #CB
    #fig = plt.imshow(arr2, cmap='seismic', interpolation='none',origin='lower',vmin=-42,vmax=20, aspect='auto') #CI
    ax.set_yticks([0, new_U_len/4, new_U_len/2, new_U_len*3/4, new_U_len])
    ax.set_xticks([0,new_str_len/10,new_str_len*2/10,new_str_len*3/10,new_str_len*4/10,new_str_len*5/10,new_str_len*6/10,new_str_len*7/10,new_str_len*8/10,new_str_len*9/10,new_str_len])
    y_label_list = ['2','3','4','5','6']
    x_label_list = ['-5', '-4', '-3', '-2', '-1', '0','1', '2', '3', '4', '5']
    ax.set_xticklabels(x_label_list)
    ax.set_yticklabels(y_label_list) 
    plt.ylabel('U (eV)', fontsize=20)
    plt.xlabel('Strain (%)', fontsize=20)
    cb = plt.colorbar(fig, orientation="vertical", pad=0.2)
    cb.set_label(label='Tc (K)', size='x-large', weight='bold')
    cb.ax.tick_params(labelsize='x-large')
    plt.show()
def poli_plot_tester(strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,J_label):
    x0,a,b,c,d,e = poly_magic(prefix,J_label)
    plotter_vs_U(x0,a,b,c,d,e,strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,J_label)
    plotter_vs_strain(x0,a,b,c,d,e,strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,J_label)
def perform_full_poly_calculation(strmax,strmin,Umax,Umin,prefix,poly_str_mesh,poly_U_mesh,J_label):   
    x0,a,b,c,d,e = poly_magic(prefix,J_label)
    poly_calculator(x0,a,b,c,d,e,strmax,strmin,poly_str_mesh,Umax,Umin,poly_U_mesh,prefix,J_label) 
def perfom_full_Curie_calculation(prefix,spin,strmax,strmin,poly_str_mesh,Umax,Umin,poly_U_mesh,T0):
    calculate_curie(prefix,spin)
    Plot_3D_map(strmax,strmin,poly_str_mesh,Umax,Umin,poly_U_mesh,T0)
def banana_based_poli(prefix,strmax,strmin,strnstep,Umax,Umin,Unstep):
    U_vector = np.array([])
    for strain in np.arange(strmin,strmax,strnstep):
        if prefix == 'crcl3':
            U = 0.0012 * strain * strain - 0.2126 * strain + 12.922
        if prefix == 'crbr3':
            U = 0.0018 * strain * strain - 0.3246 * strain + 18.369
        if prefix == 'cri3':
            U = 0.0027 * strain * strain - 0.4645 * strain + 24.392
        U_vector = np.append(U_vector,U)
    
if __name__ == '__main__':
    prefix = 'crbr3'
    spin =1.5
    #T0 = 23 # crcl3
    T0 = 55.3 #crbr3
    #T0 = 94.22 # cri3
    plt.rcParams['figure.max_open_warning'] = 0
    #definitive 16k
    #strmax = 105; strmin = 95; strnstep = 1; Umax = 6.0; Umin = 2.0; Unstep =  1.0; poly_str_mesh = 0.05 ; poly_U_mesh = 0.05
        #test 4k
    strmax = 105; strmin = 95; strnstep = 1; Umax = 6.0; Umin = 2.0; Unstep =  1.0; poly_str_mesh = 0.1 ; poly_U_mesh = 0.1
        #test lessk
    #strmax = 105; strmin = 95; strnstep = 1; Umax = 6.0; Umin = 2.0; Unstep =  1.0; poly_str_mesh = 0.03 ; poly_U_mesh = 0.03
    #inputdir = parser()
    #format_input(prefix,strmax,strmin,strnstep,Umax,Umin,Unstep)

    #poli_plot_tester(strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,'J1iso')
    #poli_plot_tester(strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,'J1x')
    #poli_plot_tester(strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,'J1y')
    #poli_plot_tester(strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,'J1z')
    #poli_plot_tester(strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,'J2iso')
    #poli_plot_tester(strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,'J2x')
    #poli_plot_tester(strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,'J2y')
    #poli_plot_tester(strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,'J2z')
    #poli_plot_tester(strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,'J3iso')
    #poli_plot_tester(strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,'J3x')
    #poli_plot_tester(strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,'J3y')
    #poli_plot_tester(strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,'J3z')

    perform_full_poly_calculation(strmax,strmin,Umax,Umin,prefix,poly_str_mesh,poly_U_mesh,'J1iso')
    perform_full_poly_calculation(strmax,strmin,Umax,Umin,prefix,poly_str_mesh,poly_U_mesh,'J1x')
    perform_full_poly_calculation(strmax,strmin,Umax,Umin,prefix,poly_str_mesh,poly_U_mesh,'J1y')
    perform_full_poly_calculation(strmax,strmin,Umax,Umin,prefix,poly_str_mesh,poly_U_mesh,'J1z')
    perform_full_poly_calculation(strmax,strmin,Umax,Umin,prefix,poly_str_mesh,poly_U_mesh,'J2iso')
    perform_full_poly_calculation(strmax,strmin,Umax,Umin,prefix,poly_str_mesh,poly_U_mesh,'J2x')
    perform_full_poly_calculation(strmax,strmin,Umax,Umin,prefix,poly_str_mesh,poly_U_mesh,'J2y')
    perform_full_poly_calculation(strmax,strmin,Umax,Umin,prefix,poly_str_mesh,poly_U_mesh,'J2z')
    perform_full_poly_calculation(strmax,strmin,Umax,Umin,prefix,poly_str_mesh,poly_U_mesh,'J3iso')
    perform_full_poly_calculation(strmax,strmin,Umax,Umin,prefix,poly_str_mesh,poly_U_mesh,'J3x')
    perform_full_poly_calculation(strmax,strmin,Umax,Umin,prefix,poly_str_mesh,poly_U_mesh,'J3y')
    perform_full_poly_calculation(strmax,strmin,Umax,Umin,prefix,poly_str_mesh,poly_U_mesh,'J3z')
    perfom_full_Curie_calculation(prefix,spin,strmax,strmin,poly_str_mesh,Umax,Umin,poly_U_mesh,T0)
