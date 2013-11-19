from ase import *
from math import *
 
a = 9.07

atoms = Atoms([Atom('Ti', (0,       0,    0)),
               Atom('Ti', (0.25,       0.25,    0.25)),
               Atom('Si', (1/3., 0, 0)),
               Atom('Si', (-1/3., 0, 0)),
               Atom('Si', (0.25+1/3., 0.25, 0.25)),
               Atom('Si', (0.25-1/3., 0.25, 0.25))])
 
cell = [(0,             a*0.5, a*0.85),
        (a*0.8275, 0, a*0.85),
        (a*0.8275,             a*0.5, 0)]
atoms.set_cell(cell, scale_atoms=True)
 
from ase.visualize import view
view(atoms)
