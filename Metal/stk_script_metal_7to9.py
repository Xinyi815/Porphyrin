# import sys
# sys.path.append('/Applications/anaconda3/lib/python3.8/site-packages')

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

# RDkit logger
rdkit_logger = RDLogger.logger()
rdkit_logger.setLevel(RDLogger.CRITICAL)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
#%matplotlib inline

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


metal_name = ['Fe','Co','Ni','Cu','Zn']
FG_name = ['m-CP','PhOH','Ph3OH']
linker_name = ['C2','C4','C6','C8']
units_name = ['2','3','4']

def porphyrin_unit_M(M_smile, metal_atom):
    porphyrin_Br = stk.BuildingBlock(
        smiles= M_smile,
        functional_groups=(
            stk.SmartsFunctionalGroupFactory(
                smarts='[#6!H]~[#7]~[#6!H]',
                bonders=(1,),
                deleters=(),
            ),
            stk.BromoFactory(),
        ),
    )
    porphyrin_Br = stko.UFF().optimize(porphyrin_Br)

    complex_M_Br = stk.ConstructedMolecule(
        topology_graph=stk.metal_complex.Porphyrin(
            metals=metal_atom,
            ligands=porphyrin_Br,
            optimizer=stk.MCHammer(),
        )
    )

    bb_M = stk.BuildingBlock.init_from_molecule(complex_M_Br,
        functional_groups=[stk.BromoFactory(),
        ]
    )

    return bb_M

# Metal centre porphyrin
metal_centers = [
    stk.BuildingBlock(
        smiles='[Fe+2]',
        functional_groups=(
            stk.SingleAtom(stk.Fe(0, charge=2))
            for i in range(6)
        ),
        position_matrix=[[0, 0, 0]],
    ),

    stk.BuildingBlock(
        smiles='[Co+2]',
        functional_groups=(
            stk.SingleAtom(stk.Co(0, charge=2))
            for i in range(6)
        ),
        position_matrix=[[0, 0, 0]],
    ),

        stk.BuildingBlock(
        smiles='[Ni+2]',
        functional_groups=(
            stk.SingleAtom(stk.Ni(0, charge=2))
            for i in range(6)
        ),
        position_matrix=[[0, 0, 0]],
    ),

        stk.BuildingBlock(
        smiles='[Cu+2]',
        functional_groups=(
            stk.SingleAtom(stk.Cu(0, charge=2))
            for i in range(6)
        ),
        position_matrix=[[0, 0, 0]],
    ),

    stk.BuildingBlock(
        smiles='[Zn+2]',
        functional_groups=(
            stk.SingleAtom(stk.Zn(0, charge=2))
            for i in range(6)
        ),
        position_matrix=[[0, 0, 0]],
    ),

]

# Define BB dictionaries.
bb1_M_smiles ={}
bb3_M_smiles = {}
bb1_M_file= open ('FG_Metal_7to9.txt','r')
for i, bb in enumerate(bb1_M_file.readlines()):
    bb1_M_smiles[i] = bb.replace('\n','')


linker_smiles = {}
linker = open ('linker.txt','r')
for i, li in enumerate(linker.readlines()):
    linker_smiles[i] = li.replace('\n','')



# Over metal atoms
for ma in range(0,len(metal_centers)):
    # # Iterate over BB1 (Initial porphyrin unit with 2 Br)
    for bb1id in bb1_M_smiles:
        bb1_M = porphyrin_unit_M(bb1_M_smiles[bb1id], metal_centers[ma])
        # Optimize with stko.
        # bb1_M = stko.UFF().optimize(bb1_Zn)

        bb3_M_smiles[i] = bb1_M_smiles[bb1id].replace('Br/','')

        # Iterate over BB3 ((Initial porphyrin unit with 1 Br))
        for bb3id in bb3_M_smiles:
            bb3_M = porphyrin_unit_M(bb3_M_smiles[bb3id], metal_centers[ma])
            # bb3_M = stko.UFF().optimize(bb1_Zn)

            # Iterate over linker.
            for liid in linker_smiles:
                linker = stk.BuildingBlock(
                    smiles=linker_smiles[liid],
                    functional_groups=[stk.BromoFactory()],
                )
                
                # Iterate over repeat units.
                for no in range(0,3):
                    repeat_units = no
                    repeating_unit_str='CB'+'AB'*repeat_units +'C'
                    orientation_str = '0, '*(len(repeating_unit_str)-1)+'1'
                    # Set name based on iterations.
                    molecule_name = f'{metal_name[ma]}_{FG_name[bb1id]}_{linker_name[liid]}_{units_name[no]}'
                    print(molecule_name)
                    


                    porphyrin_M = stk.ConstructedMolecule(
                        topology_graph=stk.polymer.Linear(
                            building_blocks=(bb1_M, linker, bb3_M),
                            repeating_unit=repeating_unit_str,
                            num_repeating_units=1,
                            orientations=tuple(map(int, orientation_str.split(', '))),
                            #optimizer=stk.MCHammer(),
                            optimizer=stk.Collapser(scale_steps=False),
                        ),
                    )

                    # Write to files.
                    #porphyrin_noM.write(f'{molecule_name}.mol')
                    porphyrin_M.write(f'{molecule_name}.xyz')
                    os.makedirs(f'{molecule_name}')
                    os.chdir(f'{molecule_name}')
                    os.system(f'mv ../{molecule_name}.xyz .')
                    #os.environ['XTBHOME'] = "/home/xwu/miniconda3/pkgs/xtb-6.4.1-hf06ca72_0/share/xtb"
                    os.system(f'xtb {molecule_name}.xyz --gfn 1 --opt -T 48 > output_{molecule_name}.txt && xtb xtbopt.xyz --gfn 1 --vipea > vipea_{molecule_name}.txt')
                    os.chdir('../')                   
                    #show_stk_mol(porphyrin_M)     
