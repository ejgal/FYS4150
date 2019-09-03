#!/bin/bash

n='10 100 1000 10000 100000 1000000'


for i in $n; do
  python thomas.py $i
  python toeplitz.py $i
done



# rm -r plots/*.png
# for i in $n; do
#   python thomas.py $i 1b_"$i"points.png
#   python toeplitz.py $i 1c_"$i"points.png
# done
#
