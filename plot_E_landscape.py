import lxml.etree as et
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import os
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
E = []
E1 = []
V = []
V1 = []
strain = []
strain1 = []
dirlist = os.listdir('.')
for dir in dirlist:
    if os.path.isdir(dir) and 'scale' in dir:
        os.chdir(dir)
        
        #os.system('~/git/elaston/ElaStic_v1.0/ElaStic_Analyze.py')
        element = et.parse('Energy.xml')
        dst = element.xpath('//Dst02/*')
        dst1 = element.xpath('//Dst03/*')
        for d in dst:
            V.append(float(d.xpath('./@volume')[0]))
            E.append(float(d.xpath('./@energy')[0]))
            strain.append(float(d.xpath('./@strain')[0]))
            
        for d in dst1:
            
            V1.append(float(d.xpath('./@volume')[0]))
            E1.append(float(d.xpath('./@energy')[0]))
            strain1.append(float(d.xpath('./@strain')[0]))
        os.chdir('..')
grid_x, grid_y = np.meshgrid(np.linspace(min(V),max(V),100), np.linspace(-0.05,0.05,100))

grid = griddata(np.transpose([V,strain]),np.array(E),(grid_x, grid_y),method='cubic')  

ax.scatter(V,strain,E)
#ax.plot_surface(grid_x,grid_y, grid, cmap=plt.get_cmap('jet'))
ax.contour(grid_x,grid_y, grid, 30,stride=2)

#plt.plot(V,strain)

#grid1_x, grid1_y = np.meshgrid(np.linspace(min(V1),max(V1),100), np.linspace(-0.05,0.05,100))

#grid1 = griddata(np.transpose([V1,strain1]),np.array(E1),(grid1_x, grid1_y),method='linear')  

#ax.scatter(V1,strain1,E1)
#ax.plot_surface(grid_x,grid_y, grid, cmap=plt.get_cmap('jet'))
#ax.contour(grid1_x,grid1_y, grid1,stride=2)


plt.show()
        