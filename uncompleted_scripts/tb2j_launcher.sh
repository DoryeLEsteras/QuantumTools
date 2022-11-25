#!/bin/bash -l
#SBATCH -o ./task.out.%j
#SBATCH -e ./task.err.%j
# Initial working directory:
#SBATCH -D ./
# Job Name:
#SBATCH -J CI
#
# Number of nodes and MPI tasks per node:
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=72
#SBATCH --partition=medium
# Wall clock limit:
#SBATCH --time=05:00:00

# Make sure each process only uses one thread, that is, force VASP to use only one thread per core

########################
# Load environment
########################

"""
TO DO LIST

 maybe include this in the run manager, so a bash script is created with the header of the appropiate cluster
"""

module load intel/21.5.0
module load  impi/2021.5

export LD_LIBRARY_PATH=/mpcdf/soft/SLE_12_SP3/packages/x86_64/intel_parallel_studio/2018.3/mkl/lib/intel64:$LD_LIBRARY_PATH
LD_LIBRARY_PATH=/raven/u/system/soft/SLE_15/packages/x86_64/anaconda/3/2020.02/lib
export LD_LIBRARY_PATH

prefix=cri3
dirx=/ptmp/jojaibal/TcCurieMX3/TcCurieMX3Finished/mapa_completo_rotado_cri3/x
diry=/ptmp/jojaibal/TcCurieMX3/TcCurieMX3Finished/mapa_completo_rotado_cri3/y
dirz=/ptmp/jojaibal/TcCurieMX3/TcCurieMX3Finished/mapa_completo_rotado_cri3/z

for str in $(seq 95 1 95)
do
   for U in $(seq 2.0 0.5 2.0)
   do
component=z
dir=${dirz}
fermi=$(grep 'the Fermi energy is' ${dir}/${prefix}.${str}.${component}.${U}.scf.out | awk '{print $5}')
 srun wann2J.py --spinor --groupby orbital --rcut 10 --nz 500  --emax 0.1 --efermi $fermi --kmesh 12 12 1 --elements Cr --posfile ${prefix}.${str}.${component}.${U}.scf.in  --prefix_spinor ${prefix}.${str}.${component}.${U} --path ${dir}  --output_path ${dir}/TB2J_results.${str}.${component}.${U} --np 72 --orb_decomposition
component=y
dir=${diry}
fermi=$(grep 'the Fermi energy is' ${dir}/${prefix}.${str}.${component}.${U}.scf.out | awk '{print $5}')
srun wann2J.py --spinor --groupby orbital --rcut 10 --nz 500  --emax 0.1 --efermi $fermi --kmesh 12 12 1 --elements Cr --posfile ${prefix}.{str}.${component}.${U}.scf.in  --prefix_spinor ${prefix}.${str}.${component}.${U} --path ${dir}  --output_path ${dir}/TB2J_results.${str}.${component}.${U} --np 72 --orb_decomposition
component=x
dir=${dirx}
fermi=$(grep 'the Fermi energy is' ${dir}/${prefix}.${str}.${component}.${U}.scf.out | awk '{print $5}')
srun wann2J.py --spinor --groupby orbital --rcut 10 --nz 500  --emax 0.1 --efermi $fermi --kmesh 12 12 1 --elements Cr --posfile ${prefix}.{str}.${component}.${U}.scf.in  --prefix_spinor ${prefix}.${str}.${component}.${U} --path ${dir}  --output_path ${dir}/TB2J_results.${str}.${component}.${U} --np 72 --orb_decomposition

TB2J_merge.py ${dirx}/TB2J_results.${str}.x.${U} ${diry}/TB2J_results.${str}.y.${U} ${dirz}/TB2J_results.${str}.z.${U} --type spin  --output_path ${dirz}/../TB2J_results.${prefix}.${str}.${U}

done
done
