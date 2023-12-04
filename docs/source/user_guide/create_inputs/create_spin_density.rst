.. create_spin_density:

**********************
create_spin_density.py
**********************

Usage
=====

Similar to 'charge_density.py', it is straightforward to create the inputs for spin density calculations:

.. code-block:: console

   create_spin_density.py -input qe.scf.in 

Options
=======

.. _create_spin_density:

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