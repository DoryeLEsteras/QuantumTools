.. create_projected:

*******************
create_projected.py
*******************

Usage
=====

The next calculation to consider is the projected density of states (includes the calculation of total density of states aswell). For this you should use 'create_projected.py':

.. code-block:: console

   create_projected.py -input qe.scf.in -k 8 8 8 

This execution will create the corresponding files to perform the calculations. An important point here is to run an nscf calculation using the occupation method tetrahedra and removing degauss.

.. note::
   By default inputs are created using a Gamma centered kpoint mesh (0 0 0).

Options
=======

.. _create_projected:

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
-----------------
Number of k-points for the nscf calculations
   
   Optional: No

   Type: List of integers