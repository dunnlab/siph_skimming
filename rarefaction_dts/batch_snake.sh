#!/bin/bash

#SBATCH --job-name=snake
#SBATCH --output=snake.txt
#SBATCH --time=4-00:00:00
#SBATCH --partition=pi_dunn
#SBATCH --nodes=1                    # number of cores and nodes
#SBATCH --cpus-per-task=18           # number of cores
#SBATCH --mem-per-cpu=10G             # shared memory, scaling with CPU request

# Set up paths
cwd=$(pwd)
echo $cwd
base=$(basename $cwd)
echo $base
scratch_dir="/gpfs/ysm/scratch60/dunn/cwd7/$base"
echo "Using this scratch dir for output: "
echo $scratch_dir
mkdir -p $scratch_dir

module purge # Unload any existing modules that might conflict
module load Jellyfish
module load miniconda
conda activate snakemake

snakemake \
  --cores $SLURM_CPUS_PER_TASK \
  --directory $scratch_dir \
  --configfile config.yaml \
  --snakefile GGSR

# snakemake --unlock --cores $SLURM_CPUS_PER_TASK
