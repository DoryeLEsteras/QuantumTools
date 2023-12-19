
for i in $(seq 95 1 105)
do
grep 'Cr1   Cr1' TB2J_results.$i/exchange.out | head -6 | awk '{print $7}'   >    J1.exchange.cucrse.$i.txt
grep 'Cr2   Cr2' TB2J_results.$i/exchange.out | head -6 | awk '{print $7}'  >    J2.exchange.cucrse.$i.txt
grep 'Cr1   Cr1' TB2J_results.$i/exchange.out | head -12 | tail -6  | awk '{print $7}'>   J3.exchange.cucrse.$i.txt
grep 'Cr2   Cr2' TB2J_results.$i/exchange.out | head -12 | tail -6  | awk '{print $7}'>   J4.exchange.cucrse.$i.txt
grep 'Cr'        TB2J_results.$i/exchange.out | head -34 | tail -6  | awk '{print $7}'>   J5.exchange.cucrse.$i.txt
done

echo "" > J1.txt;echo "" > J2.txt;echo "" > J3.txt;echo "" > J4.txt;echo "" > J5.txt
for i in $(seq 95 1 105)
do
	echo " $i $(paste -sd+ J1.exchange.cucrse.$i.txt | bc)" >> J1.txt
	echo " $(paste -sd+ J2.exchange.cucrse.$i.txt | bc)" >> J2.txt	
	echo " $(paste -sd+ J3.exchange.cucrse.$i.txt | bc)" >> J3.txt
	echo " $(paste -sd+ J4.exchange.cucrse.$i.txt | bc)" >> J4.txt
	echo " $(paste -sd+ J5.exchange.cucrse.$i.txt | bc)" >> J5.txt
done

paste -d ' ' J1.txt J2.txt J3.txt J4.txt J5.txt > J.txt
