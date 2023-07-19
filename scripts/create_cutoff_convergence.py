import os
from argparse import ArgumentParser

import numpy as np
from QuantumTools.library import manage_input_dir, substitute_pattern,initialize_clusters


def parser():
    parser = ArgumentParser(description="Script to converge the cutoffs")
    parser.add_argument("-input", "--input",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the scf input file
                        """)
    parser.add_argument("-outdir", "--outdir",
                        type=str,
                        required=False,
                        default='./',
                        help="output directory ")
    parser.add_argument("-wfcmax", "--wfcmax",
                        type=int,
                        required=False,
                        default='0',
                        help="Top limit for ecutwfc scanning")
    parser.add_argument("-wfcmin", "--wfcmin",
                        type=int,
                        required=False,
                        default='0',
                        help="Starting value for ecutwfc scanning")
    parser.add_argument("-wfcstep", "--wfcstep",
                        type=int,
                        required=False,
                        default='1',
                        help=" Step for ecutwfc scanning")
    parser.add_argument("-rhomax", "--rhomax",
                        type=int,
                        required=False,
                        default='0',
                        help="Top limit for ecutrho scanning")
    parser.add_argument("-rhomin", "--rhomin",
                        type=int,
                        required=False,
                        default='0',
                        help="Starting value for ecutrho scanning")
    parser.add_argument("-rhostep", "--rhostep",
                        type=int,
                        required=False,
                        default='1',
                        help=" Step for ecutrho scanning")
    args = parser.parse_args()
    return args.input,args.outdir,args.wfcmin,args.wfcmax,args.wfcstep,args.rhomin,args.rhomax,args.rhostep

def create_total_scan():
    with open(file_dir_and_name,'r') as file:
        readed_file = file.read()
    for wfc in np.arange(wfcmin,wfcmax + wfcstep,wfcstep):
        for rho in np.arange(rhomin,rhomax + rhostep,rhostep):
            new_file_name = file_name
            if wfc != 0:
                readed_file = substitute_pattern(readed_file,'ecutwfc', wfc)
                new_file_name = new_file_name.replace('.scf','.wfc.' + str(wfc) + '.scf')
            if rho != 0:
                readed_file = substitute_pattern(readed_file,'ecutrho', rho)
                new_file_name = new_file_name.replace('.scf','.rho.'+ str(rho) + '.scf')
            with open(os.path.join(outdir,new_file_name),'w') as new_file:
                 new_file.write(readed_file)    
            if wfc != 0 and rho != 0:
               initialize_clusters('basic_scf',outdir,new_file_name,'.wfc.' + str(wfc) + '.rho.' + str(rho))   
               initialize_clusters('launcher',outdir,'','') 
            elif wfc != 0 and rho == 0:
               initialize_clusters('basic_scf',outdir,new_file_name,'.wfc.' + str(wfc))
            elif wfc == 0 and rho != 0:
               initialize_clusters('basic_scf',outdir,new_file_name,'.rho.' + str(rho)) 

if __name__ == '__main__':    
   file_dir_and_name,outdir,wfcmin,wfcmax,wfcstep,rhomin,rhomax,rhostep = parser()
   file_name,file_dir = manage_input_dir(file_dir_and_name)
   create_total_scan()

