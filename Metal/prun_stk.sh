#!/bin/bash --login
#PBS -j oe
#PBS -o pormetal-stk.out
#PBS -l walltime=72:00:00
#PBS -l select=1:ncpus=48:mem=124gb
#PBS -N pormetal-stk

cd $PBS_O_WORKDIR
export XTBHOME="/rds/general/user/xw1619/home/anaconda3/pkgs/xtb-6.5.1-h97a9613_0/share/xtb"
export PATH=/rds/general/user/xw1619/home/anaconda3/bin:${PATH} 

module load anaconda3/personal
python stk_script_metal.py
