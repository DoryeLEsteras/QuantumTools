import numpy as np
from argparse import ArgumentParser
import re
import math

"""
 to do list
 loop it
 extract atm pos dangerous
"""

def parser():
    parser = ArgumentParser(description="Script for creating SpinW input files")
    parser.add_argument("-scf", "--scf",
                        type=str,
                        required=False,
                        help="""
                        Relative or absulute path to the scf input file,
                        including the name and extention of the file itself.
                        """)
    parser.add_argument("-op", "--output-dir",
                        type=str,
                        default='.',
                        help="""
                        Relative or absolute path for the output file
                        """)
    parser.add_argument("-ex", "--exchange",
                        type=str,
                        required=True,
                        default='exchange',
                        help="Seedname for the output files.")
    parser.add_argument("-U", "--U",
                        type=float,
                        required=True,
                        help="Hubbard U")
    parser.add_argument("-strain", "--strain",
                        type=float,
                        required=True,
                        help="Strain prefix.")
    parser.add_argument("-n", "--n",
                        type=str,
                        required=True,
                        nargs='+',
                        help="n1 n2 n3 n4 n5 n6 for number of neighbours in exchange file ")
    args = parser.parse_args()
    return  args.output_dir,args.exchange, args.U, args.strain,args.n


def readblock_resolved_soc(Jiso,Jorb,Jani,DMI,input_file):
    readed_line = input_file.readline()
    readed_line = readed_line.replace("(", "")
    readed_line = readed_line.replace(")", "")
    readed_line = readed_line.replace(",", "")
    readed_line = readed_line.split()
    Label_atom_1 = readed_line[0]
    Label_atom_1 = re.sub('[^0-9]','',Label_atom_1)
    Label_atom_2 = readed_line[1]
    Label_atom_2 = re.sub('[^0-9]','',Label_atom_2)
    NN_vector = np.array([int(readed_line[2]),int(readed_line[3]),int(readed_line[4])])
    Jiso =  float(readed_line[5])
    input_file.readline()
    readed_line = input_file.readline()
    readed_line = readed_line.replace("(", "")
    readed_line = readed_line.replace(")", "")
    readed_line = readed_line.replace(",", "")
    readed_line = readed_line.split()
    DMI = np.array([float(readed_line[2]),float(readed_line[3]),float(readed_line[4])])
    input_file.readline()
    readed_line1 = input_file.readline()
    readed_line1 = readed_line1.replace("[", "")
    readed_line1 = readed_line1.replace("]", "")
    readed_line1 = readed_line1.split()
    readed_line2 = input_file.readline()
    readed_line2 = readed_line2.replace("[", "")
    readed_line2 = readed_line2.replace("]", "")
    readed_line2 = readed_line2.split()
    readed_line3 = input_file.readline()
    readed_line3 = readed_line3.replace("[", "")
    readed_line3 = readed_line3.replace("]", "")
    readed_line3 = readed_line3.split()
    Jani = np.matrix([ [ float(readed_line1[0]), \
    + float(readed_line1[1]),float(readed_line1[2])], [ float(readed_line2[0]),\
     float(readed_line2[1]),float(readed_line2[2])],\
     [float(readed_line3[0]),float(readed_line3[1]),float(readed_line3[2])]])
    input_file.readline()    
    input_file.readline()
    readed_line1 = input_file.readline()
    readed_line1 = readed_line1.replace("[", "")
    readed_line1 = readed_line1.replace("]", "")
    readed_line1 = readed_line1.split()
    readed_line2 = input_file.readline()
    readed_line2 = readed_line2.replace("[", "")
    readed_line2 = readed_line2.replace("]", "")
    readed_line2 = readed_line2.split()
    readed_line3 = input_file.readline()
    readed_line3 = readed_line3.replace("[", "")
    readed_line3 = readed_line3.replace("]", "")
    readed_line3 = readed_line3.split()
    readed_line4 = input_file.readline()
    readed_line4 = readed_line4.replace("[", "")
    readed_line4 = readed_line4.replace("]", "")
    readed_line4 = readed_line4.split()
    readed_line5 = input_file.readline()
    readed_line5 = readed_line5.replace("[", "")
    readed_line5 = readed_line5.replace("]", "")
    readed_line5 = readed_line5.split()
    Jorb = np.matrix([ [ float(readed_line1[0]), float(readed_line1[1]),float(readed_line1[2]),float(readed_line1[3]),float(readed_line1[4])], [ float(readed_line2[0]), float(readed_line2[1]),float(readed_line2[2]),float(readed_line2[3]),float(readed_line2[4])], [float(readed_line3[0]),float(readed_line3[1]),float(readed_line3[2]),float(readed_line3[3]),float(readed_line3[4])],[ float(readed_line4[0]), float(readed_line4[1]),float(readed_line4[2]),float(readed_line4[3]),float(readed_line4[4])],[ float(readed_line5[0]), float(readed_line5[1]),float(readed_line5[2]),float(readed_line5[3]),float(readed_line5[4])]])
    Jani = np.array([Jani.item((0, 0)),Jani.item((1, 1)),Jani.item((2, 2))])
    for i in range(1, 74, 1):
        #print(input_file.readline())
        input_file.readline()
    return Jiso,Jani,DMI,Jorb,Label_atom_1,Label_atom_2,NN_vector
