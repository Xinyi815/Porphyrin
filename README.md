# Porphyrin Electronic Properties
The main aim of this project is to use stk to build both free and metal-based (Fe,Co,Ni,Cu,Zn) porphyrin chains and xtb to obtain the optimised structure and electronic properties. Then Keras - deep machine learning model will be used to train our dataset and predict electronic properties of further configurations which are not considered in the constructed database.

## First part: building (stk) and optimisation (xtb)
- For loop was used to build all the porphyrin arrays.
- Then xtb used xyz files of constructed molecule to optimise and generate a series of files: The value of HOMO-LUMO (H-L) gap can be found in the output_molecule_name.txt file; The values of electron affinity (EA) and ionisation potential (IP) can be found in the vipea_molecule_name.txt file. The xtbopt.xyz and xtbtopo.mol can be used to see the finial optimised structure. 

## Obtain dataset
- After xtb optimisation, the values HOMO-LUMO (H-L) gap, electron affinity (EA) and ionisation potential (IP) of each molecule need to be abstracted.
- Also, descriptors (the physicochemical properties for the molecules) should be obtained from xtbtopo.mol (remember to covert xtbtopo.mol to an RDKit mol!)
Note: For free-based porphyrin chain: number of carbon atom in the linker and number of units are added to the descriptors; For metal-based porphyrin chain, atomic number of each metal center, number of carbon atom in the linker and number of units are added into the descriptors.
- Then descriptors, EA, IP and HL were combined together to obtain our finial dataset file.

## Keras - deep machine learning, training our dataset
- datasets of free-based one and metal-based one were trained separately.
Note: the HL value of Fe, Co, Cu in the metal's datasets are very close to 0 which is not correct so that they were excluded and were not used for training the model.
- When our model is successfully trained, we can change some properties such as C10 as a linker or different porphyrin unit and use the model_noEAIP (as we do not know the EA and IP values of new configurations) to predict HL values of a series of new configurations. 
- Random Forest model is used to check the consistency, reliability and accuracy of the Tensorflow Keras model.

## MTPP (metal meso-tetraphenyl porphines)
- The 5 structures MTPP (M = Fe, Co, Ni, Cu, Zn) from literature were also built by stk and optimised by xtb. The HL values are different from the literature because the optimized structures are not planar.
