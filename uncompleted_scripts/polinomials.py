import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# To Do List
"""
Prepare inferface with real J inputs
Include the massive 3D plot
Plot gifures with lines
"""
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
    plotter_vs_U(x0,a,b,c,d,e,strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,J_label)
    plotter_vs_strain(x0,a,b,c,d,e,strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,J_label)
    poly_calculator(x0,a,b,c,d,e,strmax,strmin,poly_str_mesh,Umax,Umin,poly_U_mesh,prefix,J_label) 

if __name__ == '__main__':
    prefix = 'crcl3'
    strmax = 105;strmin = 95;strnstep = 1;Umax = 6;Umin = 2;Unstep =  1; poly_str_mesh = 1 ; poly_U_mesh = 1
    perform_full_calculation(strmax,strmin,strnstep,Umax,Umin,Unstep,prefix,poly_str_mesh,poly_U_mesh,'J1','J1.txt')

    
