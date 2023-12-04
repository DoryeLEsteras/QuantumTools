.. create_ft:

************
create_ft.py
************

Usage
=====

The next tool creates the necessary input to perform MAE (magnetic anisotropy energy) according to the Force Theorem. As a result, three nscf files (with spin pointing in x, y, z) will start from the previous 
scf calculations.

.. code-block:: console

   create_ft.py -input qe.scf.in -k 30 30 1 -conv -8 -mat Cr1 Cr2

This execution will create the corresponding files to perform the calculations, considering a convergence criteria for the charge density of 10^-6 and considering both species, Cr1 and Cr2 for the spin orientation.

.. note::
   An important thing to consider, is that nscf calculations should include relativistic pseudopotentials. The script will print a message to remind you to check their names in nscf files.

Options
=======

.. _create_ft:

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

-k, --k
-------
Number of k-points for the nscf calculations (should be specially high for these calculations)
   
   Optional: No

   Type: List of integers

-conv, --conv
-------------
Convergence criterion for the nscf calculations. It is relevant for MAE calculations.

   Optional: No

   Type: float (negative always; ex : -7 -> 10^-7)

-mat, --mat
-----------
List of atom types to be considered (separated by spaces). The spin of this atoms will be oriented in the different Cartesian directions.
   
   Optional: No

   Type: List of strings