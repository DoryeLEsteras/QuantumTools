DFT_Kpath_dict = {
"hex": "\
4\n\
0.000 0.000 0.000 20 !Γ\n\
0.500 0.000 0.000 20 !M\n\
0.333 0.333 0.000 20 !K\n\
0.000 0.000 0.000  0 !Γ\n",

"ort": "\
5\n\
0.000 0.000  0.000 20 !Γ\n\
0.500 0.000  0.000 20 !X\n\
0.500 0.500  0.000 20 !S\n\
0.000 0.500  0.000 20 !Y\n\
0.000 0.000  0.000  0 !Γ\n",

"bcc": "\
8\n\
0.000  0.000 0.000 15 !Γ\n\
0.500 -0.500 0.500 15 !H\n\
0.250  0.250 0.250 15 !P\n\
0.000  0.000 0.000 15 !Γ\n\
0.000  0.000 0.500 15 !N\n\
0.250  0.250 0.250 15 !P\n\
0.000  0.000 0.500 15 !N\n\
0.500 -0.500 0.500  0 !H\n",

"pmc": "\
8\n\
0.000 0.000 0.000 15 !Γ\n\
0.500 0.500 0.000 15 !Y\n\
0.500 0.500 0.500 15 !M\n\
0.000 0.000 0.500 15 !A\n\
0.000 0.000 0.000 15 !Γ\n\
0.000 0.500 0.500 15 !L2\n\
0.000 0.000 0.000 15 !Γ\n\
0.000 0.500 0.000  0 !V2\n"
}

def count_nbands(bands_file_name:str) -> int:
    nbands = 0
    with open(bands_file_name,'r') as f:
        for line in f:
            read_line = line.split()
            read_line.append('end')
            if read_line[0] == 'end':
               nbands = nbands + 1
    return nbands
def count_nk(bands_file_name:str) -> int:
    nk = 0; counter = 0
    with open(bands_file_name,'r') as f:
        while nk == 0 :
            line = f.readline()
            read_line = line.split()
            read_line.append('end')
            if read_line[0] == 'end':
                nk = counter
            counter = counter + 1
    return nk
def count_occ_bands(bands_file_name:str, fermi:float, file_column:int) -> int:
    nocc_bands = 0
    nk = count_nk(bands_file_name)
    nbands = count_nbands(bands_file_name)
    bands_file = open(bands_file_name,'r')
    for i in range(0,nbands):
        for j in range(0,nk,1):  
            energy = float(bands_file.readline().split()[file_column-1])
            if fermi > energy:
               nocc_bands = i + 1
        bands_file.readline() # to remove \n at the end of each band 
    return nocc_bands