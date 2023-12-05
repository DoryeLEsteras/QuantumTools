
.. extract_fatbands:

*******************
extract_fatbands.py
*******************

Usage
=====

This is a tool to do postprocessing of fatbands calculated with Wannier90. 
When bands are resolved in orbitals, the contributions are plotted in colors over
the bandstructure. In the case you have many bands (the excellent example are
ARPES calculations with many layers) is very difficult to see the
contributions of each band. This tool allows to remove the bands that are not interesting
from the data files, using the '-cut' flag and the two different modes available, let's see some examples:

.. code-block:: console

   extract_fatbands.py -input /mydir/qe.bands.dat.gnu -out /mydir/newfile_mode1.dat.gnu -cut 0.1 -mode 1

This execution uses mode 1, and as an example we used cut 0.1. The cut flag will
remove all the bands where the contribution of the selected orbitals is less than 0.1.
Mode 1 implies the bands that in some kpoints, have more than 0.1 constribution,
will be fully extracted, including the regions were the orbital contribution is lower than 0.1.
Plotting this data will result in figures where the bands are complete and not 
just pieces, however it will be more difficult to see the information, because
plots will have too much useless information or too few bands.
In the case you want a more detailed analysis and you admit extracting just the 
regions of the bands where contribution is significant, you should use mode 2:

.. code-block:: console

   extract_fatbands.py -input /mydir/qe.bands.dat.gnu -out /mydir/newfile_mode2.dat.gnu -cut 0.1 -mode 2

This mode is going to very accuratelly extract just the regions where the orbitals
selected really have a significative role, however your plots will not contain complete bands in most of the cases.

.. note::
   Play with different cutoffs and modes to obtain information about your system.
   You can automatize this with a loop in a bash script.
    
Options
=======

.. _extract_fatbands:

-input, --input
---------------
Bands.dat file calculated with wannier90 (or QuantumEspresso). It should have a
column with the weight of the contribution

   Optional: No

   Type: str

-out, --out
-----------
Output name and directory for the new file.

   Optional: No

   Type: str

-cut, --cut
-----------
Cutoff to filter the weights.
   
   Optional: Yes

   Default: 0.0
   
   Type: float

-mode, --mode
-------------
Mode for band extraction (mode 1: full bands mode 2: regions of bands)
   
   Optional: No 
   
   Type: int (1 or 2)