#!/bin/bash
#SBATCH --partition=snowy
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --time=0-1:00:00

module purge
module load foss/2019b
module load python/3.7.4

count=$(wc -l bigTwitter.json| awk '{print $1}')
time srun -n 8 python  HappyCityAnalysis.py bigTwitter.json $count
