import sys
sys.path.pop(1)
import plot_thermal
import os
import matplotlib.pyplot as plt
import numpy as np

trange = np.linspace(0,1000,101)

E0tot =[-1603.31046092,-1609.65924216,-1614.30440208,-1617.35670433,-1618.90558513,-1619.03524097,-1617.85298827,-1615.42182936,-1611.82607060,-1607.13759994]
E0 = [x/125. for x in E0tot]
inst = plot_thermal.PLOT_THERMAL('/home/MCL/t.dengg/calc/phonons_vasp/DFPT/W/conv_cell/s5x5x5')
dict = inst.get_data()
inst.lname = r'$W$'
inst.free_ene(dict, trange,E0)


#E0tot =[-1603.31340590,-1609.66758602,-1614.31900855,-1617.38171960,-1618.94457141,-1619.08846239,-1617.91749977,-1615.49316604,-1611.90002937,-1607.21116509]
#E0 = [x/125. for x in E0tot]
#inst = plot_thermal.PLOT_THERMAL('/home/MCL/t.dengg/calc/phonons_vasp/DFPT/W/conv_cell/s5x5x5')
#dict = inst.get_data()
#inst.lname = r'$W Fr$'
#inst.free_ene(dict, trange,E0)


E0tot = [-1604.95572510,-1609.44981834,-1612.92140288,-1615.34754644,-1616.82353934,-1617.36916656,-1617.03017334,-1615.83420462,-1613.84110815,-1611.09259060,-1607.5992790]
E0 = [x/125. for x in E0tot]
inst = plot_thermal.PLOT_THERMAL('/home/MCL/t.dengg/calc/WRe/0.12/s5x5x5/Cij_T')
dict = inst.get_data()
inst.lname = r'$W_{0.88}$ $Re_{0.12}$'
inst.free_ene(dict, trange,E0)


E0tot = [-1602.09882400,
-1605.91860775,
-1608.71031429,
-1610.46502401,
-1611.24690424,
-1611.11827955,
-1610.11617181,
-1608.27261845,
-1605.63817391,
-1602.26999234,
-1598.18194813]
E0 = [x/125. for x in E0tot]
inst = plot_thermal.PLOT_THERMAL('/home/MCL/t.dengg/calc/WRe/0.25/s5x5x5/Cij_T')
dict = inst.get_data()
inst.lname = r'$W_{0.75}$ $Re_{0.25}$'
inst.free_ene(dict, trange,E0)


expT = [5,25,50,100,200,293,400,500,600,700,800,900,1000]
expalpha = [0.0006,0.21,0.88,2.6,4.1,4.5,4.5,4.6,4.7,4.8,5.0,5.0,5.2]
plt.plot(expT,expalpha,'bx',ms=10., label = r'$W$ $exp.$')
plt.legend(loc=4,prop={'size':18})
plt.xlabel('T in $K$')
plt.ylabel(r'$\alpha$ in $10^6 K^{-1}$ ')
#plt.title('Linear Thermal Expansion Coefficients of W and WRe alloys (VCA).')
plt.savefig('/home/MCL/t.dengg/results/alpha.png',transparent=True)
#plt.show()