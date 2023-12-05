
.. extract_wan_h:

****************
extract_wan_h.py
****************

Usage
=====
The objective of this tool is to extract the hoppings and on-site parameters of Wannier90
Hamiltonian in a more understandable format. The Hamiltonian is divided in 4 regions: 

.. centered:: Hamiltonian matrix format

.. list-table:: 
   :widths: 50 50
   :header-rows: 0

   * - .. centered:: d-d
     - .. centered:: d-l
   * - .. centered:: l-d
     - .. centered:: l-l

These 4 Hamiltonians represent the hoppings between the metallic centers (d-d, direct hopping)
between ligands (l-l) and between ligands and metallic centers (d-l and l-d) (signature of superexchange mechanism).

.. note::
   The actual notation comes from the fact, this was originally developed for d-orbitals
   and ligands, but it can be used for any kind of orbitals, like f.

Let's see an example of usage:

.. code-block:: console

   extract_fatbands.py -input /mydir/qe.bands.dat.gnu -cut 0.1 -norb 10

This execution will extract the mentioned Hamiltonians separatelly for every cell
of the Wannier Hamiltonian. The 'cut' flag allows to round to zero, the hoppings
that are under a particular value. This is useful to remove the hoppings that are
not significant, and see a clear picture of the Hamiltonian. 'norb' indicates that
the first Hamiltonian (d-d) is going to be formed by the first 10 orbitals (10x10 matrix)
thus, it determines all the matrices.

.. warning::
  norb is a fundamental parameter to extract correctly the matrices. Make sure 
  you correctly choose it, specially in noncollinear or spin-orbit calculations
  were the amount of Wannier functions is doubled.

Options
=======

.. _extract_wan_h:

-input, --input
---------------
Bands.dat file calculated with wannier90 (or QuantumEspresso). It should have a
column with the weight of the contribution

   Optional: No

   Type: str

-outdir, --outdir
-----------------
Directory where the outputs will be generated.

   Optional: Yes

   Default: Directory selected with --input flag

   Type: str

-cut, --cut
-----------
Cutoff to filter the hoppings.
   
   Optional: Yes

   Default: 0.0
   
   Type: float

-norb, --norb
-------------
Number of orbitals to create the first Hamiltonian (d-d). 
Ex: if nwan = 40 and norb = 10, the dimensions of the Hamiltonians will be:

* Hd_d = 10x10
* Hl_l = 30x30
* Hd_l = 10x30
* Hl_d = 30x10

   Optional: No 
   
   Type: int