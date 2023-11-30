.. scripts_cover :

************************************
Introduction to QuantumTools scripts
************************************

Workflow
========
The QuantumTools workflow is organized in three main pilars. 1) The automatization of input creation for your DFT softwares, 2) The synchronization with your cluster to create the run files for your calculations and 3) Extraction tools for treating the obtained outputs. To start with the workflow, documentation is structured in this three pilars:

* Sync your cluster's batch files
* Learn about the 'create' scripts
* Learn about the 'extract' scripts

At the moment, the package is highly focused in creation over extraction, thus extract scripts are more limited. Also, the majority of the tools are based in QuantumEspresso and the interface of other packages such as Wannier90, WannierTools, TB2J and spinW with QuantumEspresso. Extending the workflow to other DFT codes is under development.

Examples of usage
=================
To illustrate the workflow, two examples are shown. The first one represents the automatization of inputs and runs for the interface with an external package, Wannier90.

.. code-block:: console

   create_wannier.py -input qe.scf.in -k 9 9 9 -kpath hex -nbands 100 -nwan 20 -Mo 10 -mo -10 -Mi 2 -mi -2 -orb Fe:d-P:s,p-S:s,p

This script creates using the scf input qe.scf.in all the files to run a Wannier calculation, considering if the system is non-magnetic, magnetic (two separated calculations) or magnetic noncollinear.

Moreover, it creates a run ready to sbatch the calculations for each synchronized cluster.

Example of the created run of a particular cluster (magnetic wannier):

.. code-block:: console

   #!/bin/bash -l
   #SBATCH --output=task.out.%j
   #SBATCH --error=task.err.%j
   #SBATCH -D ./
   
   # Job Name
   #SBATCH --job-name= job_name
   #SBATCH --nodes=1
   #SBATCH --mem=200gb
   #SBATCH --partition=interactive
   #SBATCH --ntasks-per-node=72
   #SBATCH --time=0-01:59:00
   
   #Libraries and modules
   module load intel/21.5.0
   module load  impi/2021.5
   module load mkl/2022.2
   module load qe/6.8
   module load wannier90/3.1.0

   srun pw.x -i qe.scf.in > qe.scf.out
   srun pw.x -i qe.nscf.in > qe.nscf.out
   srun wannier90.x -pp qe.up.win
   srun pw2wannier90.x -i qe.up.pw2wan.in > qe.up.pw2wan.out
   srun wannier90.x qe.up.win
   srun wannier90.x -pp qe.down.win
   srun pw2wannier90.x -i qe.down.pw2wan.in > qe.down.pw2wan.out
   srun wannier90.x qe.down.win

Example of the created run in a cluster with different configuration (non-magnetic wannier):

.. code-block:: console

   #!/bin/bash -l
   #SBATCH --job-name= job_name
   ##SBATCH --nodes= 2
   #SBATCH --workdir=./
   #SBATCH --output=task.out.%j
   #SBATCH --error=task.err.%j
   ##SBATCH --mem-per-cpu=2GB
   #SBATCH --ntasks=32
   #SBATCH --cpus-per-task=1
   ##SBATCH --tasks-per-node=8
   #SBATCH --time=0-03:10:00
   
   export LD_LIBRARY_PATH=/storage/apps/Intel_Comp/xe_2019u4/mpi/intel64/:$LD_LIBRARY_PATH
   
   module load intel/2018.3.222
   module load mkl/2018.3.222
   module load impi/2018.3.222
   module load hdf5/1.10.1
   module load wannier90/3.1
   
   ulimit -s unlimited
   export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}
   
   srun /storage/home/vlc93/qe-6.8/bin/pw.x -i qe.scf.in > qe.scf.out
   srun /storage/home/vlc93/qe-6.8/bin/pw.x -i qe.nscf.in > qe.nscf.out
   srun wannier90.x -pp qe.win
   srun /storage/home/vlc93/qe-6.8/bin/pw2wannier90.x -i qe.pw2wan.in > qe.pw2wan.out
   srun wannier90.x qe.win

The second example illustrates a case that requires to prepare decens or hundreds of files,the convergence of a cutoff in QuantumEspresso:

.. code-block:: console

   create_cutoff_convergence.py -input qe.scf.in -wfcmin 50 -wfcmax 150 -rhomin 500 -rhomax 1500 -wfcstep 10 -rhostep 100

The previous script will generate a sizable grid of calculations, with their respective run.sh files and a launcher ready to submit everything. This represents a clear case where automatization saves a lot of time and avoid errors. However, this way of using the cutoff script is too based in brute force, because of that, the next sections have the purpose of teaching how to use appropriately this and the rest of scripts in QuantumTools package..