def data_extractor(prefix,spin,angle1_lattice,angle2_lattice,angle3_lattice,SIA,SWinput_directory,tb2j_extracted_results_directory,n):
    Jiso = 0;Jani = np.zeros((3, 3));DMI = np.array([0,0,0]);Jorb = np.zeros((5, 5))
    line = fileTB2J.readline()
    while line != 'Cell (Angstrom):\n':
        line = fileTB2J.readline()
    a = fileTB2J.readline()
    a = a.split()
    a = float(a[0])
    b = a
    fileTB2J.readline()
    c = fileTB2J.readline()
    c = c.split()
    c = float(c[2])
    while line != 'Atoms:  \n':
        line = fileTB2J.readline()
    line = fileTB2J.readline()
    line = fileTB2J.readline()
    at_pos = fileTB2J.readline()   
    at_pos = at_pos.split()
    if at_pos[0] == 'Cr1' or at_pos[0] == 'Cr2':
        #at1 = np.array([float(float(at_pos[1])+factora)/a,float(at_pos[2])/factorb,float(at_pos[3])/c])
        at1 =np.array([0,0,float(at_pos[3])/c])
    at_pos = fileTB2J.readline()   
    at_pos = at_pos.split()
    if at_pos[0] == 'Cr1' or at_pos[0] == 'Cr2':
        #at2 = np.array([(float(at_pos[1])+factora)/a,float(at_pos[2])/factorb,float(at_pos[3])/c])
        at2 =np.array([0.333333,0.6666667,float(at_pos[3])/c])
    while line != 'Exchange: \n':
        line = fileTB2J.readline()
    fileTB2J.readline()
    fileTB2J.readline()
    number_neighbors = int(len(n)) 
    nn = 0 
    for i in range(0,len(n),1):
        nn = int(n[int(i)]) + int(nn)
    Jiso_vector = np.array([]);Jani_matrix = np.zeros((nn,3));DMI_matrix = np.zeros((nn,3)); counter = 0
    NN_matrix = np.zeros((nn,3));Label_atom_1_vector = [];Label_atom_2_vector = [];Jiso_mean = np.array([]); Jmean = 0;Label_exchange_vector=[]
    for index in range(0,number_neighbors,1):
        ni = int(n[index])   
        for index2 in range(0,ni,1):
            Jiso,Jani,DMI,Jorb,Label_atom_1,Label_atom_2,NN_vector = readblock_resolved_soc(Jiso,Jorb,Jani,DMI,fileTB2J)
            Jiso_vector = np.append(Jiso_vector,Jiso)
            Jmean = Jiso + Jmean
            Jani_matrix[counter][0] = Jani[0];Jani_matrix[counter][1] = Jani[1];Jani_matrix[counter][2] = Jani[2]
            DMI_matrix[counter][0] = DMI[0];DMI_matrix[counter][1] = DMI[1];DMI_matrix[counter][2] = DMI[2]
            NN_matrix[counter][0] = NN_vector[0];NN_matrix[counter][1] = NN_vector[1];NN_matrix[counter][2] = NN_vector[2]
            Label_atom_1_vector.append(Label_atom_1) 
            Label_atom_2_vector.append(Label_atom_2)
            Label_exchange = str(index+1) + "_" +str(index2+1)
            Label_exchange_vector.append(Label_exchange)
            counter = counter +1 
        Jiso_mean = np.append(Jiso_mean,Jmean/ni) 
        Jmean = 0
    clean_indices = np.array([]);clean_label_exchange_vector = []
    for index_vector_to_compare in range(0,len(Label_atom_1_vector),1):
        for index in range(index_vector_to_compare + 1,len(Label_atom_1_vector),1):
            #print(index_vector_to_compare,index)
            if np.array_equal(NN_matrix[index_vector_to_compare][:],-NN_matrix[index][:]) == True and Label_atom_1_vector[index_vector_to_compare] == Label_atom_2_vector[index] and Label_atom_2_vector[index_vector_to_compare] == Label_atom_1_vector[index]:
                clean_indices = np.append(clean_indices,index_vector_to_compare)

