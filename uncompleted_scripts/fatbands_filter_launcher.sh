for i in $(seq 2 1 6)
do
python3 ../scripts/fatbands_filter.py -input /mnt/c/Users/Work/Desktop/mirko_merry_christmas/deep_analisis_nm_4S_full_DFTsurfaces/typical_path/originals/feps3.nm.${i}_band.dat  -out /mnt/c/Users/Work/Desktop/mirko_merry_christmas/deep_analisis_nm_4S_full_DFTsurfaces/typical_path/feps3.nm.${i}_band.dat -mode 2 -cut 0.35
done
