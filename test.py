import sys
sys.path.pop(1)
from phonopy import Phonopy
from phonopy.structure.atoms import Atoms as PhonopyAtoms
import numpy as np
import lxml.etree as etree
from phonopy.interface import vasp

###read force constants from vasprun.xml###
vasprun = etree.iterparse('vasprun.xml', tag='varray')
fc = vasp.get_force_constants_vasprun_xml(vasprun)
###########################################

########### read positionsl ###############
primitive = vasp.get_atoms_from_poscar(open('POSCAR-p'),'W')
superc =  vasp.get_atoms_from_poscar(open('POSCAR'),'W')
###########################################
numbatom =  superc.get_number_of_atoms()
print fc
#print superc.get_scaled_positions()
a = primitive.get_cell()[0][0]*2
bulk = PhonopyAtoms(symbols=['Si'] * numbatom,
                    scaled_positions= superc.get_scaled_positions())
bulk.set_cell(np.diag((a, a, a)))
phonon = Phonopy(bulk,
                 [[1,0,0],[0,1,0],[0,0,1]],
                 primitive_matrix=[[-0.5, 0.5, 0.5],
                                   [0.5, -0.5, 0.5],
                                   [0.5, 0.5, -0.5]],
                 distance=0.01)

phonon.set_force_constants(fc[0])
phonon.set_dynamical_matrix()
print phonon.get_dynamical_matrix_at_q([0,0,0])
mesh = [20, 20, 20]
phonon.set_mesh(mesh)
qpoints, weights, frequencies, eigvecs = phonon.get_mesh()
phonon.set_total_DOS()
phonon.plot_total_DOS().show()