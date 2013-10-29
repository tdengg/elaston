import os
import plot3d as p3
import matplotlib.pyplot as plt
"""
Read Elastic
"""
class ReadElastic(object):
    def __init__(self):
        self.SM = {}
        self.C11 = {}
        self.C12 = {}
        self.C44 = {}
        self.YM = {}
        self.filelist = os.listdir(os.curdir)
        
    def readSM(self):
        j=0
        
        for f in self.filelist:
            print f
            if os.path.isdir(f): os.chdir(f)
            else: continue
            
            self.SM[f] = []
            
            k=0
            for line in open("./ElaStic_2nd.out"):
                 
                ############ Read Youngs Modulus ############
                if k == 45 and line.split(' ')[12] != '': self.YM[f]=(float(line.split(' ')[12]))
                elif k == 45 and line.split(' ')[12] == '': self.YM[f]=(float(line.split(' ')[13]))
                #-------------------------------------------#
                
                ########### Read Stiffness Matrix ###########
                if k in [15,16,17,18,19,20]:
                    for i in line.split(' '):
                        if i != '': self.SM[f].append(float(i.rstrip('\n')))
                    
                #############################################        
                
                k+=1
                 
            os.chdir('..')
            j+=1
        
        for di in self.SM.keys():
            self.C11[di] = self.SM[di][0]
        
        for di in self.SM.keys():
            self.C12[di] = self.SM[di][1]
            
        for di in self.SM.keys():
            self.C44[di] = self.SM[di][21]
            
        ########## PLOT ##########
        print self.YM
        #plt.plot([7,11,15,21],[self.YM['o_7'],self.YM['o_11'],self.YM['o_15'],self.YM['o_21']], label = "Youngs Modulus")
        #plt.plot([7,11,15,21],[self.C12['o_7'],self.C12['o_11'],self.C12['o_15'],self.C12['o_21']], label = "C11")
        #plt.plot([7,11,15,21],[self.C11['o_7'],self.C11['o_11'],self.C11['o_15'],self.C11['o_21']], label = "C12")
        #plt.plot([7,11,15,21],[self.C44['o_7'],self.C44['o_11'],self.C44['o_15'],self.C44['o_21']], label = "C44")
        #plt.legend(title='ngridk')
        #plt.title('Number of distorted Structures N')
        #plt.xlabel("N")
        #plt.ylabel("GPa")
        
        #plt.show()
        
        p3.Plot3d([6,10,15,18,21],[0.05,0.01,0.002],self.YM, 'Youngs Modulus').plot()
        p3.Plot3d([6,10,15,18,21],[0.05,0.01,0.002],self.C11, 'C11').plot()
        p3.Plot3d([6,10,15,18,21],[0.05,0.01,0.002],self.C12, 'C12').plot()
        p3.Plot3d([6,10,15,18,21],[0.05,0.01,0.002],self.C44, 'C44').plot()
        
if __name__ == "__main__": ReadElastic().readSM()