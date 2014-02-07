import matplotlib.pyplot as plt
import lxml.etree as et
import numpy as np
import json
import sys
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA


class PointBrowser:
    """
    Click on a point to select and highlight it -- the data that
    generated the point will be shown in the lower axes.  Use the 'n'
    and 'p' keys to browse through the next and previous points
    """
    def __init__(self):
        self.lastind = 0

        self.text = ax.text(0.05, 0.95, 'none',
                            transform=ax.transAxes, va='top')
        self.selected,  = ax.plot([X1dst1[0]], [Ydst1[0]], 'o', ms=12, alpha=0.4,
                                  color='yellow', visible=False)

    def onpick(self, event):

        if event.artist!=line: return True

        N = len(event.ind)
        if not N: return True

        # the click locations
        x = event.mouseevent.xdata
        y = event.mouseevent.ydata


        distances = np.hypot(x-X1dst1[event.ind], y-Ydst1[event.ind])
        indmin = distances.argmin()
        dataind = event.ind[indmin]

        self.lastind = dataind
        self.update()

    def update(self):
        if self.lastind is None: return

        dataind = self.lastind

        self.selected.set_visible(True)
        self.selected.set_data(X1dst1[dataind], Ydst1[dataind])
        if X2dst1[dataind] < 10:
            self.text.set_text('selected: Dst%s_0%i'%(dstn, X2dst1[dataind]))
        else:
            self.text.set_text('selected: Dst%s_%i'%(dstn, X2dst1[dataind]))
        fig.canvas.draw()

if __name__ == '__main__':    
    if sys.argv[1] == 'EvS':
        try:
            order = int(sys.argv[2])
        except:
            order = 4
        X1 = []
        X2 = []
        Y1 = []
        
        fig, ax = plt.subplots(1,1)
        tree = et.parse('Energy.xml')
        for n in range(len(tree.xpath("/Energy_Strain/*"))):
            if n+1 < 10:
                dstn = '0'+str(n+1)
            else:
                dstn = str(n+1)
            X1dst1 = (map(float, tree.xpath("//Dst%s/*/@strain"%dstn)))
            X2dst1 = (map(float, tree.xpath("//Dst%s/*/@number"%dstn)))
            Ydst1  = (map(float, tree.xpath("//Dst%s/*/@energy"%dstn)))
            X1.append(X1dst1)
            X2.append(X2dst1)
            Y1.append(Ydst1)
            """  Polynomial fitting:  """
            coeff = np.polyfit(X1dst1, Ydst1 , 6)
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
                if delta > 2*rms: ax.plot(X1dst1[i],Ydst1[i], 'ro', markersize = 10)
                i+=1
            line, = ax.plot(X1dst1,Ydst1, 'k+', picker=5) 
            ax.plot(xp, poly(xp), label='Dst'+ dstn + ':   RMS = %.3E'%rms)

        ax.set_xlabel('Strain')
        ax.set_ylabel('Energy   in Ry')
 
        plt.legend()
        plt.draw()
        
        browser = PointBrowser()

        fig.canvas.mpl_connect('pick_event', browser.onpick)
        
        plt.show()
        
    else:
        f = 'Elastic_SM.xml'
        tree = et.parse(f)
        X = []
        C11 = []
        C12 = []
        C13 = []
        C44 = []
        for n in range(31):
            try:
                
                C11.append(float(json.loads(tree.xpath("//*[@n='%s'and @ngridk and @swidth='0.01']/@SM"%n)[0])[0])) #//*[@n='%s'and @swidth='0.01']/@SM
                C12.append(float(json.loads(tree.xpath("//*[@n='%s'and @ngridk and @swidth='0.01']/@SM"%n)[0])[1]))
                C13.append(float(json.loads(tree.xpath("//*[@n='%s'and @ngridk and @swidth='0.01']/@SM"%n)[0])[2]))
                C44.append(float(json.loads(tree.xpath("//*[@n='%s'and @ngridk and @swidth='0.01']/@SM"%n)[0])[21]))
                X.append(tree.xpath("//*[@n='%s']/@ngridk"%n)[0])
            except:
                continue
            
        
        plt.plot(X,C11,label= r'$C_{11}$')
        plt.plot(X,C11,'k.')
        plt.plot(X,C12,label= r'$C_{12}$')
        plt.plot(X,C12,'k.')
        plt.plot(X,C44,label= r'$C_{44}$')
        plt.plot(X,C44,'k.')
        
        plt.legend()
        plt.xlabel('Number of k-points')
        plt.ylabel('Elements of stiffness matrix     in GPa')
        #plt.title('Convergence at rgkmax = 0.01')
        plt.show()