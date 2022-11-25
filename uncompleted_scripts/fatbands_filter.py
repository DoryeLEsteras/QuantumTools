import numpy as np
from argparse import ArgumentParser

# TO DO LIST
"""
If necessary add an option to filter pieces of bands and not the full bands
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
    parser.add_argument("-nk", "--nk",
                        type=int,
                        required=True,
                        help="nk ")
    parser.add_argument("-nb", "--nb",
                        type=int,
                        required=True,
                        help="nb ")
    args = parser.parse_args()

    return args.input,args.out,args.nk,args.nb

cutoff = 0.2
check = 'no'
provided_input_file,provided_output_file,nk,nbands= parser()
input_file = open(str(provided_input_file), 'r')
output_file = open(str(provided_output_file), 'w')

readed_line = '0'
read_matrix = np.zeros((nk, 3))

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
            output_file.write(str(read_matrix[subline_index][0]) + '  ' + str(read_matrix[subline_index][1]) + '  ' + str(read_matrix[subline_index][2]) + '\n')
        output_file.write('\n')
    check = 'no'