# Soy muy consciente de que esto es muy refactorizable. Basicamente empece el codigo contando 
#dos veces todos las interacciones. Deberia ser tan facil como subir arriba y comenzar con
# ni -> ni/2 y derivados, pero estoy cansado y tengo que seguri adelante. Por ahora estas
# lineas reescriben los indices y funcionan
    clean_Jani_matrix = np.array([[]]);clean_DMI_matrix = np.array([[]]);clean_NN_matrix = np.array([[]])
    clean_label_atom_1_vector = [];clean_label_atom_2_vector = [];clean_Label_exchange_vector = []
    for i in clean_indices:
        clean_Jani_matrix = np.append(clean_Jani_matrix,Jani_matrix[int(i), :] )
        clean_DMI_matrix = np.append(clean_DMI_matrix,DMI_matrix[int(i), :] )
        clean_NN_matrix = np.append(clean_NN_matrix,NN_matrix[int(i), :])
        clean_label_atom_1_vector.append(Label_atom_1_vector[int(i)])
        clean_label_atom_2_vector.append(Label_atom_2_vector[int(i)])
    clean_NN_matrix =np.resize(clean_NN_matrix,(len(clean_indices),3))
    clean_DMI_matrix =np.resize(clean_DMI_matrix,(len(clean_indices),3))
    clean_Jani_matrix =np.resize(clean_Jani_matrix,(len(clean_indices),3))
    for index in range(0,number_neighbors,1):
        ni = int(n[index])   
        for index2 in range(0,int(ni/2),1):
            clean_Label_exchange = str(index+1) + "_" +str(index2+1)
            clean_Label_exchange_vector.append(clean_Label_exchange)
    return a,b,c,at1,at2,Jiso_vector,Jiso_mean,clean_Jani_matrix,clean_DMI_matrix,clean_NN_matrix,clean_label_atom_1_vector,clean_label_atom_2_vector,nn,number_neighbors,clean_Label_exchange_vector
