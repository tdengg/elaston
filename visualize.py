from ase import *
from math import *
 
a = 9.07

atoms = Atoms([Atom('Ti', (0,       0,    0)),
               Atom('Si', (0.3333,       0.3333,    -0.3333))])
 
cell = [(0,             a*0.5, a*0.85),
        (a*0.8275, 0, a*0.85),
        (a*0.8275,             a*0.5, 0)]
atoms.set_cell(cell, scale_atoms=True)
 
from ase.visualize import view
view(atoms)
