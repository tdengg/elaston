import os
import json
import collections
import numpy as np
import lxml.etree as et
import matplotlib.pyplot as plt
conv = 96.47244
E0tot = []#[-1604.95572510,-1609.44981834,-1612.92140288,-1615.34754644,-1616.82353934,-1617.36916656,-1617.03017334,-1615.83420462,-1613.84110815,-1611.09259060,-1607.5992790]

f = []
l = []
dic = {}
dict =  {}
for d in os.listdir('./'):
    
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


j = 0
for out in dic:
    
    T = []
    F = []
    for i in dic[out]['file']:
        T.append(float(i.split()[0]))
        F.append(float(i.split()[1]))
        
    dic[out]['F'] = F
    dic[out]['T'] = T
    #plt.plot(T,F)
    
    j+=1

trange = T

ndic = collections.OrderedDict(sorted(dic.items()))    #sort dictionary
minF = []
minl = []
for temp in trange:
    xdata = []
    ydata = []
    i=0
    for out in ndic:
        xdata.append(out)
        ind = dic[out]['T'].index(temp)
        
        ydata.append(dic[out]['F'][ind]/conv + dic[out]['E0'] + 13.5)
        i+=1
    #plt.plot(xdata,ydata)
    #polyfit:
    coeff = np.polyfit(xdata,ydata,3)
    p = np.poly1d(coeff)
    
    polyx = np.linspace(min(xdata),max(xdata),1000)
    
    minl.append(np.roots(p.deriv())[1])
    minF.append(p(np.roots(p.deriv())[1]))
dict['F_min'] = minF
dict['l_min'] = minl
dict['T'] = T
plt.plot(minl,T)
with open('out_Vmin-T.json','w') as f2:
    json.dump(dict, f2)
plt.show()