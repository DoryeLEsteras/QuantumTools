import os
import re
from typing import List
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import numpy as np

def parser():
    parser = ArgumentParser(description="Script to plot pdos")
    parser.add_argument("-inputdir", "--inputdir",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the input directory
                        """)
    args = parser.parse_args()
    return args.inputdir
    
def find_files(inputdir:str):
    dir_list = os.listdir(inputdir)
    pattern = re.compile(r'(\w*\.pdos_tot\.pdos_atm\#\d\(([A-Z]?[a-z]?)\d?\)_wfc\#\d*\((\w)\))',re.IGNORECASE)
    atom_list = [];orbital_list = [];file_list = []
    for file_name in dir_list:
        results_search = pattern.search(str(file_name))
        if results_search != None:
            file_list.append(results_search.group(1))
            atoms = results_search.group(2)
            orbitals = results_search.group(3)
            if atoms not in atom_list:
               atom_list.append(atoms)
            if orbitals not in orbital_list:
               orbital_list.append(orbitals)
    return file_list, atom_list, orbital_list

def read_columns(file_name_and_dir:str,orbital_label:str):
    number_of_columns = orbitals_nosoc_dim[orbital_label]
    data = np.loadtxt(file_name_and_dir)[:, 0]
    for column in range(1,number_of_columns):
        data = np.vstack((data,np.loadtxt(file_name_and_dir)[:,column]))
    return data

def sum_atoms(file_list:List,atom_list:List,orbital_list:List,inputdir:str):
    for f in file_list:
        if '(s)' in str(f): 
            data_matrix_s = np.empty_like(read_columns(os.path.join(inputdir, str(f)),'s'))
        if '(p)' in str(f): 
            data_matrix_p = np.empty_like(read_columns(os.path.join(inputdir, str(f)),'p'))
        if '(d)' in str(f): 
            data_matrix_d = np.empty_like(read_columns(os.path.join(inputdir, str(f)),'d'))
        if '(f)' in str(f): 
            data_matrix_f = np.empty_like(read_columns(os.path.join(inputdir, str(f)),'f'))

    for atom in atom_list:
        for f in file_list:
            if '(' + str(atom) in str(f) and '(s)' in str(f):
                   data_matrix_s = data_matrix_s + read_columns(os.path.join(inputdir, str(f)),'s')
            if '(' + str(atom) in str(f) and '(p)' in str(f):
                   data_matrix_p = data_matrix_p + read_columns(os.path.join(inputdir, str(f)),'p')
            if '(' + str(atom) in str(f) and '(d)' in str(f):
                   data_matrix_d = data_matrix_d + read_columns(os.path.join(inputdir, str(f)),'d')
            if '(' + str(atom) in str(f) and '(f)' in str(f):     
                   print(f)                 
                   data_matrix_f = data_matrix_f + read_columns(os.path.join(inputdir, str(f)),'f')
                   data_matrix_f[0,:] = read_columns(os.path.join(inputdir, str(f)), 'f')[0]
    print(data_matrix_f)
    return data_matrix_f      

def plot_f_orbitals(data_to_plot:List):
    figtot,ax = plt.subplots(1,1,figsize=[12,5]) 
    ax.plot(data_to_plot[0],data_to_plot[3],'-', color='pink',label='m = -3')
    ax.plot(data_to_plot[0],data_to_plot[5],'-', color='red',label='m = -2')
    ax.plot(data_to_plot[0],data_to_plot[7],'-', color='blue',label='m = -1')
    ax.plot(data_to_plot[0],data_to_plot[9],'-', color='green',label='m = 0')
    ax.plot(data_to_plot[0],data_to_plot[11],'-', color='cyan',label='m = 1')
    ax.plot(data_to_plot[0],data_to_plot[13],'-', color='yellow',label='m = 2')
    ax.plot(data_to_plot[0],data_to_plot[15],'-', color='purple',label='m = 3')
    ax.plot(data_to_plot[0],-data_to_plot[4],'-', color='pink')
    ax.plot(data_to_plot[0],-data_to_plot[6],'-', color='red')
    ax.plot(data_to_plot[0],-data_to_plot[8],'-', color='blue')
    ax.plot(data_to_plot[0],-data_to_plot[10],'-', color='green')
    ax.plot(data_to_plot[0],-data_to_plot[12],'-', color='cyan')
    ax.plot(data_to_plot[0],-data_to_plot[14],'-', color='yellow')
    ax.plot(data_to_plot[0],-data_to_plot[16],'-', color='purple')
    ax.set_ylabel(r'PDOS (states/eV)',fontsize = 20)
    ax.set_xlabel(r'Energy (eV)',fontsize = 20)
    ax.axhline(y=0.0, color='black', linestyle='--')
    ax.tick_params(axis='both',  labelsize=15)
    ax.set_xlim(-15, 5.0)
    ax.set_ylim(-50, 50.0)
    figtot.subplots_adjust(bottom=0.2)
    figtot.subplots_adjust(left=0.2)
    ax.legend()
    plt.show()



if __name__ == "__main__":
    orbitals_nosoc_dim= {
     's': 4, 
     'p': 8,
     'd': 12,
     'f': 17,
    }


    inputdir = parser()
    file_list,atom_list,orbital_list = find_files(inputdir)
    to_plot = sum_atoms(file_list,atom_list,orbital_list,inputdir)
    plot_f_orbitals(to_plot)