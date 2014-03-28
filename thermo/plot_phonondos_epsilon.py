import matplotlib.pyplot as plt
import os
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, zoomed_inset_axes


#### indicate maxima #####
color = ['r','g','b']
max10=[4.02,5.4]
max11=[4.7,6.15]
max12=[4.05,5.4]

max20=[4.8,6.4]
max21=[4.75,6.1]
max22=[4.4,8.45]

max30=[4.3,5.1]
max31=[4.8,6.2]
max32=[5.4,7.05]

label=[r'$\epsilon =\, -0.05$',r"$\epsilon = \, \; 0.00$",r'$\epsilon = +0.05$']
################# Dst02 ############################
ax0 = plt.subplot(311)
axins = inset_axes(ax0,
                   width="20%", # width = 30% of parent_bbox
                   height="70%", # height : 1 inch
                   loc=2)
axins.set_xlim(xmin=-0.06,xmax=0.06)
axins.set_xticks([-0.05,0.,0.05])
axins.set_xlabel(r'$\epsilon$')
axins.set_yticks([-12,-8,-4,0,4])
axins.set_ylabel(r'$F_{vib}$  in eV')

axins.yaxis.tick_right()
axins.yaxis.set_label_position("right")
#axins.axis["left"].major_ticklabels.set_visible(False)
#axins.axis["right"].yticks(0)
#axins.axis["right"].major_ticklabels.set_visible(True)
#axins.axis["right"].major_ticklabels.set_visible(True)
os.chdir('/home/MCL/t.dengg/results/W/Cij_T_F/Cij_T/scale_3.17226/Dst02')
n=0
j=0
for d in sorted(os.listdir('./')):
    
    if os.path.isdir(d) and 'Dst' in d and j in [0,5,10,11,16,21]: n+=1
    j+=1
hatch=["///","||",'/']
j=0
k=0
F0=[]
F1=[]
for d in sorted(os.listdir('./')):
    
    if os.path.isdir(d) and 'Dst' in d and j in [0,10,20]:
        os.chdir(d)
        
        f = open('total_dos.dat','r')
        dos = f.readlines()
        f.close()
        
        f = []
        di = []
        i=0
        for line in dos:
            if i == 0: 
                i+=1
                continue
            
            di.append(float(line.split()[1]))
            f.append(float(line.split()[0]))
            i+=1
        ax0.fill(f,di, label = label[k], lw=2.,alpha=0.5, hatch=hatch[k])#, color=(1,0,float(k)/float(n)))
        ax0.set_xlim(xmin=0)
        ax0.set_ylim(ymax=2.0)
        ax0.set_title('tetragonal deformation')
        ax0.set_ylabel(r'phonon DOS  in $THz^{-1}$')
        #plt.vlines(f[di.index(max(di))], 0, 1.7)
        
        Fdata = open('F_TV').readlines()
        F0.append(float(Fdata[0].split()[1]))
        F1.append(float(Fdata[50].split()[1]))
        
        os.chdir('..')
        j+=1
        k+=1
    else:
        j+=1
        continue

axins.plot([-0.05,0,0.05],F0,lw=2.,label='T =  10K')
axins.plot([-0.05,0,0.05],F1,lw=2.,label='T = 500K')
axins.set_ylim(ymin=-12,ymax=4)
axins.legend(loc=7,prop={'size':18})
################# Dst03 ############################

ax1 = plt.subplot(312)
axins1 = inset_axes(ax1,
                   width="20%", # width = 30% of parent_bbox
                   height="70%", # height : 1 inch
                   loc=2)
axins1.set_xlim(xmin=-0.06,xmax=0.06)
axins1.set_xticks([-0.05,0.,0.05])
axins1.set_xlabel(r'$\epsilon$')
axins1.set_yticks([-12,-8,-4,0,4])
axins1.set_ylabel(r'$F_{vib}$  in eV')

axins1.yaxis.tick_right()
axins1.yaxis.set_label_position("right")
#axins1.axis["left"].major_ticklabels.set_visible(False)
os.chdir('/home/MCL/t.dengg/results/W/Cij_T_F/Cij_T/scale_3.17226/Dst03')
n=0
j=0
F0=[]
F1=[]
for d in sorted(os.listdir('./')):
    
    if os.path.isdir(d) and 'Dst' in d and j in [0,5,10,11,16,21]: n+=1
    j+=1
