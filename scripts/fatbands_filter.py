import numpy as np
from argparse import ArgumentParser

# TO DO LIST
"""
Done
"""

def parser():
    parser = ArgumentParser(description="Script to disentangle the interesting bands after a fatband calculation")
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
                        Output file name and directory
                        """)    
    parser.add_argument("-cut", "--cut",
                        type=float,
                        required=True,
                        help="cutoff for extracting the bands ")
    parser.add_argument("-mode", "--mode",
                        type=int,
                        required=True,
                        help="Mode1 to filter full bands, mode 2: surface only mode ")
    args = parser.parse_args()
    return args.input,args.out,args.cut,args.mode

provided_input_file,provided_output_file,cutoff,mode= parser()
input_file = open(str(provided_input_file), 'r')
output_file = open(str(provided_output_file), 'w')
read_line = [];counter = 0; nk = 0;nbands = 0

# Calculate number of bands and number of kpoints per band
with open(str(provided_input_file),'r') as f:
    while nk == 0 :
        line = f.readline()
        read_line = line.split()
        read_line.append('end')
        if read_line[0] == 'end':
            nk = counter
        counter = counter + 1
with open(str(provided_input_file),'r') as f:
    for line in f:
        read_line = line.split()
        read_line.append('end')
        if read_line[0] == 'end':
            nbands = nbands +1




readed_line = '0'; check = 'no'; read_matrix = np.zeros((nk, 3))
if mode == 1:
    for i in range(0,nbands,1):
        for subline_index in range(0,nk,1):
            readed_line = input_file.readline()
            readed_line = readed_line.split()
            read_matrix[subline_index][0] = readed_line[0]
            read_matrix[subline_index][1] = readed_line[1]
            read_matrix[subline_index][2] = readed_line[2]
            if float(readed_line[2]) > cutoff:
                check = 'yes'
        input_file.readline() 
        if check == 'yes':
            for subline_index in range(0,nk,1):
                output_file.write(str(read_matrix[subline_index][0]) + '  ' + \
                str(read_matrix[subline_index][1]) + '  ' + \
                str(read_matrix[subline_index][2]) + '\n')
            output_file.write('\n')
        check = 'no'
if mode == 2:
    for i in range(0,nbands,1):
        for subline_index in range(0,nk,1):
            readed_line = input_file.readline()
            readed_line = readed_line.split()
            read_matrix[subline_index][0] = readed_line[0]
            read_matrix[subline_index][1] = readed_line[1]
            read_matrix[subline_index][2] = readed_line[2]
            if float(readed_line[2]) > cutoff:
                output_file.write(str(read_matrix[subline_index][0]) + '  ' + \
                str(read_matrix[subline_index][1]) + '  ' + \
                str(read_matrix[subline_index][2]) + '\n')
        input_file.readline() 
input_file.close()
output_file.close()
