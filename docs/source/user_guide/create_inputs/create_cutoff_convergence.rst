.. create_cutoff_convergence:

****************************
create_cutoff_convergence.py
****************************

Usage
=====

Let's think you have an scf file to start the calculations of your new material (like the one you can obtain completing the file provided by create_template.py). One of the first things probably you want to do is to converge the cutoff of your new system. As briefly discussed in the introduction of the package, you can do this in two different ways, using the brute force or the two step methods.

Brute force method
------------------
If your material does not require an important amount of resources to compute scf calculations or if you just one to solve this in one shoot, probably you want to use this method. Where basically a full grid of both wave function (wfc) and charge density (rho) cutoffs will be generated to converge both magnitudes at the same time.

.. code-block:: console

   create_cutoff_convergence.py -input qe.scf.in -wfcmin 50 -wfcmax 150 -rhomin 500 -rhomax 1500 -wfcstep 10 -rhostep 100

This execution will create a large grid of scf files, with different prefixes and cutoffs in the specified ranges. Also the run files and a launcher.sh ready to submit the calculations will be generated.

Two-step method
---------------
Despite the previous approach is very automatic, is not efficient and if your system is computationally expensive, you will waste a lot of resources. The alternative to the brute force requires to do the calculation in two steps, first converging the wave function cutoff and then, using it to converge the charge density cutoff:

.. code-block:: console

   create_cutoff_convergence.py -input qe.scf.in -wfcmin 50 -wfcmax 150 -wfcstep 10

.. code-block:: console

   create_cutoff_convergence.py -input qe.converged.wfc.scf.in -rhomin 500 -rhomax 1500 -rhostep 100
  
.. note::
   If we assume N possible values for both, wfc and rho cutoffs, the number of calculation scales with N^2 in the brute force method and with 2N in the two step method. Depends on the time of the simulation and the value of N you need, this will be apocaliptical or almost the same cost. It is your choice to select the light or the dark side.

Options
=======

.. _create_cutoff_convergence:

-input, --input
---------------
Name of the initial input file

   Optional: No

   Type: str

-outdir, --outdir
-----------------
Directory where the outputs will be generated.

   Optional: Yes

   Default: Directory selected with --input flag

   Type: str

-wfcmin, --wfcmin
-----------------
Minimum value for the wfc cutoff scan
   
   Optional: Yes

   Default: The value provided in the input 
   
   Type: int

-wfcmax, --wfcmax
-----------------
Maximum value for the wfc cutoff scan
   
   Optional: Yes

   Default: The value provided in the input 
   
   Type: int

-rhomin, --rhomin
-----------------
Minimum value for the rho cutoff scan
   
   Optional: Yes

   Default: The value provided in the input 
   
   Type: int

-rhomax, --rhomax
-----------------
Maximum value for the rho cutoff scan
   
   Optional: Yes

   Default: The value provided in the input 
   
   Type: int

-wfcstep, --wfcstep
-------------------
Step value for the wfc cutoff scan
   
   Optional: Yes

   Default: 10
   
   Type: int

-rhostep, --rhostep
-------------------
Step value for the rho cutoff scan
   
   Optional: Yes

   Default: 10
   
   Type: int
