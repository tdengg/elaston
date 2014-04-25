import destort
import spacegroup
import vaspIO
import numpy as np
import os

o_poscar = vaspIO.POS('POSCAR')
poscar = o_poscar.read_pos()                 # Generate sgroup.out from POSCAR file                    ###MOD


###### Structure ####################
bv = [poscar["vlatt_1"],poscar["vlatt_2"],poscar["vlatt_3"]]
M_old= np.array(bv)
D    = np.linalg.det(M_old)
V0   = abs(poscar['scale']**3*D)
#####################################

sg = spacegroup.Sgroup(poscar)                      #spacegroup instance
dist = destort.Destort()                            #distort instance


dist.sgn = sg.sgn                                   #get and set spacegroup number

dist.set_strainList()                               # set strain list according to space group number


etaMax = 0.05                                       #maximal lagrangian strain
NoP = 11                                            #number of destortion points
### first strain type
strainType = next(dist.strainList_iter)
dst=1
os.mkdir(os.getcwd()+'/Dst01')
for eta in np.linspace(-etaMax,etaMax, NoP):
    dist.eta = eta
    dist.set_strainType(strainType)
    dist.set_defMatrix()
    def_mat = dist.get_defMatrix()
    M_new = np.dot(M_old, def_mat)
    
    
    pname = os.getcwd()+"/Dst01/Dst01_%.2d/"%dst
    for j in range(3):           
        poscar["vlatt_%s"%(j+1)] = [M_new[j,0],M_new[j,1],M_new[j,2]]
    os.mkdir(pname)
    o_poscar.write_pos(poscar, pname+'POSCAR')
    
    dst+=1
### second strain type
strainType = next(dist.strainList_iter)
for eta in np.linspace(-etaMax,etaMax, NoP):
    strainType = next(dist.strainList_iter)
    dist.set_strainType(strainType)
    dist.set_defMatrix()
    def_mat = dist.get_defMatrix()
    M_new = np.dot(M_old, def_mat)
    
### third strain type
strainType = next(dist.strainList_iter)
for eta in np.linspace(-etaMax,etaMax, NoP):
    strainType = next(dist.strainList_iter)
    dist.set_strainType(strainType)
    dist.set_defMatrix()
    def_mat = dist.get_defMatrix()
    M_new = np.dot(M_old, def_mat)

