import os
import plot3d as p3
import lxml.etree as etree
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
        pars = {'1':{'ngridk':6, 'swidth':0.05},'2':{'ngridk':10, 'swidth':0.05},'3':{'ngridk':15, 'swidth':0.05},'4':{'ngridk':18, 'swidth':0.05},'5':{'ngridk':21, 'swidth':0.05},'6':{'ngridk':25, 'swidth':0.05},'7':{'ngridk':6, 'swidth':0.01},'8':{'ngridk':10, 'swidth':0.01},'9':{'ngridk':15, 'swidth':0.01},'10':{'ngridk':18, 'swidth':0.01},'11':{'ngridk':21, 'swidth':0.01},'12':{'ngridk':25, 'swidth':0.01},'13':{'ngridk':6, 'swidth':0.002},'14':{'ngridk':10, 'swidth':0.002},'15':{'ngridk':15, 'swidth':0.002},'16':{'ngridk':18, 'swidth':0.002},'17':{'ngridk':21, 'swidth':0.002},'18':{'ngridk':25, 'swidth':0.002},'19':{'ngridk':27, 'swidth':0.05},'20':{'ngridk':30, 'swidth':0.05},'21':{'ngridk':27, 'swidth':0.01},'22':{'ngridk':30, 'swidth':0.01},'23':{'ngridk':27, 'swidth':0.002},'24':{'ngridk':30, 'swidth':0.002},'25':{'ngridk':33, 'swidth':0.01},'26':{'ngridk':36, 'swidth':0.01}}
        #pars = {'o_7':{'dist':7},'o_11':{'dist':11},'o_15':{'dist':11},'o_21':{'dist':21}}
        for f in self.filelist:
            
            if os.path.isdir(f) and os.path.exists('%s/ElaStic_2nd.out'%f): os.chdir(f)
            else: continue
            
            self.SM[f] = {}
            self.SM[f]['SM'] = []
            k=0
            for line in open("./ElaStic_2nd.out"):
                 
                ############ Read Youngs Modulus ############
                if k == 45 and line.split(' ')[12] != '': self.YM[f]={'YM':(float(line.split(' ')[12]))}
                elif k == 45 and line.split(' ')[12] == '': self.YM[f]={'YM':(float(line.split(' ')[13]))}
                #-------------------------------------------#
                
                ########### Read Stiffness Matrix ###########
                if k in [15,16,17,18,19,20]:
                    for i in line.split(' '):
                        if i != '': 
                            
                            self.SM[f]['SM'].append(float(i.rstrip('\n')))
                            
                #############################################        
                
                k+=1
            
            for key in pars[f].keys():
                self.SM[f][key] = pars[f][key]
            
                self.YM[f][key] = pars[f][key]
                
                 
            os.chdir('..')
            j+=1
        
        for di in self.SM.keys():
            self.C11[di] = self.SM[di]['SM'][0]
        
        for di in self.SM.keys():
            self.C12[di] = self.SM[di]['SM'][1]
            
        for di in self.SM.keys():
            self.C44[di] = self.SM[di]['SM'][21]
            
        ########## xml-output #########
        
        root = etree.Element("C")
        i = 0
        for el in self.SM.keys():
            root.append(etree.Element('d'+str(el)))
            root[i].set('n', str(el))
            for tag in self.SM[el]:
                root[i].set(tag,str(self.SM[el][tag]))
            
            i+=1
        
        et = etree.ElementTree(root)
        et.write('Elastic_SM.xml', pretty_print=True)
        
        root = etree.Element("C")
        i = 0
        for el in self.YM.keys():
            root.append(etree.Element('d'+str(el)))
            root[i].set('n', str(el))
            for tag in self.YM[el]:
                root[i].set(tag,str(self.YM[el][tag]))
            
            i+=1
        
        et = etree.ElementTree(root)
        et.write('Elastic_YM.xml', pretty_print=True)
        
        
        
        
        ##########    PLOT    ##########
        
        #plt.plot([7,11,15,21],[self.YM['o_7'],self.YM['o_11'],self.YM['o_15'],self.YM['o_21']], label = "Youngs Modulus")
        #plt.plot([7,11,15,21],[self.C12['o_7'],self.C12['o_11'],self.C12['o_15'],self.C12['o_21']], label = "C11")
        #plt.plot([7,11,15,21],[self.C11['o_7'],self.C11['o_11'],self.C11['o_15'],self.C11['o_21']], label = "C12")
        #plt.plot([7,11,15,21],[self.C44['o_7'],self.C44['o_11'],self.C44['o_15'],self.C44['o_21']], label = "C44")
        #plt.legend(title='ngridk')
        #plt.title('Number of distorted Structures N')
        #plt.xlabel("N")
        #plt.ylabel("GPa")
        
        #plt.show()
        #self.X = {}
        #p3.Plot3d([6,10,15,18,21,25,27,30],[0.05,0.01,0.002],self.YM, 'YM').plot()#0.05,0.01,0.002
        #p3.Plot3d([6,10,15,18,21,25,27,30],[0.05,0.01,0.002],self.C11, 'C11').plot()
        #p3.Plot3d([6,10,15,18,21,25,27,30],[0.05,0.01,0.002],self.C12, 'C12').plot()
        #p3.Plot3d([6,10,15,18,21,25,27,30],[0.05,0.01,0.002],self.C44, 'C44').plot()
        
if __name__ == "__main__": ReadElastic().readSM()