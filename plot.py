import matplotlib.pyplot as plt
import lxml.etree as et
import numpy as np
import json
import sys
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA

if sys.argv[1] == 'EvS':
    
    ax = host_subplot(111, axes_class=AA.Axes)
    tree = et.parse('Energy.xml')
    for n in range(len(tree.xpath("/Energy_Strain/*"))):
        if n+1 < 10:
            dstn = '0'+str(n+1)
        else:
            dstn = str(n+1)
        X1dst1 = map(float, tree.xpath("//Dst%s/*/@strain"%dstn))
        X2dst1 = map(float, tree.xpath("//Dst%s/*/@number"%dstn))
        Ydst1 = map(float, tree.xpath("//Dst%s/*/@energy"%dstn))
        
        """  Polynomial fitting:  """
        coeff = np.polyfit(X1dst1, Ydst1 , 4)
        poly = np.poly1d(coeff)
        xp = np.linspace(min(X1dst1), max(X1dst1), 100)
        """  Calculate RMS:  """
        deltasq = 0
        deltas = []
        for i in range(len(X1dst1)):
            delta = Ydst1[i] - poly(X1dst1[i])
            deltas.append(delta)
            deltasq += (delta)**2.0
            
        rms = np.sqrt(deltasq/len(X1dst1))
        i=0
        for delta in deltas: 
            if delta > 2*rms: ax.plot(X1dst1[i],Ydst1[i], 'ro')
            i+=1
        ax.plot(X1dst1,Ydst1, 'k+')
        ax.plot(xp, poly(xp), label='Dst'+ dstn + ':   RMS = %.3E'%rms)
        
    ax2 = ax.twin()
    ax.set_xlabel('Strain')
    ax.set_ylabel('Energy   in Ry')
    ax2.set_xticks(X1dst1)
    ax2.set_xticklabels(map(str, X2dst1))
    ax2.set_xlabel('Distortion number')
    ax2.axis["right"].major_ticklabels.set_visible(False)
        
    plt.legend()
    plt.draw()
    plt.show()
else:
    f = 'Elastic_SM.xml'
    tree = et.parse(f)
    X = []
    C11 = []
    C12 = []
    C13 = []
    C44 = []
    for n in range(27):
        try:
            C11.append(float(json.loads(tree.xpath("//*[@n='%s'and @swidth='0.01']/@SM"%n)[0])[0]))
            C12.append(float(json.loads(tree.xpath("//*[@n='%s'and @swidth='0.01']/@SM"%n)[0])[1]))
            C13.append(float(json.loads(tree.xpath("//*[@n='%s'and @swidth='0.01']/@SM"%n)[0])[2]))
            C44.append(float(json.loads(tree.xpath("//*[@n='%s'and @swidth='0.01']/@SM"%n)[0])[21]))
            X.append(tree.xpath("//*[@n='%s'and @swidth='0.01']/@ngridk"%n)[0])
        except:
            continue
        
    
    plt.plot(X,C11,label= r'$C_{11}$')
    plt.plot(X,C12,label= r'$C_{12}$')
    plt.plot(X,C44,label= r'$C_{44}$')
    
    plt.legend()
    plt.xlabel('Number of k-points')
    plt.ylabel('Elements of stiffness matrix     in GPa')
    #plt.title('Convergence at rgkmax = 0.01')
    plt.show()