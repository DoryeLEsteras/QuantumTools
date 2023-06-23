
import re

# plan: coje un archivo y un rango de cutwfc y cutrho te copia el archivo
#en un bucle y te sustituye los cutoffs, te prepara runs y un launcher masivo.
"""
3 modos, wfc,rho, masivo. 
wfc calcula n wfc con rho = wfc* factor
cuando este esta convergido se puede usar rho
para un wfc convergido tira muchos rho
Esto tiene coste de 2n donde n es el numero de calculos para wfc
modo masivo es tirar una red de wfc y rho, es muy automatico pero el coste es n2
launchers con modo serial y paralelo
"""
def substitute_pattern(string:str,pattern_keyword:str,replacement:str):
    pattern_ecutwfc = re.compile(r'(ecutwfc(\s*)?=(\s*)?)\d*')
    pattern_ecutrho = re.compile(r'(ecutrho(\s*)?=(\s*)?)\d*') 
    pattern_hubbard = re.compile(r'(Hubbard_U\(\d\)(\s*)?=(\s*)?)\d*)\.?(\d*)?') 
    
    patterns_and_keywords = {
    'ecutwfc':pattern_ecutwfc,
    'ecutrho':pattern_ecutrho,
    'hubbard':pattern_hubbard,
    }

    new_string = patterns_and_keywords[pattern_keyword].sub(r'\1\b{}\b'.format(replacement),string)
    return new_string

file = open('./entorno_controlado/feps3.nm.nscf.in','r')
read_vector = file.read()
print(substitute_pattern(read_vector,'hubbard','X'))
