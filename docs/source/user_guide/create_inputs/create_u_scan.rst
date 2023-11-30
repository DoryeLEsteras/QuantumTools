.. installation:

****************
create_u_scan.py
****************

Usage
=====
The objective of this tools is to help you in those situations when you were performing a relax or vc-relax calculation that resulted uncompleted.

Brute force method
------------------
.. code-block:: console

   create_cutoff_convergence.py -input qe.scf.in -wfcmin 50 -wfcmax 150 -rhomin 500 -rhomax 1500 -wfcstep 10 -rhostep 100
 
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

