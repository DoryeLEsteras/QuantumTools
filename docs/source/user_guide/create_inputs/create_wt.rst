.. create_wt:

************
create_wt.py
************

Usage
=====

This is another script working in the interface between softwares. In particular, Wannier90-WannierTools.
Given WannierTools inputs are complex and allow to do many different calculations,
this script does not provide a complete input, but provides a template containing
all the necessary parameters you can be interested in. It saves time and avoids missing important flags.


.. code-block:: console

   create_wt.py -win /mydir/qe.win

Options
=======

.. _create_wt:

-win, --win
---------------
Initial Wannier input file

   Optional: No

   Type: str

-outdir, --outdir
-----------------
Directory where the outputs will be generated.

   Optional: Yes

   Default: Directory selected with --input flag

   Type: str