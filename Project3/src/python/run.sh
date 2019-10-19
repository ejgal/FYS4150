#!/bin/bash -x
python run_guassquad.py --N_start 1 --N_end 50
python run_montecarlo.py --exp 10 --points 50
