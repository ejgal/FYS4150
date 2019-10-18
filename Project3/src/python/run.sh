#!/bin/bash -x
python run_montecarlo.py --exp 6 --points 40
python run_guassquad.py --N_start 1 --N_end 30
