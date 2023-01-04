Scripts included:

LIBRARIES

run_manager                            DONE 

INPUT GENERATION

create_bands                          DONE 
create_projected                      DONE 
create_wannier                        IN PROCESS
optimization_manager                  IN PROCESS     (restarts optimizations and create scfs from optimization) 
create_force_theorem                  IN PROCESS
create_spin_density                   DONE 
create_charge_density                 DONE 
create_hubbard_scanning               EMPTY
create_Hubbard_convergence            bash
create_Hubbard_scf_calculation        EMPTY
create_qe_template                    EMPTY
create_sw 	                      IN PROCESS
create_band_alignment                 EMPTY
create_bader_analysis                 EMPTY
create_wannier_fatbands               EMPTY  (this should be just an addition to the create_wannier)
create_wannier_functions              EMPTY  (this should be just an addition to the create_wannier)
create_strain                         bash
create_wannier_tools                 EMPTY

smearing_tester
kpoint tester
cutoff tester

OUTPUT MANAGMENT

bands_repair	                      IN PROCESS
polinomials                           IN PROCESS
energy_method                         bash
tb2j_filter 	                      IN PROCESS
scf_output_analyser                   EMPTY 
gaussian_filter                       DONE 
wannier90_hamiltonian_reader          COMPLETE
convergence_checker                   bash
fatbands_filter                       COMPLETE

PLOTTERS
resolved_exchange_strain_u_plotter   COMPLETE

BASH launchers
tb2j_launcher                        DONE

