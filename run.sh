#!/bin/bash
count=$(wc -l smallTwitter.json| awk '{print $1}')
time mpirun -n 1 python  HappyCityAnalysis.py smallTwitter.json $count
