import sys
sys.path.pop(1)

import phonopy.interface.vasp as vasp
import numpy as np
import lxml.etree as etree
from phonopy import Phonopy
from phonopy.structure.atoms import Atoms as PhonopyAtoms


vasprun = etree.iterparse('vasprun.xml', tag='varray')
fc = vasp.get_force_constants_vasprun_xml(vasprun)

primitive = vasp.get_atoms_from_poscar(open('POSCAR-p'),'W')
superc =  vasp.get_atoms_from_poscar(open('POSCAR'),'W')

print superc.get_scaled_positions()

a = 5.404
bulk = PhonopyAtoms(symbols=['W'] * 216,
                    positions=superc.get_scaled_positions())
bulk.set_cell(np.diag((a, a, a)))
phonon = Phonopy(bulk,[[1,0,0],[0,1,0],[0,0,1]],primitive_matrix=[[-0.5, 0.5, 0.5],[0.5, -0.5, 0.5],[0.5, 0.5, -0.5]])

phonon.set_force_constants(fc)

mesh = [3, 3, 3]
phonon.set_mesh(mesh)
qpoints, weights, frequencies, eigvecs = phonon.get_mesh()


phonon.set_total_DOS()
phonon.plot_total_DOS().show()