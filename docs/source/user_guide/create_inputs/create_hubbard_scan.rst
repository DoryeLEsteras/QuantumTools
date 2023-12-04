.. create_hubbard_scan:

**********************
create_hubbard_scan.py
**********************

Usage
=====
Let's say you already have your optimized structure, with converged parameters. Something very useful you can do in the case your material has strongly correlated electrons (d or f orbitals) is to perform an scan of the Hubbard parameters. For this, 'create_u_scan.py' prepares a grid of calculations varying the Hubbard U parameters:

Brute force method
------------------
.. code-block:: console

   create_hubbard_scan.py -input qe.scf.in -min 1.0 -max 6.0 -step 0.5 -version new
 
.. note::

   As already discussed in the 'create_template.py' script, in version 7.0 of QuantumEspresso the input format for the Hubbard parameters was drastically modified. You can choose the format of your input with the flag -version, specifying 'old' (< 7.0) or 'new' (>= 7.0).

.. warning::

   At the moment Hubbard V and Hubbard J are not implemented. Also if you have different atoms with Hubbard U, the script will generate homogeneous grid of U for both of them.

Options
=======
.. _create_u_scan:

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
-----------
Minimum value for Hubbard U scan
   
   Optional: No

   Type: float

-max, --max
-----------
Maximum value for Hubbard U scan
   
   Optional: No

   Type: float

-step, --step
-------------
Step value for Hubbard U scan
   
   Optional: No

   Type: float

-version, --version
-------------------
Version of QuantumEspresso to format the template (< 7.0 or >= 7.0)

   Optional: No

   Type: str

   Options: old, new