hatch=["///","||",'/']
j=0
k=0
for d in sorted(os.listdir('./')):
    
    if os.path.isdir(d) and 'Dst' in d and j in [0,10,20]:
        os.chdir(d)
        
        f = open('total_dos.dat','r')
        dos = f.readlines()
        f.close()
        
        f = []
        di = []
        i=0
        for line in dos:
            if i == 0: 
                i+=1
                continue
            
            di.append(float(line.split()[1]))
            f.append(float(line.split()[0]))
            i+=1
        ax1.fill(f,di, label = d, lw=2.,alpha=0.5, hatch=hatch[k])#, color=(1,0,float(k)/float(n)))
        ax1.set_xlim(xmin=0)
        ax1.set_ylim(ymax=2.0)
        ax1.set_title('shear deformation')
        ax1.set_ylabel(r'phonon DOS  in $THz^{-1}$')
        
        Fdata = open('F_TV').readlines()
        F0.append(float(Fdata[0].split()[1]))
        F1.append(float(Fdata[50].split()[1]))
        #plt.vlines(f[di.index(max(di))], 0, 1.7)
        os.chdir('..')
        j+=1
        k+=1
    else:
        j+=1
        continue
    

axins1.plot([-0.05,0,0.05],F0,lw=2.)
axins1.plot([-0.05,0,0.05],F1,lw=2.)
axins1.set_ylim(ymin=-12,ymax=4)
################# Dst03 ############################
ax2 = plt.subplot(313)
axins2 = inset_axes(ax2,
                   width="20%", # width = 30% of parent_bbox
                   height="70%", # height : 1 inch
                   loc=2)
axins2.set_xlim(xmin=-0.06,xmax=0.06)
axins2.set_xticks([-0.05,0.,0.05])
axins2.set_xlabel(r'$\epsilon$')
axins2.set_yticks([-12,-8,-4,0,4])
axins2.set_ylabel(r'$F_{vib}$  in eV')

axins2.yaxis.tick_right()
axins2.yaxis.set_label_position("right")
#axins2.axis["left"].major_ticklabels.set_visible(False)
os.chdir('/home/MCL/t.dengg/results/W/Cij_T_exp/T_expansion')

n=0
j=0
F0=[]
F1=[]
for d in sorted(os.listdir('./')):
    
    if os.path.isdir(d) and 'scale' in d and n in [0,1,2,3,4,5,6,7,8,9]: 
        n+=1
        j+=1
    else:
        j+=1
    
        continue

hatch=["///","||",'/']
j=0
k=0
for d in sorted(os.listdir('./')):
    print k
    if os.path.isdir(d) and 'scale' in d and j in [0,4,8]:
        os.chdir(d)
        
        f = open('total_dos.dat','r')
        dos = f.readlines()
        f.close()
        
        f = []
        di = []
        i=0
        for line in dos:
            if i == 0: 
                i+=1
                continue
            
            di.append(float(line.split()[1]))
            f.append(float(line.split()[0]))
            i+=1
        ax2.fill(f,di, label = label[k], lw=2.,alpha=0.5,hatch=hatch[k])#, color=(1,0,float(k)/float(n)))
        ax2.set_xlim(xmin=0)
        ax2.set_ylim(ymax=2.0)
        ax2.set_title('volume deformation')
        ax2.set_xlabel(r'frequency  in $THz$')
        ax2.set_ylabel(r'phonon DOS  in $THz^{-1}$')
        
        Fdata = open('F_TV').readlines()
        F0.append(float(Fdata[0].split()[1]))
        F1.append(float(Fdata[50].split()[1]))
        
        os.chdir('..')
        j+=1
        k+=1
    elif os.path.isdir(d) and 'scale' in d:
        j+=1
        continue

axins2.plot([-0.05,0,0.05],F0,lw=2.)
axins2.plot([-0.05,0,0.05],F1,lw=2.) 
axins2.set_ylim(ymin=-12,ymax=4)
ax0.legend(prop={'size':20})
#ax1.legend()
#ax2.legend()
#plt.show()

plt.savefig("/home/MCL/t.dengg/results/DOS1.png",transparent = True)
