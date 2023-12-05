.. create_updated_optimization:

******************************
create_updated_optimization.py
******************************

Usage
=====
The objective of this tool is to help you in after the optimization of the structure.
If the calculation was uncompleted it will create a new file and run to continue 
with the relax or vc-relax calculation, but if convegence was reached it will 
create an updated scf file with the new structure and some flags that you could 
consider for your new scf calculation.


.. note::
   The script will transform always the structures to ibrav 0 using the cell_parameters matrix.
   It is important to understand that this script is going to be one of the most 
   important origins of scf files. Given that some applications such as the Wannier 
   calculations just admit ibrav 0 specifying the cell parameter matrix, all the 
   scripts of QuantumTools will move around this convention.

.. warning::
   There is one particular case in QuantumEspresso where ibrav = 0 is not admisible,
   this is the case of optimizations that use cell_dofree = 'ibrav'. If ibrav 0
   is used in this case, your calculation will continue running but in the output
   you will see a warning and basically you will be loosing time. In this case
   is important to use ibrav != 0, but this transformation is not implemented
   yet in QuantumTools, instead 'create_updated_optimization' will print a 
   warning to remind you that if you selected this conditions by purpose, 
   you should manually move to ibrav !=0.

Let's see two examples of the script usage:

.. code-block:: console

   create_updated_optimization.py -optin /mydir/qe.vcrelax.in -optout /mydir/qe.vcrelax.out -newname qe.vcrelax2.in

This execution takes the 'qe.vcrelax.in' input file and the new structure of 
'qe.vcrelax.out' to create a new vcrelax input 'qe.vcrelax2.in' to continue with the calculations.

.. code-block:: console
   
   create_updated_optimization.py -optin /mydir/qe.relax.in -optout /mydir/qe.relax.out

This execution takes the 'qe.relax.in' input file and the optimized structure of
'qe.relax.out'. This relax was converged until the end, thus the script directly
creates a new scf and there is no necessity to specify the -newname flag.

Options
=======

.. _create_updated_optimization:

-optin, --optin
---------------
Initial vcrelax/relax input file

   Optional: No

   Type: str

-optout, --optout
-----------------
Vcrelax/relax output file. 

   Optional: No

   Type: str

-newname, --newname
-------------------
Name for the vcrelax/relax input file for the new calculation.
   
   Optional: No if the optimization was not converged. Ignored if the optimization finished successfully.

   Type: str

