prefix=cri3
for strain in $(seq 95 1 105)
do
python3 magnon_gap_analyser.py -ac /Users/Dorye/Downloads/magnons_cri3/${prefix}.${strain}.0.0.0.omega2.txt -op /Users/Dorye/Downloads/magnons_cri3/${prefix}.${strain}.0.0.0.omega1.txt
done
