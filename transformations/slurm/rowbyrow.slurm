#!/bin/bash
#SBATCH --job-name=3_5
#SBATCH --partition=scavenge
#SBATCH --ntasks=1
#SBATCH --time=01:00:00
#SBATCH --export=ALL
#SBATCH --mail-user=jcm10@rice.edu
#SBATCH --mail-type=ALL

module load GCC/5.4.0  CUDA/7.5.18  OpenMPI/1.10.3
module load Python/3.5.2
python rowbyrow.py C11 $SLURM_ARRAY_TASK_ID $SLURM_ARRAY_TASK_COUNT

#sbatch --array=0-99 rowbyrow.slurm
