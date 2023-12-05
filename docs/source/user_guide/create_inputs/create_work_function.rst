.. create_work_function:

***********************
create_work_function.py
***********************

Usage
=====

Another simple tool, this time for performing work function calculations:

.. code-block:: console

   create_work_function.py -input /mydir/qe.scf.in 

.. note::
   At the moment the input file guide for the file .avg can be just found in the 
   QuantumEspresso code. It is a good practice to read about the parameters of the 
   calculation. In particular herein I assume vacuum is in z direction.

Options
=======

.. _create_work_function:

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