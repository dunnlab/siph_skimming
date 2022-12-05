#!/bin/bash

#SBATCH --job-name=snake
#SBATCH --output=snake.txt
#SBATCH --requeue
#SBATCH --time=2-00:00:00
#SBATCH --partition=general
#SBATCH --nodes=1                    # number of cores and nodes
#SBATCH --cpus-per-task=1           # number of cores
#SBATCH --mem-per-cpu=4G             # shared memory, scaling with CPU request

# Set up paths
cwd=$(pwd)
echo $cwd
base=$(basename $cwd)
echo $base
scratch_dir="/gpfs/ysm/scratch60/dunn/cwd7/$base"
echo "Using this scratch dir for output: "
echo $scratch_dir
mkdir -p $scratch_dir


zcat /gpfs/ysm/scratch60/dunn/cwd7/Novaseq_siphgenomes/Sample_CWD116_134_059/* > $scratch_dir/Agalma-elegans_CWD116.fastq
zcat /gpfs/ysm/scratch60/dunn/cwd7/Novaseq_siphgenomes/Sample_CWD122_133_060/* > $scratch_dir/Chelophyes_CWD122.fastq
zcat /gpfs/ysm/scratch60/dunn/cwd7/Novaseq_siphgenomes/Sample_NA10_182_011/* >   $scratch_dir/Resomia_NA10.fastq
zcat /gpfs/ysm/scratch60/dunn/cwd7/Novaseq_siphgenomes/Sample_CWD6_184_009/* >   $scratch_dir/Cordagalma_CWD6.fastq



head $scratch_dir/Agalma-elegans_CWD116.fastq -n 6211280156 >  $scratch_dir/Agalma-elegans_CWD116_100x.fastq
head $scratch_dir/Agalma-elegans_CWD116.fastq -n 5590152140 >  $scratch_dir/Agalma-elegans_CWD116_090x.fastq
head $scratch_dir/Agalma-elegans_CWD116.fastq -n 4969024124 >  $scratch_dir/Agalma-elegans_CWD116_080x.fastq
head $scratch_dir/Agalma-elegans_CWD116.fastq -n 4347896108 >  $scratch_dir/Agalma-elegans_CWD116_070x.fastq
head $scratch_dir/Agalma-elegans_CWD116.fastq -n 3726768092 >  $scratch_dir/Agalma-elegans_CWD116_060x.fastq
head $scratch_dir/Agalma-elegans_CWD116.fastq -n 3105640076 >  $scratch_dir/Agalma-elegans_CWD116_050x.fastq
head $scratch_dir/Agalma-elegans_CWD116.fastq -n 2484512060 >  $scratch_dir/Agalma-elegans_CWD116_040x.fastq
head $scratch_dir/Agalma-elegans_CWD116.fastq -n 1863384048 >  $scratch_dir/Agalma-elegans_CWD116_030x.fastq
head $scratch_dir/Agalma-elegans_CWD116.fastq -n 1242256032 >  $scratch_dir/Agalma-elegans_CWD116_020x.fastq

head $scratch_dir/Chelophyes_CWD122.fastq -n 2559270292 > $scratch_dir/Chelophyes_CWD122_080x.fastq
head $scratch_dir/Chelophyes_CWD122.fastq -n 2239361504 > $scratch_dir/Chelophyes_CWD122_070x.fastq
head $scratch_dir/Chelophyes_CWD122.fastq -n 1919452720 > $scratch_dir/Chelophyes_CWD122_060x.fastq
head $scratch_dir/Chelophyes_CWD122.fastq -n 1599543932 > $scratch_dir/Chelophyes_CWD122_050x.fastq
head $scratch_dir/Chelophyes_CWD122.fastq -n 1599543932 > $scratch_dir/Chelophyes_CWD122_040x.fastq
head $scratch_dir/Chelophyes_CWD122.fastq -n 959726360 > $scratch_dir/Chelophyes_CWD122_030x.fastq
head $scratch_dir/Chelophyes_CWD122.fastq -n 639817572 > $scratch_dir/Chelophyes_CWD122_020x.fastq

head $scratch_dir/Resomia_NA10.fastq -n 4428771880 > $scratch_dir/Resomia_NA10_100x.fastq
head $scratch_dir/Resomia_NA10.fastq -n 3985894692 > $scratch_dir/Resomia_NA10_090x.fastq
head $scratch_dir/Resomia_NA10.fastq -n 3543017504 > $scratch_dir/Resomia_NA10_080x.fastq
head $scratch_dir/Resomia_NA10.fastq -n 3100140316 > $scratch_dir/Resomia_NA10_070x.fastq
head $scratch_dir/Resomia_NA10.fastq -n 2657263128 > $scratch_dir/Resomia_NA10_060x.fastq
head $scratch_dir/Resomia_NA10.fastq -n 2214385940 > $scratch_dir/Resomia_NA10_050x.fastq
head $scratch_dir/Resomia_NA10.fastq -n 1771508752 > $scratch_dir/Resomia_NA10_040x.fastq
head $scratch_dir/Resomia_NA10.fastq -n 1328631564 > $scratch_dir/Resomia_NA10_030x.fastq
head $scratch_dir/Resomia_NA10.fastq -n 885754376 > $scratch_dir/Resomia_NA10_020x.fastq

head $scratch_dir/Cordagalma_CWD6.fastq -n 1104324048 > $scratch_dir/Cordagalma_CWD6_060x.fastq
head $scratch_dir/Cordagalma_CWD6.fastq -n 920270040 > $scratch_dir/Cordagalma_CWD6_050x.fastq
head $scratch_dir/Cordagalma_CWD6.fastq -n 736216032 > $scratch_dir/Cordagalma_CWD6_040x.fastq
head $scratch_dir/Cordagalma_CWD6.fastq -n 552162024 > $scratch_dir/Cordagalma_CWD6_030x.fastq
head $scratch_dir/Cordagalma_CWD6.fastq -n 368108016 > $scratch_dir/Cordagalma_CWD6_020x.fastq