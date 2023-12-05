.. create_wannier:

*****************
create_wannier.py
*****************

Usage
=====

This script analyzes the presence of magnetism and/or spin-orbit coupling, and 
creates the inputs necessary to run Wannier90 calculations.
It is one of the most useful scripts but also the one that requires more flags.

.. code-block:: console

   create_wannier.py -input /mydir/qe.scf.in -kpath hex -k 6 6 6 -nbands 90 -nwan 13 -mo -5 -Mo 5 -mi 0 -Mi 2 -orb Cr:d I:p,s

This execution will create the corresponding files to perform the calculations. 
In this example, I selected the projectors, windows, number of bands...
All these flags are explained below.

.. warning::
   As explained in 'create_bands.py', the path library is under development, 
   you can see the available paths in 'create_wannier.py -h'.

Options
=======

.. _create_wannier:

-input, --input
---------------
Initial input file

   Optional: No

   Type: str

-outdir, --outdir
-----------------
Directory where the outputs will be generated.

   Optional: Yes

   Default: Directory selected with --input flag

   Type: str

-kpath, --kpath
---------------
Kpoint path to calculate the Wannier band structure
   
   Optional: Yes

   Default: 'ort' (orthorombic path)
   
   Type: str

-k, --k
-------
Number of k-points for the nscf calculations
   
   Optional: No

   Type: List of integers

-nbands, --nbands
-----------------
Number of bands for the nscf calculations

   Optional: Yes

   Default: 0

   Type: int

-nwan, --nwan
-------------
Number of wannier functions to be calculated. Should be consistent with the number of projectors.

   Optional: Yes

   Default: 0

   Type: int

-mo, --mo
---------
Minimum energy to define the outer window.

   Optional: Yes

   Default: 0

   Type: float

-Mo, --Mo
---------
Maximum energy to define the outer window.

   Optional: Yes

   Default: 0

   Type: float

-mi, --mi
---------
Minimum energy to define the inner window.

   Optional: Yes

   Default: 0

   Type: float

-Mi, --Mi
---------
Maximum energy to define the inner window.

   Optional: Yes

   Default: 0

   Type: float

-orb, --orb
-----------
Projectors to be used in the Wannierization. They should be consistent with 'nwan'
The format is 'element:orbital element:orbital ...' (e.g. 'Cr:d I:p,s').

   Optional: Yes

   Default: ''

   Type: List of strings