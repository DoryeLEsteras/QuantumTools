import numpy as np
from argparse import ArgumentParser

# TO DO LIST
"""
    All the workflow is working but just readblock for resolved no soc is done
    do the other 3 functions: 
    - readblock noresolved no soc, 
    - readblock noresolved soc 
    - and readblock resolved  soc
    - DMI
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
    parser.add_argument("-n", "--n",
                        type=str,
                        required=True,
                        nargs='+',
                        help="n1 n2 n3 n4 n5 n6 for number of neighbours in exchange file ")
    args = parser.parse_args()
    return args.input,args.out,args.n
def readblock_noresolved_soc(Jiso,Jani,DMI,input_file):
    readed_line = input_file.readline()
    readed_line = readed_line.split()
    Jiso = Jiso + float(readed_line[1])
    input_file.readline()
    readed_line = input_file.readline()
    readed_line = readed_line.split()
    #DMI = np.add(DMI, np.array([readed_line[2],readed_line[3],readed_line[4]]))    
    #DMI=0
    """
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
    Jani=0
    return Jiso,Jani,DMI 
    """
"""
    Jani = np.add(Jani,np.matrix([ [ float(readed_line1[1]), \
    + float(readed_line1[2]),float(readed_line1[3])], [ float(readed_line2[1]),\
     float(readed_line2[2]),float(readed_line2[3])],\
     [float(readed_line3[1]),float(readed_line3[2]),float(readed_line3[3])]]))
    input_file.readline()    
    input_file.readline()
    print(Jiso)
"""
def readblock_resolved_nosoc(Jiso,Jorb,input_file):
    readed_line = input_file.readline()
    readed_line = readed_line.split()
    Jiso = Jiso + float(readed_line[1])
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
    Jorb = np.add(Jorb,np.matrix([ [ float(readed_line1[0]), float(readed_line1[1]),float(readed_line1[2]),float(readed_line1[3]),float(readed_line1[4])], [ float(readed_line2[0]), float(readed_line2[1]),float(readed_line2[2]),float(readed_line2[3]),float(readed_line2[4])], [float(readed_line3[0]),float(readed_line3[1]),float(readed_line3[2]),float(readed_line3[3]),float(readed_line3[4])],[ float(readed_line4[0]), float(readed_line4[1]),float(readed_line4[2]),float(readed_line4[3]),float(readed_line4[4])],[ float(readed_line5[0]), float(readed_line5[1]),float(readed_line5[2]),float(readed_line5[3]),float(readed_line5[4])]]))
    input_file.readline()    
    input_file.readline()
    return Jiso,Jorb
def calculator(ni,Jlabel,output_file,input_file):
    Jiso = 0;Jorb = Jper = np.zeros((5, 5))
    DMI= np.array([0,0,0])
    Jani = np.zeros((3, 3))
    for i in range(0,ni,1):
        #Jiso , Jorb = readblock_resolved_nosoc(Jiso,Jorb,input_file)
        Jiso , Jorb = readblock_noresolved_soc(Jiso,Jani,DMI,input_file)
    Jiso= round(Jiso/ni,3)
    Jorb= np.divide(Jorb,ni)
    Jper= np.divide(Jorb,Jiso/100)
    Jorb=np.matrix.round(Jorb,3)
    Jper=np.matrix.round(Jper,1)
    output_file.write(Jlabel + ' iso : ' + str(Jiso) + '\n')
    output_file.write(Jlabel + ' orb :\n' + str(Jorb[0][0]) + ' ' + str(Jorb[1][0]) + ' ' \
        + str(Jorb[2][0]) + ' ' + str(Jorb[3][0])  + ' ' + str(Jorb[4][0]) + '\n' \
        + str(Jorb[0][1]) + ' ' + str(Jorb[1][1]) + ' ' \
        + str(Jorb[2][1]) + ' ' + str(Jorb[3][1]) + ' ' + str(Jorb[4][1]) + '\n ' \
        + str(Jorb[0][2]) + ' ' + str(Jorb[1][2]) + ' ' +  str(Jorb[2][2]) \
        + ' ' + str(Jorb[3][2]) + ' ' + str(Jorb[4][2]) + '\n' \
        + str(Jorb[0][3]) + ' ' +  str(Jorb[1][3]) + ' ' + str(Jorb[2][3]) \
        + ' ' + str(Jorb[3][3]) + ' ' + str(Jorb[4][3]) + '\n' \
        +  str(Jorb[0][4]) + ' ' + str(Jorb[1][4]) + ' ' + str(Jorb[2][4]) \
        + ' ' + str(Jorb[3][4]) + ' ' + str(Jorb[4][4]) + '\n' + '\n')
    """
    output_file.write(Jlabel + ' percentage :\n' + str(Jper[0][0]) + ' ' + str(Jper[1][0]) + ' ' \
        + str(Jper[2][0]) + ' ' +  str(Jper[3][0])  + ' ' + str(Jper[4][0]) + '\n' \
        + str(Jper[0][1]) + ' ' + str(Jper[1][1]) + ' ' \
        + str(Jper[2][1]) + ' ' + str(Jper[3][1]) + ' ' + str(Jper[4][1]) + '\n ' \
        + str(Jper[0][2]) + ' ' + str(Jper[1][2]) + ' ' +  str(Jper[2][2]) \
        + ' ' + str(Jper[3][2]) + ' ' + str(Jper[4][2]) + '\n' \
        + str(Jper[0][3]) + ' ' +  str(Jper[1][3]) + ' ' + str(Jper[2][3]) \
        + ' ' + str(Jper[3][3]) + ' ' + str(Jper[4][3]) + '\n' \
        +  str(Jper[0][4]) + ' ' + str(Jper[1][4]) + ' ' + str(Jper[2][4]) \
        + ' ' + str(Jper[3][4]) + ' ' + str(Jper[4][4]) + '\n' + '\n')
    """
def execution():
    provided_input_file,provided_output_file,n= parser()
    input_file = open(str(provided_input_file), 'r')
    output_file = open(str(provided_output_file), 'a')
    line = input_file.readline()
    while line != 'Exchange: \n':
        line = input_file.readline()
    input_file.readline()
    input_file.readline()
    input_file.readline()
    calculator(int(n[0]),'J1',output_file,input_file)
    calculator(int(n[1]),'J2',output_file,input_file)
    calculator(int(n[2]),'J3',output_file,input_file)
    calculator(int(n[3]),'J4',output_file,input_file)
    calculator(int(n[4]),'J5',output_file,input_file)
    calculator(int(n[5]),'J6',output_file,input_file)

execution()
#FePS3 rel CoPS3 rel
#execution(8,4,8,16,4,8)
#FePS3 norel cops3 norel
#execution(4,8,16,8,4,8)
#Nips3rel
#execution(4,8,16,8,8,4)
#Nips3norel
#execution(8,4,8,16,8,4)