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


def grep(read_vector,key_word,position): 
    """
    read_vector is the a vector of strings that contains the input file obtained as:
    text = file1.read(); text_list = text.split() position is the number of sites 
    where the desired word is present respect to the key_word 
    """
    position_of_word = int(read_vector.index(key_word)) + int(position)
    return read_vector[position_of_word] 

if __name__ == '__main__':
    file1 = open('/Users/Dorye/Downloads/crcl3.100.z.5.0.scf.in', "r")
    text = file1.read()
    text_list = text.split()
    file1.close()
    print(grep(text_list,'-0.0250908',3))