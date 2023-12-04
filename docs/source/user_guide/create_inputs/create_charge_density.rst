.. create_charge_density:

************************
create_charge_density.py
************************

Usage
=====

This is a very simple tool for charge density calculations:

.. code-block:: console

   create_charge_density.py -input qe.scf.in 

Options
=======

.. _create_charge_density:

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