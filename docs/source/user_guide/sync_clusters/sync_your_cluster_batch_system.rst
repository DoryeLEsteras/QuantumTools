.. sync_your_cluster_batch_system:

Motivation: examples of usage
=============================

The first thing you can do with QuantumTools is to configure your setup for the 
automatization of the batch files that run the calculations in your clusters.  
Example: Every time you execute the create_wannier.py script used in the previous introduction,
you will generate the ready to submit batch files for a Wannier calculation with your particular Wannier file names.
Moreover, one batch file will be generated for each cluster you configured. 
You can configure the same cluster several times with different conditions.
Let's see some examples:

Herein, I have created three configurations, so in every run, three batch files will be generated.
In particular I configured cluster1 in two ways (cluster1_fast,cluster1_largescale) and then a different cluster (cluster2)

For the cluster 1 we have this configuration that I called, 'fast_cluster1' 
which loads and exports libraries in the manner cluster1 needs,
but in particular is focused in fast calculations (1 node, interactive queue, 30min):

.. code-block:: console

   #!/bin/bash -l 
   #SBATCH --job-name=job_name
   #SBATCH --nodes=1
   #SBATCH --partition=interactive
   #SBATCH --ntasks-per-node=72
   #SBATCH --time=0-00:30:00
   
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

But now, I have a second configuration of cluster 1, speciallized in large calculations
(cluster1_largescale). So when I run the create_wannier.py script, a second batch file is created:

.. code-block:: console

   #!/bin/bash -l 
   #SBATCH --job-name=job_name
   #SBATCH --nodes=4
   #SBATCH --partition=large
   #SBATCH --ntasks-per-node=72
   #SBATCH --time=2-20:30:00
   #SBATCH --mem=200GB
   
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

You can see the cluster details are the same, but now this is ready to submit a 
calculation in a large queue, with 4 nodes, extra large memory and almost 3 days duration.

Finally we have the third batch file generated, that corresponds to a different cluster:

.. code-block:: console

   #!/bin/bash -l
   #SBATCH --job-name=job_name
   #SBATCH --nodes= 2
   #SBATCH --ntasks=32
   #SBATCH --cpus-per-task=1
   #SBATCH --tasks-per-node=8
   #SBATCH --time=0-00:30:00
   
   export LD_LIBRARY_PATH=/storage/apps/Intel_Comp/xe_2019u4/mpi/intel64/:$LD_LIBRARY_PATH
   
   module load intel/2018.3.222
   module load mkl/2018.3.222
   module load impi/2018.3.222
   module load hdf5/1.10.1
   module load wannier90/3.1
   
   ulimit -s unlimited
   export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}
   
   srun /storage/home/vlc/qe-6.8/bin/pw.x -i qe.scf.in > qe.scf.out
   srun /storage/home/vlc/qe-6.8/bin/pw.x -i qe.nscf.in > qe.nscf.out
   srun wannier90.x -pp qe.up.win
   srun /storage/home/vlc/qe-6.8/bin/pw2wannier90.x -i qe.up.pw2wan.in > qe.up.pw2wan.out
   srun wannier90.x qe.up.win
   srun wannier90.x -pp qe.down.win
   srun /storage/home/vlc/qe-6.8/bin/pw2wannier90.x -i qe.down.pw2wan.in > qe.down.pw2wan.out
   srun wannier90.x qe.down.win

Here, you can see the cluster has different requirements, for example a particular 
version of QuantumEspresso installed by the user is specified in the srun command,
we need to export some paths with libraries, the version of the modules is different...
But everything is configured in QuantumTools. You can extend this as much as you want! Let's see how to do it:

How to setup QuantumTools with your clusters
============================================
If you follow the installation guide, you have a Quantum Tools folder in your computer.
Inside of the QuantumTools package folder, you have another folder called QuantumTools that includes the libraries.

.. code-block:: console
   
   cd QuantumTools
   cd QuantumTools
   ls

Herein, there are two important files to look at. First, you have several cluster files,
that end with the extension '.cluster', for example 'Tirant.cluster'.
These are some illustrative templates, you can use them to create your own files 
and fill them with the information of your clusters.  
Basically you have two sections, the directories and the header:

.. code-block:: console

   ######### Tirant directories #########
   QE_dir:  /storage/home/vlc/vlc93/qe-6.8/bin/
   Wan_dir:  
   WT_dir:

   ######### Tirant run header #########
   #!/bin/bash -l
   #SBATCH --job-name= job_name
   #SBATCH --nodes= 2
   #SBATCH --workdir=./
   #SBATCH --output=task.out.%j
   #SBATCH --error=task.err.%j
   #SBATCH --mem-per-cpu=2GB
   #SBATCH --ntasks=32 
   #SBATCH --cpus-per-task=1
   ##SBATCH --tasks-per-node=8
   #SBATCH --time=0-03:10:00

   export LD_LIBRARY_PATH=/storage/apps/Intel_Comp/xe_2019u4/compilers_and_libraries_2019.4.243/linux/mpi/intel64/lib/:$LD_LIBRARY_PATH

   module load intel/2018.3.222   
   module load mkl/2018.3.222 
   module load impi/2018.3.222   
   module load hdf5/1.10.1
   module load wannier90/3.1 

   ulimit -s unlimited
   export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}

The header makes reference to the contents of your batch file (everything except the sections 
where you launch the calculations with srun, that will be automatically generated),
you should paste here your personal header

The directories section is optional, if you want to use a version of QuantumEspresso,
WannierTools or Wannier90 different from the one you can obtain with 'module load' (you installed in the cluster by yourself)
you can put here the directories, thus when srun is automatically generated, it will specify these directories.

You can create as many .cluster files as you want, build your own collection!
This is thanks to the second important file in this folder, Cluster.config, that
basically contains those particular cluster files from your collection, that you want to consider for batch file generation:
 
.. code-block:: console

   Tirant 
   Tirant_largescale
   Tirant_fast
   Vives
   Draco

In this example, from my collection QuantumTools will just create 5 batch files,
one for each cluster (Tirant, Vives, Draco) and in particular 
I have 3 configurations for Tirant (Tirant, Tirant_largescale, Tirant_fast).

Remember always, after you modify these files to use pip to reinstall QuantumTools,
you can do this easily in the main folder of QuantumTools with:

.. code-block:: console

   pip install .

