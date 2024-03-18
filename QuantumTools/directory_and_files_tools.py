import os
import re
from typing import List
def manage_input_dir(input_dir_and_name:str) -> str: 
    file_name = os.path.basename(input_dir_and_name)
    file_dir = os.path.abspath(os.path.dirname(input_dir_and_name))
    #outdir = os.path.abspath(output_directory)
    return file_name, file_dir#, outdir
def handle_comments(file_name:str) -> List[str]:
    with open(file_name, 'r') as file:
        lines = file.readlines()
        new_line = ''; uncommented_file = []
        for line in lines:
            for character in line:
                if character != '!':
                   new_line = new_line + character
                if character == '!':
                    new_line = new_line + '\n'
                    break 
            uncommented_file.append(new_line)
            new_line = ''
    return uncommented_file
def clean_uncommented_file(file_list:List[str]) -> List[str]:
    clean_file = []
    symbol_colection = '=()[],"'
    for line in file_list:
        for symbol in symbol_colection:
            line= line.replace(symbol,' ').replace('d0','')
        clean_file.append(line)   
    return clean_file

def substitute_pattern(string:str,pattern_keyword:str,replacement:str):
    pattern_ecutwfc = re.compile(r'(ecutwfc(\s*)?=(\s*)?)\d*')
    pattern_ecutrho = re.compile(r'(ecutrho(\s*)?=(\s*)?)\d*') 
    pattern_hubbard_under_v7 = re.compile(r'(Hubbard_U\(\d\)\s*?\=\s*?) (\d*\.?\d*)?')
    pattern_hubbard_over_v7 = re.compile(r'(U\s\s*?\w*\s\s*?) (\d*\.\d*)?')
    #prefix = re.compile(r'(prefix\s*?=\s*?\'\w*)\'')
    patterns_and_keywords = {
    'ecutwfc':pattern_ecutwfc,
    'ecutrho':pattern_ecutrho,
    'hubbard_under_v7':pattern_hubbard_under_v7,
    'hubbard_over_v7':pattern_hubbard_over_v7,
    #'prefix':prefix,
    }
    #if pattern_keyword == 'hubbard_under_v7':
    #    new_string = patterns_and_keywords[pattern_keyword].sub(r'\1 '+ str(replacement),string)
    #elif pattern_keyword == 'hubbard_over_v7':
    #    new_string = patterns_and_keywords[pattern_keyword].sub(r'\1 '+ str(replacement),string) 
    #elif pattern_keyword == 'ecutwfc':
    new_string = patterns_and_keywords[pattern_keyword].sub(r'\1 '+ str(replacement),string)  
    return new_string
    
def get_time(value) -> str:
    timestr = ''
    if(value == 0):
        timestr += '00'
    elif(value < 10):
        timestr += '0%s'%value
    else:
        timestr += str(value)
    return timestr

def stop_watch(start, finish) -> str:
    s_in_h = 3600
    s_in_min = 60
    elapsed = int(finish-start)
    mystr = ''
    mystr += 'Time wasted: '
    if(elapsed > 0):
        mystr += get_time(int(elapsed / s_in_h))
        mystr += ':'
        mystr += get_time(int((elapsed % s_in_h) / s_in_min))
        mystr += ':'
        mystr += get_time(int((elapsed % s_in_h) % (s_in_min)))
    else:
        mystr += '00:00:00'
    mystr += '\n'
    return mystr
