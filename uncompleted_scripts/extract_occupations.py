import numpy as np
from argparse import ArgumentParser

# TO DO LIST
"""
Meter la U

"""

def parser():
    parser = ArgumentParser(description="")
    parser.add_argument("-inputdir", "--inputdir",
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
    return args.inputdir,args.out

def extract_occupations(scfout_file,output_file):
    counter = 0; nmag = 2; occ_matrix = np.zeros((5*nmag, 5*nmag)); occ_vector = []
    readed_scfout_file = open(str(scfout_file), 'r')
    readed_file = readed_scfout_file.readlines()
    for line in readed_file:
        counter = counter + 1
        line = line.split()
        line.append('end')
        keyword = line[0]
        if keyword == 'occupations,':
            occ_vector =[]
            for selected_line in range(0,5*nmag,1):
                line = readed_file[selected_line + counter]
                line = line.split()
                counter2 = -1
                for term in line:
                    counter2 = counter2 + 1
                    occ_matrix[selected_line][counter2] = term   
                occ_vector.append(occ_matrix[selected_line][selected_line])             
    for component in occ_vector:
        output_file.write(' ' + str(component))    
    readed_scfout_file.close() 

def create_strain_files(strmax,strmin,strnstep,prefix,scfout_dir,U,provided_output_dir):   
    output_file_strain = provided_output_dir  + 'U_' + str(U)
    output_file_strain = open(str(output_file_strain), 'w')
    for strain in np.arange(strmin,strmax+1,strnstep):
        file_name = str(prefix) + '.' + str(strain) + '.' + 'z' + '.' + str(U) + '.' + 'scf.out' 
        scfout_file = scfout_dir + file_name 
        output_file_strain.write(str(strain) + ' ')
        extract_occupations(scfout_file,output_file_strain) 
        output_file_strain.write('\n')  
    output_file_strain.close()   
  


prefix = 'cri3'
strmax,strmin,strnstep = 105,95,1 
Umax,Umin,Unstep = 6.0,2.0,1.0 

scfout_file, provided_output_dir = parser()
  
for U in np.arange(Umin,Umax+1,Unstep):
    create_strain_files(strmax,strmin,strnstep,prefix,scfout_file,U,provided_output_dir)
