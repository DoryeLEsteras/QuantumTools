
.. extract_vasp_bands:

*********************
extract_vasp_bands.py
*********************

Usage
=====

This is a first script for VASP. In Vasp the computed bands are located inside of 
the file OUTCAR, in a particular format that is not straightforward to extract.
There are different tools to directly plot the bands from the OUTCAR, but they do not 
provide the raw data in a simple-to-plot format, thus flexibility is lost.
'extract_vasp_bands.py' provides the bands in the format of QuantumEspresso, so 
you can plot them in a simple way. The script work in a very similar way than 'extract_repaired_bands.py':

.. code-block:: console

   extract_vasp_bands.py -outcar /mydir/OUTCAR  -hs 5

This execution extracts the repaired bands and provides you the data and the new
high symmetry points in the usual format.

Options
=======

.. _extract_vasp_bands:

-outcar, --outcar
-----------------
OUTCAR file of VASP 

   Optional: No

   Type: str

-outdir, --outdir
-----------------
Directory where the outputs will be generated.

   Optional: Yes

   Default: Directory selected with --input flag

   Type: str


-bands, --bands
---------------
File with the bands calculated with bands.x (the wrong ones)

   Optional: No

   Type: str

-nk, --nk
---------
Number of high symmetry points in the calculation (Ex: Gamma-K-M-K-Gamma -> 5)
   
   Optional: No 
   
   Type: int