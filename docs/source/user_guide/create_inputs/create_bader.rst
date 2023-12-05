.. create_bader:

***************
create_bader.py
***************

Usage
=====

This tool creates the files for performing a Bader analysis of charge transfer:

.. code-block:: console

   create_bader.py -input /mydir/qe.scf.in 

Options
=======

.. _create_bader:

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