import sys
sys.path.pop(1)
import plot_thermal
import os
import matplotlib.pyplot as plt
import numpy as np
import lxml.etree as et
dir0 = os.getcwd()
trange = np.linspace(0,1000,101)
def get_E0(dir):
    l = []
    dic = {}
    dict =  {}
    for d in os.listdir(dir):
        print d
        if 'scale_' in d:
            os.chdir(d)
            l = float(d.lstrip('scale_'))
            dic[l] = {}
            dic[l]['file'] = open('F_TV').readlines()
            
            
            vaspout = et.parse('vasprun.xml')
            elem = vaspout.xpath("//scstep/energy/i[@name = 'e_fr_energy']")
            allengys = []
            for k in elem:
                try:
                    allengys.append(float(k.text))
                except:
                    allengys.append(0.)
                        
            trueengys = []
            for engy in allengys:
                if engy < -1000. and engy > -3000.: trueengys.append(engy)
            gsenergy = trueengys[-1]
            
            dic[l]['E0']=gsenergy/125.
            os.chdir('..')
        else:
            continue
    return dic
#E0tot =[-1603.31046092,-1609.65924216,-1614.30440208,-1617.35670433,-1618.90558513,-1619.03524097,-1617.85298827,-1615.42182936,-1611.82607060,-1607.13759994]
#E0 = [x/125. for x in E0tot]
dir = '/home/MCL/t.dengg/results/W/Cij_T_exp/T_expansion_PBEsol'
os.chdir(dir)
E0=[]
dic = get_E0(dir)
for latt in sorted(dic):
    E0.append(dic[latt]['E0'])
os.chdir(dir0)
inst = plot_thermal.PLOT_THERMAL(dir)
dict = inst.get_data()
inst.lname = r'$W$ PBEsol'
inst.free_ene(dict, trange,E0)


#E0tot =[-1603.31340590,-1609.66758602,-1614.31900855,-1617.38171960,-1618.94457141,-1619.08846239,-1617.91749977,-1615.49316604,-1611.90002937,-1607.21116509]
#E0 = [x/125. for x in E0tot]
#inst = plot_thermal.PLOT_THERMAL('/home/MCL/t.dengg/calc/phonons_vasp/DFPT/W/conv_cell/s5x5x5')
#dict = inst.get_data()
#inst.lname = r'$W Fr$'
#inst.free_ene(dict, trange,E0)


#E0tot = [-1604.95572510,-1609.44981834,-1612.92140288,-1615.34754644,-1616.82353934,-1617.36916656,-1617.03017334,-1615.83420462,-1613.84110815,-1611.09259060,-1607.5992790]
#E0 = [x/125. for x in E0tot]

################ PBE-SOL #########################################################
dir = '/home/MCL/t.dengg/results/WRe/0.12/Cij_T_exp/T_expansion_PBEsol'
os.chdir(dir)
E0=[]
dic = get_E0(dir)
for latt in sorted(dic):
    E0.append(dic[latt]['E0'])
os.chdir(dir0)
inst = plot_thermal.PLOT_THERMAL(dir)
dict = inst.get_data()
inst.lname = r'$W_{0.88}$ $Re_{0.12}$ PBEsol'
inst.free_ene(dict, trange,E0)


#E0tot = [-1602.09882400,
#-1605.91860775,
#-1608.71031429,
#-1610.46502401,
#-1611.24690424,
#-1611.11827955,
#-1610.11617181,
#-1608.27261845,
#-1605.63817391,
#-1602.26999234,
#-1598.18194813]
#E0 = [x/125. for x in E0tot]

dir = '/home/MCL/t.dengg/results/WRe/0.25/Cij_T_exp/T_expansion_PBEsol'
os.chdir(dir)
E0=[]
dic = get_E0(dir)
for latt in sorted(dic):
    E0.append(dic[latt]['E0'])
os.chdir(dir0)
inst = plot_thermal.PLOT_THERMAL(dir)
dict = inst.get_data()
inst.lname = r'$W_{0.75}$ $Re_{0.25}$ PBEsol'
inst.free_ene(dict, trange,E0)

######################### PBE #############################################
dir = '/home/MCL/t.dengg/results/W/Cij_T_exp/T_expansion'
os.chdir(dir)
E0=[]
dic = get_E0(dir)
for latt in sorted(dic):
    E0.append(dic[latt]['E0'])
os.chdir(dir0)
inst = plot_thermal.PLOT_THERMAL(dir, style='--')
dict = inst.get_data()
inst.lname = r'$W$'
inst.free_ene(dict, trange,E0)

dir = '/home/MCL/t.dengg/results/WRe/0.25/Cij_T_exp/T_expansion'
os.chdir(dir)
E0=[]
dic = get_E0(dir)
for latt in sorted(dic):
    E0.append(dic[latt]['E0'])
os.chdir(dir0)
inst = plot_thermal.PLOT_THERMAL(dir, style='--')
dict = inst.get_data()
inst.lname = r'$W_{0.75}$ $Re_{0.25}$'
inst.free_ene(dict, trange,E0)

####################### EXPERIMENTAL #####################################

expT = [5,25,50,100,200,293,400,500,600,700,800,900,1000]
expalpha = [0.0006,0.21,0.88,2.6,4.1,4.5,4.5,4.6,4.7,4.8,5.0,5.0,5.2]
plt.plot(expT,expalpha,'b<',ms=10., label = r'$W$ $exp.$')
x = np.linspace(300,1000,2)

y1 = 3.114*10**(-4.) * (x+273.) + 4.3315
plt.plot(x,y1,'b-.', lw = 1.5, label=r'$\alpha (W) = 3.114 * 10^{-4} * (T+273) + 4.3315$')
print y1

y = 3.531*10**(-4.) * (x+273.) + 5.0405
print y
plt.plot(x,y,'r-.', lw = 1.5, label=r'$\alpha (WRe_{0.26}) = 3.531 * 10^{-4} * (T+273) + 5.0405$)')

expT=[373,
473,
573,
673,
773,
873,
973,
1073,
1173,
1273,
1373,
1473]
expalpha=[4.45,
4.35,
4.30,
4.30,
4.30,
4.50,
4.56,
4.62,
4.68,
4.73,
4.81,
4.84]
plt.plot(expT,expalpha,'g1',ms=10., label = r'$W_{0.95}Re_{0.05}$ $exp.$')


expT = [100,
200,
300,
400,
500,
600,
700,
800,
900,
1000,
1100,
1200,
1300
]
expT = [T+273.15 for T in expT]
expalpha = [5.20,
5.00,
5.05,
5.05,
5.12,
5.13,
5.25,
5.39,
5.51,
5.62,
5.72,
5.81,
5.89
]
plt.plot(expT,expalpha,'r2',ms=10., label = r'$W_{0.75}Re_{0.25}$ $exp.$')


plt.legend(loc=4,prop={'size':16})
plt.xlabel('T in $K$')
plt.ylabel(r'$\alpha$ in $10^6 K^{-1}$ ')
#plt.title('Linear Thermal Expansion Coefficients of W and WRe alloys (VCA).')
#plt.savefig('/home/MCL/t.dengg/results/alpha.png',transparent=True)
plt.show()