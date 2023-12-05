.. create_bands:

***************
create_bands.py
***************

Usage
=====

Let's start discussing scripts to create the inputs associated to the typical 
calculations you perform in a material. It is the turn of the electronic band 
structure, for that the script 'create_bands.py' will be your best tool.

.. code-block:: console

   create_bands.py -input /mydir/qe.scf.in -kpath hex 

This execution will analyze the presence of magnetism and/or spin orbit coupling 
in the input, to create the files for the bands calculation.
The flag -kpath allows to select a particular bandpath from the ones defined in QuantumTools.
  
.. warning::
   The path library is under development, you can see the available paths in 'create_bands.py -h'.

.. note::
   By default calculations are performed with 20 kpoints per segment of the path,
   that is usually an appropiate number of points.

Options
=======

.. _create_bands:

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
-----------------
Kpoint path to calculate the band structure
   
   Optional: Yes

   Default: 'ort' (orthorombic path)
   
   Type: str