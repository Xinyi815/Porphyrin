#!/bin/bash --login
#PBS -j oe
#PBS -o pormetal-stk-7to9.out
#PBS -l walltime=62:00:00
#PBS -l select=1:ncpus=48:mem=124gb
#PBS -N pormetal-stk-7to9

cd $PBS_O_WORKDIR
export XTBHOME="/rds/general/user/xw1619/home/anaconda3/pkgs/xtb-6.5.1-h97a9613_0/share/xtb"
export PATH=/rds/general/user/xw1619/home/anaconda3/bin:${PATH} 

module load anaconda3/personal
python stk_script_metal_7to9.py