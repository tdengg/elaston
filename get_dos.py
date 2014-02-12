import sys
sys.path.pop(1)
import phonopy.interface.vasp as vasp
import phonopy.harmonic.dynamical_matrix as dynmat
import lxml.etree as etree
import phonopy.structure.cells as cells
import phonopy.phonon.mesh as mesh
import phonopy.phonon.dos as dos
import phonopy.phonon.thermal_properties as tm
import numpy as np

print dynmat.__file__
###read force constants from vasprun.xml###
vasprun = etree.iterparse('vasprun.xml', tag='varray')
fc = vasp.get_force_constants_vasprun_xml(vasprun)
###########################################

########### read positionsl ###############
primitive = vasp.get_atoms_from_poscar(open('POSCAR-p'),'W')
superc =  vasp.get_atoms_from_poscar(open('POSCAR'),'W')
###########################################
Fr = np.dot(np.linalg.inv(primitive.get_cell()),superc.get_cell())
#print Fr

primc = cells.Primitive(vasp.get_atoms_from_poscar(open('POSCAR'),'W'),Fr)#primitive.get_cell())
#print primc
#print "fc", fc[0]
dyninst = dynmat.DynamicalMatrix(superc,primc,fc[0])#,frequency_scale_factor=15.633302)

dyninst.set_dynamical_matrix([10.,10.,15.])
print dyninst.get_dynamical_matrix()

#supercm = superc.get_cell()
M = mesh.Mesh(dyninst, [10,10,10])#, factor = 15.633302)
DOS = dos.TotalDos(M)
DOS.run()
#thermal = tm.ThermalProperties(DOS.get_dos()[0])
#thermal.set_thermal_properties()
#print thermal.get_thermal_properties()
#print DOS.get_dos()
plt = DOS.plot_dos()
plt.show()