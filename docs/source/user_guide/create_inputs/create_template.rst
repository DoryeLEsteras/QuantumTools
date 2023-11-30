.. installation:

******************
create_template.py
******************

Usage
=====

The first thing you can do to start a project, is create a template for your structure. This template contains all the basic flags you should consider in a QuantumEspresso calculation.
It is fast, and avoids forgetting an important flag in the modelling of the systems. To do this you can use the 'create_template.py' script:

.. code-block:: console

   create_template.py -input qe.scf.in -calculation scf -version new

This execution creates a QuantumEspresso file called 'qe.scf.in' with the parameters required for the selected calculation type (scf, relax or vc-relax). 


.. note::
   An important point to consider is that in QuantumEspresso version 7.0, the input format was changed (in particular for the Hubbard corrections). Because of this, you create_template has a flag called 'version' to generate templates for the 'old' or 'new' versions.


Options
=======

.. _create_template:

-input, --input
---------------
Name for the template 

   Optional: No
   Type: str

-calculation, --calculation
---------------------------
Type of calculation to run
   
   Optional: No 
   
   Type: str

   Options: scf, relax, vc-relax


-version, --version
-------------------
Version of QuantumEspresso to format the template (< 7.0 or >= 7.0)

   Optional: No 
   
   Type: str

   Options: old, new
