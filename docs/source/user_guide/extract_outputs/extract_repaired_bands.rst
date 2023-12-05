.. extract_repaired_bands:

*************************
extract_repaired_bands.py
*************************

Usage
=====

In some particular cases, QuantumEspresso experiments a problem during the 
printing of the band structure. You can observe this when in the output of the bs
file/files (the output of bands.x) two high symmetry points are degenerated. 
The origin of this is a bad printing of the k point path, given the correct 
information is present in the bands.out file (the pw.x output file). To obtained
the repaired bands and high symmetry points you can use 'extract_repaired_bands.py':

.. code-block:: console

   extract_repaired_bands.py -input /mydir/qe.bands.out -bands qe.bands.dat.gnu -hs 5

This execution extracts the repaired bands and provides you the data and the new
high symmetry points in the usual format.


.. warning::
   At the moment just homogeneous k point paths are implemented. 
   (Ex: always 20 points between segments of the path, except the last one of course)

Options
=======

.. _extract_repaired_bands:

-input, --input
---------------
Bands.out file calculated with pw.x (not bands.x) 

   Optional: No

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