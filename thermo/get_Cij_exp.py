import collections
import json
import matplotlib.pyplot as plt
import numpy as np

T_exp = [0,
20,
40,
60,
80,
100,
120,
140,
160,
180,
200,
220,
240,
260,
280,
300]

C11_exp = [5.3255,
5.3255,
5.3254,
5.3254,
5.3252,
5.3239,
5.3220,
5.3180,
5.3132,
5.3049,
5.2936,
5.2817,
5.2697,
5.2576,
5.2452,
5.2327]
C11_exp = [x*100. for x in C11_exp]

C12_exp = [2.0495,
2.0495,
2.0494,
2.0496,
2.0496,
2.0503,
2.0516,
2.0550,
2.0592,
2.0609,
2.0592,
2.0569,
2.0543,
2.0514,
2.0484,
2.0453]
C12_exp = [x*100. for x in C12_exp]

C44_exp = [1.6313,
1.6313,
1.6313,
1.6312,
1.6312,
1.6310,
1.6298,
1.6273,
1.6238,
1.6207,
1.6178,
1.6153,
1.6130,
1.6108,
1.6089,
1.6072]
C44_exp = [x*100. for x in C44_exp]




with open('Cij_0/FT_out.json') as data_file:    
    Cij_dict = json.load(data_file)

with open('T_expansion/FT_out.json') as data_file:    
    lMin_T_dict = json.load(data_file)
    
Cij_dict_sorted = collections.OrderedDict(sorted(Cij_dict.items()))

lMin_T_dict_sorted = collections.OrderedDict(sorted(lMin_T_dict.items()))
C11 = []
C12 = []
C44 = []
l = []
for key in Cij_dict_sorted.keys(): 
    C11.append( Cij_dict_sorted[key]['SM'][0] )
    C12.append( Cij_dict_sorted[key]['SM'][1] )
    C44.append( Cij_dict_sorted[key]['SM'][-1] )
for key in Cij_dict_sorted.keys(): l.append(float(key))

#### C11(T)
coeff11 = np.polyfit(l,C11,5)
pC11 = np.poly1d(coeff11)
polyCx = np.linspace(min(l),max(l),1000)

#### C12(T)
coeff12 = np.polyfit(l,C12,5)
pC12 = np.poly1d(coeff12)
polyCx = np.linspace(min(l),max(l),1000)

#### C44(T)
coeff44 = np.polyfit(l,C44,5)
pC44 = np.poly1d(coeff44)
polyCx = np.linspace(min(l),max(l),1000)

F_min = lMin_T_dict_sorted['F_min']
l_min = lMin_T_dict_sorted['l_min']
T = lMin_T_dict_sorted['T']


ax1 = plt.subplot(121)
ax1.plot(l, C11,'+')
ax1.plot(polyCx, pC11(polyCx))
ax1.plot(l_min,pC11(l_min),'o')

ax2 = plt.subplot(122)
ax2.plot(T,pC11(l_min),label=r'$C_{11}$ VASP (GGA)')
ax2.plot(T,pC12(l_min),label=r'$C_{12}$ VASP (GGA)')
ax2.plot(T,pC44(l_min),label=r'$C_{44}$ VASP (GGA)')
ax2.plot(T_exp,C11_exp,'o',label=r'$C_{11}$ exp.')
ax2.plot(T_exp,C12_exp,'o',label=r'$C_{12}$ exp.')
ax2.plot(T_exp,C44_exp,'o',label=r'$C_{44}$ exp.')
ax2.set_xlabel(r'T   in K')
ax2.set_ylabel(r'$C_{ij}$    in GPa')
ax2.legend(loc=7)

####################### write json output ############################
plotdict = {'C11(T)':{'x':T, 'y':list(pC11(l_min)), 'label':r'$C_{11}$ VASP (GGA)'},
            'C12(T)':{'x':T, 'y':list(pC12(l_min)), 'label':r'$C_{12}$ VASP (GGA)'},
            'C44(T)':{'x':T, 'y':list(pC44(l_min)), 'label':r'$C_{44}$ VASP (GGA)'},
            'C11_exp':{'x':T_exp, 'y':list(C11_exp), 'label':r'$C_{11}$ exp.'},
            'C12_exp':{'x':T_exp, 'y':list(C12_exp), 'label':r'$C_{12}$ exp.'},
            'C44_exp':{'x':T_exp, 'y':list(C44_exp), 'label':r'$C_{44}$ exp.'},
            'xlabel':'T   in K',
            'ylabel':r'$C_{ij}$    in GPa'
            }

plotout = open('plot.json','w')
plotout.write(json.dumps(plotdict, indent=3))
plotout.close()
######################################################################

plt.show()