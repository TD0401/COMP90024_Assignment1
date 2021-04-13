#!/bin/bash
count=$(wc -l tempJson.json| awk '{print $1}')
time mpirun -n 4 python  HappyCityAnalysis.py tempJson.json $count
