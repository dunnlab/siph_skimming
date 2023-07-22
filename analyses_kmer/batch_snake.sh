#!/bin/bash

#SBATCH --job-name=snake
#SBATCH --output=snake.txt
#SBATCH --time=1-00:00:00
#SBATCH --partition=pi_dunn
#SBATCH --nodes=1                    # number of cores and nodes
#SBATCH --cpus-per-task=16           # number of cores
#SBATCH --mem-per-cpu=10G            # shared memory, scaling with CPU request

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

# module load Jellyfish
# module load snakemake # This one is an old version
module load miniconda
#mamba activate snakemake
conda activate snakemake
snakemake --cores $SLURM_CPUS_PER_TASK
