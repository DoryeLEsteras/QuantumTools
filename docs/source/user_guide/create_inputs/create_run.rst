.. create_run:


*************
create_run.py
*************

Usage
=====

As previously discussed, QuantumTools already creates batch scripts to launch the 
calculations in your clusters. However at a certain moment, maybe you already 
have an input, and you just need to create the run file. For this you can use 
create_run.py, that will create runs for the configured clusters and adapted to 
your type of calculations.

.. code-block:: console

   create_run.py -input /mydir/qe.scf.in -calculation band_alignment

This execution takes the 'qe.scf.in' input file and creates the run files 
(one per configured cluster) to submit a band alignment calculation using QuantumEspresso.

Options
=======

.. _create_run:

-input, --input
---------------
Calculation file. The run files will be created around this name.

   Optional: No

   Type: str

-calculation, --calculation
---------------------------
Type of calculation to run
   
   Optional: No 
   
   Type: str

   Options: 
   
   * basic_scf 
   * spin_bands
   * nospin_bands
   * projected
   * cd
   * sd
   * bader
   * band_alignment
   * spin_wannier
   * nospin_wannier
   * force_theorem
   * wt