def createSW(prefix,fileSW,a,b,c,at1,at2,Jiso_vector,Jiso_mean,Jani_matrix,DMI_matrix,NN_matrix,Label_atom_1_vector,Label_atom_2_vector,nn,number_neighbors,U,strain,Label_exchange_vector):
    nn = int(nn/2)   # esto es el parche a la falta de refactorizacion, seria muy simple de arreglar! Pero estoy petado
    fileSW.write("clc\n")
    fileSW.write("clear class\n")
    fileSW.write(prefix + "=spinw;\n")
    fileSW.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%crystal and magnetic stucture%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
    fileSW.write(prefix + ".genlattice('lat_const',[" + str(a)+ " " + str(b) + " " + str(c) +"]);\n")
    fileSW.write(prefix + ".genlattice('angled',[" + str(angle1_lattice) + " " + str(angle2_lattice) + " " + str(angle3_lattice) + "]);\n")
    fileSW.write(prefix + ".addatom('label','Cr','r',[" + str(at1[0]) +  " " + str(at1[1]) +  " " + str(at1[2]) + "],'S',"+ str(spin) + " , 'color', 'red');\n")
    fileSW.write(prefix + ".addatom('label','Cr','r',[" + str(at2[0]) +  " " + str(at2[1]) +  " " + str(at2[2]) + "],'S',"+ str(spin) +", 'color', 'red');\n")
    fileSW.write(prefix + ".gencoupling('maxDistance',10);\n")
    fileSW.write(prefix + ".genmagstr('mode','helical','k',[0 0 0], 'n', [0 0 1],'S',[0; 0; 1]);\n")
    fileSW.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Exchange Hamiltonian%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
    fileSW.write(" f = -0.5\n")
    fileSW.write(prefix + ".addmatrix('label','D','value',diag([0 0 " + str(SIA) + "]*f))\n")
    for i in range(0,number_neighbors,1):   
        fileSW.write(prefix + ".addmatrix('label','J" + str(i + 1) + "iso','value', " + str(Jiso_vector[i]) + "*f,'color','b')\n")
    for i in range(0,nn,1):
        fileSW.write(prefix + ".addmatrix('label','J" + str(Label_exchange_vector[i]) + "ani','value', [" + " " + str(Jani_matrix[i][0]) +\
         " " +  '0' + " " + '0' + ";" + " " + '0' + " " + str(Jani_matrix[i][1]) + " " + '0' + " " + ";" + " " + '0' + " " +  '0' + " " + str(Jani_matrix[i][2]) + " " + "]*f,'color','b')\n")
    for i in range(0,nn,1):        
        fileSW.write(prefix + ".addmatrix('label','DM" + str(Label_exchange_vector[i]) + "','value', [" + " " + str(DMI_matrix[i][0]) + " " +  str(DMI_matrix[i][1]) + " " + str(DMI_matrix[i][2]) + " " + "]*f,'color','b')\n")
    fileSW.write(prefix + ".addaniso('D');\n")
    for i in range(0,nn,1):
        fileSW.write(prefix + ".addmatrix('label','J" + str(Label_exchange_vector[i]) + "ani','value', [" + " " + str(Jani_matrix[i][0]) +\
         " " +  '0' + " " + '0' + ";" + " " + '0' + " " + str(Jani_matrix[i][1]) + " " + '0' + " " + ";" + " " + '0' + " " +  '0' + " " + str(Jani_matrix[i][2]) + " " + "]*f,'color','b')\n")
    for i in range(0,number_neighbors,1):  
        fileSW.write(prefix + ".addcoupling('mat','J" + str(i+1) +"iso','bond'," + str(i+1) + ")\n")        
    for i in range(0,nn,1):
        number = str(Label_exchange_vector[i]).split('_')
        index = number[0]  
        subindex = number[1]
        fileSW.write(prefix + ".addcoupling('mat','J" + str(Label_exchange_vector[i]) + "ani','bond'," + str(index) + ",'subidx'," + str(subindex) + ")\n" )
    for i in range(0,nn,1):
        number = str(Label_exchange_vector[i]).split('_')
        index = number[0]  
        subindex = number[1]
        fileSW.write(prefix + ".addcoupling('mat','DM" + str(Label_exchange_vector[i]) + "','bond'," + str(index) + ",'subidx',"  + str(subindex) + ")\n" )  
    for i in range(0,nn,1):
        fileSW.write(prefix + ".coupling.dl(:," + str(i + 1) + ")=[" +  str(int(NN_matrix[i][0])) + " " +  str(int(NN_matrix[i][1])) + " " +  str(int(NN_matrix[i][2])) +"];\n")
        fileSW.write(prefix + ".coupling.atom1("+ str(i + 1)+ ")=" + str(Label_atom_1_vector[i]) + ";\n" )
        fileSW.write(prefix + ".coupling.atom2("+ str(i + 1)+ ")=" + str(Label_atom_2_vector[i]) + ";\n")


    fileSW.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Plotting%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
    fileSW.write("plot(" + prefix + ",'range',[4 4 1]);\n")
    fileSW.write(prefix + ".table('bond',1:3);\n")

    fileSW.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Magnons%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
    fileSW.write("Qcorner = {[0 0 0] [1/3 1/3 0] [1/2 0 0] [1/3 1/3 0] [0 0 0] 500};\n")  
    fileSW.write("kag33Spec =" + prefix + ".spinwave(Qcorner,'hermit',false);\n")
    fileSW.write("kag33Spec = sw_egrid(kag33Spec,'component','Sxx+Syy+Szz','imagChk',true);\n")
    fileSW.write("sw_plotspec(kag33Spec,'mode',1,'axLim',[0 30],'colorbar',false','colormap',[0 0 0],'imag',false,'sortMode',true,'dashed',false, 'qLabel',{'\Gamma' 'K' 'M' 'K' '\Gamma'})\n")
    fileSW.write("mode1 =fopen('./" + prefix + "." + str(strain) + "." + str(U) + "." + "omega1.txt', 'w' );\n")
    fileSW.write("mode2 =fopen('./" + prefix + "." + str(strain) + "." + str(U) + "." + "omega2.txt', 'w' );\n")
    fileSW.write("mode3 =fopen('./" + prefix + "." + str(strain) + "." + str(U) + "." + "omega3.txt', 'w' );\n")
    fileSW.write("mode4 =fopen('./" + prefix + "." + str(strain) + "." + str(U) + "." + "omega4.txt', 'w' );\n")
    fileSW.write("fprintf(mode1,'%g\\n', kag33Spec.omega(1,:));\n")
    fileSW.write("fprintf(mode2,'%g\\n', kag33Spec.omega(2,:));\n")
    fileSW.write("fprintf(mode3,'%g\\n', kag33Spec.omega(3,:));\n")
    fileSW.write("fprintf(mode4,'%g\\n', kag33Spec.omega(4,:));\n")
    fileSW.write("fclose(mode1);\n")
    fileSW.write("fclose(mode2);\n")
    fileSW.write("fclose(mode3);\n")
    fileSW.write("fclose(mode4);\n")

# Variables to set 
prefix = 'cri3'
spin = 3/2
angle1_lattice = angle2_lattice = 90
angle3_lattice = 120
SIA = 0

SWinput_directory,tb2j_extracted_results_directory,U,strain,n = parser()
fileSW = open(SWinput_directory, "w")
fileTB2J = open(tb2j_extracted_results_directory, "r")
a,b,c,at1,at2,Jiso_vector,Jiso_mean,Jani_matrix,DMI_matrix,NN_matrix,Label_atom_1_vector,Label_atom_2_vector,nn,number_neighbors,Label_exchange_vector = data_extractor(prefix,spin,angle1_lattice,angle2_lattice,angle3_lattice,SIA,SWinput_directory,tb2j_extracted_results_directory,n)
createSW(prefix,fileSW,a,b,c,at1,at2,Jiso_vector,Jiso_mean,Jani_matrix,DMI_matrix,NN_matrix,Label_atom_1_vector,Label_atom_2_vector,nn,number_neighbors,U,strain,Label_exchange_vector)