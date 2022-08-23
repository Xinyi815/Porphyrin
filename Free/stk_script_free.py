import sys
#sys.path.append('/Applications/anaconda3/lib/python3.8/site-packages')

from rdkit import Chem 
from rdkit.Chem import AllChem as rdkit
from collections import defaultdict
from rdkit.Chem import rdFMCS
from rdkit.Chem import Draw
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem import rdDistGeom
IPythonConsole.ipython_3d = True

import py3Dmol
from IPython.display import Image
import matplotlib.pyplot as plt
import subprocess
import time
import stk
import stko
import os
import spindry as spd
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdDistGeom
from rdkit.Chem import rdMolAlign
from rdkit import RDLogger
import logging


def show_stk_mol(stk_mol):
    data = rdkit.MolToMolBlock(stk_mol.to_rdkit_mol())
    p = py3Dmol.view(
        data=data,
        style={'stick':{'colorscheme':'cyanCarbon'}}, 
        width=400,
        height=400,
    )
    p.setBackgroundColor('0xeeeeee')
    p.zoomTo()
    p.show()


# Optimize with the MMFF force field.
def rdkit_op(bb):
    rdkit_bb = bb.to_rdkit_mol()
    rdkit.SanitizeMol(rdkit_bb)
    rdkit.MMFFOptimizeMolecule(rdkit_bb)

    # stk molecules are immutable. with_position_matrix returns a
    # a clone, holding the new position matrix.
    bb = bb.with_position_matrix(
        position_matrix=rdkit_bb.GetConformer().GetPositions(),
    )

    return bb


FG_name = ['H','Py','DHP','C2Py','Ph','p-CP','m-CP','PhOH','Ph3OH','PhCHO','Ph2Me','Ph3Me','Ph2OMe','BSA','PhCN','NMA','PhNH2','PhNO2']
linker_name = ['C2','C4','C6','C8']
units_name = ['2','3','4','5','6','7','8','9','10']

bb1_free = open ('FG_free.txt','r')
linker = open ('linker.txt','r')

# Define BB dictionaries.
bb1_smiles = {}
bb3_smiles = {}
for i, bb in enumerate(bb1_free.readlines()):
    bb1_smiles[i] = bb.replace('\n','')
    

linker_smiles = {}
for i, li in enumerate(linker.readlines()):
    linker_smiles[i] = li.replace('\n','')


# Iterate over BB1.
for bb1id in bb1_smiles:
    bb1 = stk.BuildingBlock(bb1_smiles[bb1id], [stk.BromoFactory()])
    # Optimize with the MMFF force field.
    bb1 = rdkit_op(bb1)
    bb3_smiles[i] = bb1_smiles[bb1id].replace('Br/','')

    # Iterate over BB3.
    for bb3id in bb3_smiles:
        bb3 = stk.BuildingBlock(bb3_smiles[bb3id], [stk.BromoFactory()])
        # Optimize with the MMFF force field.
        bb3 = rdkit_op(bb3)
            
        # Iterate over linkers.
        for liid in linker_smiles:
            linker = stk.BuildingBlock(
                smiles=linker_smiles[liid],
                functional_groups=[stk.BromoFactory()],
            )
            # Iterate over repeat units.
            for no in range(0,9):
                repeat_units = no
                repeating_unit_str='CB'+'AB'*repeat_units +'C'
                orientation_str = '0, '*(len(repeating_unit_str)-1)+'1'
                # Set name based on iterations.
                molecule_name = f'{FG_name[bb1id]}_{linker_name[liid]}_{units_name[no]}'
                
                #construct finial porphyrin arrays
                porphyrin_noM = stk.ConstructedMolecule(
                    topology_graph=stk.polymer.Linear(
                        building_blocks=(bb1, linker, bb3),
                        repeating_unit=repeating_unit_str,
                        num_repeating_units=1,
                        orientations=tuple(map(int, orientation_str.split(', '))),
                        #optimizer=stk.MCHammer(),
                        optimizer=stk.Collapser(scale_steps=False),

                    ),
                )
                
                # Write to files.
                #porphyrin_noM.write(f'{molecule_name}.mol')
                porphyrin_noM.write(f'{molecule_name}.xyz')
                os.makedirs(f'{molecule_name}')
                os.chdir(f'{molecule_name}')
                os.system(f'mv ../{molecule_name}.xyz .')
                #os.environ['XTBHOME'] = "/home/xwu/miniconda3/pkgs/xtb-6.4.1-hf06ca72_0/share/xtb"
                os.system(f'xtb {molecule_name}.xyz --gfn 1 --opt -T 48 > output_{molecule_name}.txt && xtb xtbopt.xyz --gfn 1 --vipea > vipea_{molecule_name}.txt')
                os.chdir('../')
            
                #show_stk_mol(porphyrin_noM