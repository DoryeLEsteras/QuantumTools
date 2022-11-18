
# TO DO LIST

"""
-extend the names of outputs (or parser)
-adapt spread extraction to noncolin case where spin=up,down
-extract magnetic moment per atom
-consider python
-plots everywhere
"""


prefix=cri3
component=z
rm scf_conv.txt
rm nscf_conv.txt
rm wout_conv.txt
rm spread_conv.txt
rm energy.txt
rm total_magnetization.txt

for str in $(seq 95 1 105)
    do
    for U in $(seq 2.0 1.0 6.0)
        do
        # total spread will CRASH if there is spin_up and spin_down in the same folder
        totalspread=$(grep 'Final Spread (Ang^2)' ${prefix}*${str}*${component}*${U}*wout | awk '{print $7}')
        energy=$(grep ! ${prefix}.${str}.${component}.${U}.scf.out | awk '{print $5}')
        totalmagx=$(grep 'total magnetization' ${prefix}.${str}.${component}.${U}.scf.out  | tail -1 | awk '{print $4}')
        totalmagy=$(grep 'total magnetization' ${prefix}.${str}.${component}.${U}.scf.out  | tail -1 | awk '{print $5}')
        totalmagz=$(grep 'total magnetization' ${prefix}.${str}.${component}.${U}.scf.out  | tail -1 | awk '{print $6}')  
        scf=$(grep 'convergence h' ${prefix}.${str}.${component}.${U}.scf.out)
        nscf=$(grep 'Writing output' ${prefix}.${str}.${component}.${U}.nscf.out)
        wout=$(grep 'convergence' ${prefix}.${str}.${component}.${U}.wout)
        echo "$str $U $scf" >>scf_conv.txt
        echo "$str $U $nscf" >>nscf_conv.txt
        echo "$str $U $wout" >>wout_conv.txt
        echo "$str $U $totalspread" >>spread_conv.txt
        echo "$str $U $energy" >>energy.txt
        echo "$str $U $totalmagx $totalmagy $totalmagz" >>total_magnetization.txt
        
    done
    echo "-----------------------------------" >> scf_conv.txt
    echo "-----------------------------------" >> nscf_conv.txt
    echo "-----------------------------------" >> wout_conv.txt
    echo "-----------------------------------" >> spread_conv.txt
    echo "-----------------------------------" >> energy.txt
    echo "-----------------------------------" >> total_magnetization.txt
done