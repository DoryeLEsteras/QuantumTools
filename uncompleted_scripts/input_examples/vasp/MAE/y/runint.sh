#!/bin/bash -l

# Standard output and error:
#SBATCH --output=task.out.%j
#SBATCH --error=task.err.%j
# Initial working directory:
#SBATCH -D ./

# Job Name
#SBATCH --job-name=y
# Number of nodes and MPI tasks per node:
#SBATCH --nodes=1
#SBATCH --mem=30gb
#SBATCH --partition=interactive
#SBATCH --ntasks-per-node=8

# Wall clock limit:
#SBATCH --time=0-00:50:00

#Libraries and modules
module purge
module load vasp/6.4.1
ulimit -s unlimited

srun  vasp_ncl
