#!/bin/bash --login

#SBATCH --job-name=PhNO2_C8_9
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=10
#SBATCH --time=240:00:00

export OPENBLAS_NUM_THREADS=1
export OMP_STACKSIZE=10G
export OMP_NUM_THREADS=10
#export OMP_MAX_ACTIVE_LEVELS=1
#export LD_LIBRARY_PATH=/home/vposligua/miniconda3/lib/
#export PATH=/home/vposligua/bin/xtb/compiled/usr/local/bin:${PATH}
#export XTBHOME="/usr/local/share/xtb"
#export PATH=/usr/local/bin:${PATH}

ulimit -s unlimited
srun xtb xtbopt.xyz --gfn 1 --vipea > vipea_PhNO2_C8_9.txt
