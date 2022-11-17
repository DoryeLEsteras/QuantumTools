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