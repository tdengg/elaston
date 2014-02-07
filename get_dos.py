import phonopy.interface.vasp as vasp
import phonopy.harmonic.dynamical_matrix as dynmat
import lxml.etree as etree
import phonopy.structure.cells as cells
import phonopy.phonon.mesh as mesh
import phonopy.phonon.dos as dos

vasprun = etree.iterparse('vasprun.xml', tag='varray')
fc = vasp.get_force_constants_vasprun_xml(vasprun)
primitive = vasp.get_atoms_from_poscar(open('POSCAR-p'),'W')
superc =  vasp.get_atoms_from_poscar(open('POSCAR'),'W')
primc = cells.Primitive(vasp.get_atoms_from_poscar(open('POSCAR'),'W'),primitive.get_cell())
dyninst = dynmat.DynamicalMatrix(superc,primc,fc[0])
#dyninst.set_dynamical_matrix([0,0,0])
#dynamical_matrix = dyninst.get_dynamical_matrix()
supercm = superc.get_cell()
M = mesh.Mesh(dyninst, superc, [3,3,3])
dos.TotalDos(M)