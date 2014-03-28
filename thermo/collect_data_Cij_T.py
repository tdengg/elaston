import json
import os
import collections
import numpy as np


dict = {}
dirlist = os.listdir('.')
ersum = 0
calcsum = 0
for dir in dirlist:
    if os.path.isdir(dir) and 'scale' in dir:
        scale = float(dir.lstrip('scale_'))
        dict[scale] = {}
        
            
            
        os.chdir(dir)
        ############################## Read Elastic Constants ##################################
        if os.path.exists('ElaStic_2nd.out'):
            print 'Found elastic constants output for %s.'%str(scale)
            dict[scale]['SM'] = []
            k=0
            for line in open("./ElaStic_2nd.out"):
                 
                ############ Read Youngs Modulus ############
                #if k == 45 and line.split(' ')[12] != '': self.YM[f]={'YM':(float(line.split(' ')[12]))}
                #elif k == 45 and line.split(' ')[12] == '': self.YM[f]={'YM':(float(line.split(' ')[13]))}
                #-------------------------------------------#
                
                ########### Read Stiffness Matrix ###########
                if k in [15,16,17,18,19,20]:
                    for i in line.split(' '):
                        if i != '': 
                            
                            dict[scale]['SM'].append(float(i.rstrip('\n')))
                            
                #############################################        
                
                k+=1
        ######################################################################################## 
        print dict   
        try:
            f = open('F_TV')
            lines = f.readlines()
            T = [float(x.split()[0]) for x in lines]
            F = [float(x.split()[1]) for x in lines]
                
            dict[scale]['F'] = F
            dict[scale]['T'] = T
            dict[scale]['path'] = os.getcwd()
            Thermal = True
            f.close()
        except:
            Thermal = False
            dict[scale]['F'] = None
            dict[scale]['T'] = None
            dict[scale]['path'] = os.getcwd()
            
        dirlist2 = os.listdir('.')
        for dir2 in dirlist2:
            if os.path.isdir(dir2) and 'Dst' in dir2:
                dict[scale][dir2] = {}
                os.chdir(dir2)
                dirlist3 = os.listdir('.')
                for dir3 in dirlist3:
                    if os.path.isdir(dir3) and 'Dst' in dir3:
                        dict[scale][dir2][dir3] = {}
                        os.chdir(dir3)
                        ###########################################################
                        try:
                            f = open('F_TV')
                            lines = f.readlines()
                            T = [float(x.split()[0]) for x in lines]
                            F = [float(x.split()[1]) for x in lines]
                                
                            dict[scale][dir2][dir3]['F'] = F
                            dict[scale][dir2][dir3]['T'] = T
                            dict[scale][dir2][dir3]['path'] = os.getcwd()
                            
                            
                            
                            
                            
                            f.close()
                        except:
                            dict[scale][dir2][dir3]['F'] = None
                            dict[scale][dir2][dir3]['T'] = None
                            dict[scale][dir2][dir3]['path'] = os.getcwd()
                            print 'something is wrong with Free Energy output in: ' +  str(scale) + ' ' + dir2
                            ersum+=1
                        #print dir,dir2,dir3
                        calcsum+=1
                        ###########################################################
                        os.chdir('..')
                os.chdir('..')
                
        os.chdir('..')

if Thermal:        
    conv = 96.47244
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
    f = []
    l = []
    dic = {}
    for d in os.listdir('./'):
        
        if 'scale_' in d:
            os.chdir(d)
            l = float(d.lstrip('scale_'))
            dic[l] = {}
            dic[l]['file'] = open('F_TV').readlines()
            print d
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
            
            ydata.append(dic[out]['F'][ind]/conv + E0[i] + 13.5)
            i+=1
        #polyfit:
        coeff = np.polyfit(xdata,ydata,3)
        p = np.poly1d(coeff)
        
        polyx = np.linspace(min(xdata),max(xdata),1000)
        
        minl.append(np.roots(p.deriv())[1])
        minF.append(p(np.roots(p.deriv())[1]))
        dict['F_min'] = minF
        dict['l_min'] = minl
        dict['T'] = T
    
    
        

print str(ersum) + 'calculations out of ' + str(calcsum) + 'went wrong.'
print os.getcwd()
f2 = open('FT_out.json','w')            
f2.write(json.dumps(dict,indent=3))
f2.close()                
            
        