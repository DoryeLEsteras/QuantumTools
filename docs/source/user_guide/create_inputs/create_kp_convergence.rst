.. create_kp_convergence:

************************
create_kp_convergence.py
************************

Usage
=====

Another important magnitude to converge is the k-point mesh. You can converge them in a very similar way than the cutoff using this time create_kp_convergence.py:

.. code-block:: console

   create_kp_convergence.py -input qe.scf.in -min 2 -max 8 -step 1

This execution will create an homogeneous grid of scf files, with different prefixes and cutoffs in the specified range. Also the run files and a launcher.sh ready to submit the calculations will be generated.

Options
=======

.. _create_kp_convergence:

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

-min, --min
-----------------
Minimum value for the k-point homogeneous scan
   
   Optional: No

   Type: int

-max, --max
-----------------
Maximum value for the k-point homogeneous scan
   
   Optional: No
   
   Type: int

-step, --step
-----------------
Step value for the k-point scan
   
   Optional: Yes

   Default: 1
   
   Type: int

