from argparse import ArgumentParser
from QuantumTools.library import manage_input_dir,initialize_clusters

def parser():
    parser = ArgumentParser(description="Script to create a basic template for QE")
    parser.add_argument("-input", "--input",
                        type=str,
                        required=True,
                        help="""
                        Relative or absolute path for the scf input file
                        """)
    parser.add_argument("-calculation", "--calculation",
                        type=str,
                        required=True,
                        help="""
                        Type of calculation: scf, relax or vc-relax
                        """)
    parser.add_argument("-version", "--version",
                        type=str,
                        required=False,
                        default='old',
                        help="version of QE:\n version < 7.0 -> old\n version >= 7.0 -> new ")
    args = parser.parse_args()
    return args.input,args.calculation,args.version
 
def create_template(input_name_and_dir:str,calculation_type:str,version:str) -> None:
    with open(input_name_and_dir,'w') as file:
        file.write('&CONTROL\n')
        file.write("calculation = '" + str(calculation_type)+ "'\n")
        file.write("prefix = 'prefix'\n")
        file.write("!pseudo_dir = '/u/jojaibal/QuantumEspresso/pseudopotentials'\n") 
        file.write("outdir = './tmp'\n")
        file.write("!restart_mode = 'restart'\n")
        file.write("!max_seconds = 3000\n")
        file.write("verbosity = 'low'\n")
        file.write("!verbosity = 'high'\n")
        file.write("!nstep = 500\n")
        file.write("!tstress = .true.\n")
        file.write("!tprnfor = .true.\n")
        file.write("!etot_conv_thr = 1.0D-5\n")
        file.write("!forc_conv_thr = 1.0D-4\n")
        file.write("!dipfield =.true.\n")
        file.write("!tefield =.true.\n")
        file.write("/\n\n") 
        file.write("&SYSTEM\n")
        file.write("a=,b=,c=,COSAB=,COSAC=,COSBC=\n")
        file.write("ibrav = \n")
        file.write("nat = \n")
        file.write("ntyp\n")
        file.write("ecutwfc = \n")
        file.write("ecutrho = \n")
        file.write("occupations = 'smearing'\n")
        file.write("smearing = 'cold'\n")
        file.write("nbnd = \n")
        file.write("degauss = 1.5d-02\n")
        if version == 'old':
           file.write("!lda_plus_u = .true.,lda_plus_u_kind = 1, U_projection_type = 'ortho-atomic'Hubbard_U(1) = \n")
        file.write("!vdw_corr = 'grimme-d3'\n")
        file.write("nspin = 2\n")
        file.write("starting_magnetization(1) = \n")
        file.write("!noncolin = .true.\n")
        file.write("!lspinorb=.true.\n")
        file.write("!angle1(1) = 0\n")
        file.write("!angle2(1) = 0\n")
        file.write("!emaxpos = 0.8\n")
        file.write("!edir = 3\n")
        file.write("!eopreg = 0.1 \n")
        file.write("!eamp = 0\n")
        file.write("!tot_charge = -0.806\n")
        file.write("/\n\n") 
        file.write("&ELECTRONS\n")
        file.write("electron_maxstep = 500\n")
        file.write("conv_thr = 1d-06\n")
        file.write("!mixing_mode = 'local-tf'\n")
        file.write("mixing_beta = 0.1\n")
        file.write("/\n\n") 
        if calculation_type == 'scf':
            pass
        elif calculation_type == 'relax':
                file.write("&IONS\n/\n\n")
        elif calculation_type == 'vc-relax':
                file.write("&IONS\n/\n\n")
                file.write("&CELL\n")
                file.write("cell_dofree = '2Dxy'\n")
                file.write("cell_dofree = 'ibrav'\n")
                file.write("/\n\n") 
        file.write("ATOMIC_SPECIES\n")
        file.write("AT  mass  pseudoname \n")
        file.write("\n") 
        file.write("CELL_PARAMETERS angstrom\n")    
        file.write("CELL_PARAMETERS alat\n")    
        file.write("0 0 0\n")
        file.write("0 0 0\n")
        file.write("0 0 0\n\n")

        file.write("ATOMIC_POSITIONS angstrom\n")
        file.write("ATOMIC_POSITIONS crystal\n")
        file.write("At x y z\n")
        file.write("\n")
        file.write("K_POINTS automatic\n")
        file.write("k k k 0 0 0\n")
        if version == 'new':   
            file.write("\n")
            file.write("HUBBARD ortho-atomic\n")
            file.write("U atmanifold U_value\n")
if __name__ == "__main__":
    file_dir_and_name,calculation_type,version = parser()
    create_template(file_dir_and_name,calculation_type,version)
    file_name, file_dir = manage_input_dir(file_dir_and_name)
    initialize_clusters('basic_scf',file_dir,file_name,'')
