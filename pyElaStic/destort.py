"""
Class for getting DEFORMATION MATRIX for given spacegroup number and Lagranian strain.

Usage:

Basic Example:
import destort

dist = destort.Destort()                              # generate instance of distortion object
dist.sgn = sgn                                        # set spacegroup number (int)
dist.set_strainList()                                 # set strain list according to space group number

strainType = next(dist.strainList_iter)               # when using the iterator property --> get first distortion type
dist.eta = eta                                        # define lagrangian strain (float)
dist.set_strainType(strainType)                       # set strain type (string)
dist.set_defMatrix()                                  # ste deformation matrix
dist.get_defMatrix()                                  # get deformation matrix
"""

import numpy as np
import sys

class Destort(object):
    def __init__(self, volumeconserving = False, mthd = 'Energy', order = 2):
        self.__eta = 0.05
        self.volumeconserving = volumeconserving
        self.mthd = mthd
        self.order = order
        
        self.Ls_Dic={                       \
        '01':[ 1., 1., 1., 0., 0., 0.],\
        '02':[ 1., 0., 0., 0., 0., 0.],\
        '03':[ 0., 1., 0., 0., 0., 0.],\
        '04':[ 0., 0., 1., 0., 0., 0.],\
        '05':[ 0., 0., 0., 2., 0., 0.],\
        '06':[ 0., 0., 0., 0., 2., 0.],\
        '07':[ 0., 0., 0., 0., 0., 2.],\
        '08':[ 1., 1., 0., 0., 0., 0.],\
        '09':[ 1., 0., 1., 0., 0., 0.],\
        '10':[ 1., 0., 0., 2., 0., 0.],\
        '11':[ 1., 0., 0., 0., 2., 0.],\
        '12':[ 1., 0., 0., 0., 0., 2.],\
        '13':[ 0., 1., 1., 0., 0., 0.],\
        '14':[ 0., 1., 0., 2., 0., 0.],\
        '15':[ 0., 1., 0., 0., 2., 0.],\
        '16':[ 0., 1., 0., 0., 0., 2.],\
        '17':[ 0., 0., 1., 2., 0., 0.],\
        '18':[ 0., 0., 1., 0., 2., 0.],\
        '19':[ 0., 0., 1., 0., 0., 2.],\
        '20':[ 0., 0., 0., 2., 2., 0.],\
        '21':[ 0., 0., 0., 2., 0., 2.],\
        '22':[ 0., 0., 0., 0., 2., 2.],\
        '23':[ 0., 0., 0., 2., 2., 2.],\
        '24':[-1., .5, .5, 0., 0., 0.],\
        '25':[ .5,-1., .5, 0., 0., 0.],\
        '26':[ .5, .5,-1., 0., 0., 0.],\
        '27':[ 1.,-1., 0., 0., 0., 0.],\
        '28':[ 1.,-1., 0., 2., 0., 0.],\
        '29':[ 1.,-1., 0., 0., 0., 2.],\
        '30':[ 1., 0.,-1., 0., 2., 0.],\
        '31':[ 0., 1.,-1., 0., 0., 2.],\
        '32':[ 1., 1.,-1., 2., 2., 2.],\
        '33':[ 1., 0., 0., 2., 2., 0.],\
        '34':[ 0., 1., 0., 2., 2., 0.],\
        '35':[ 1., 1., 0., 2., 2., 0.],\
        '36':[ 1., 1., 0., 2., 0., 0.],\
        '37':[ 1., 1.,-1., 0., 0., 0.],\
        '38':[ 1., 1., 1.,-2.,-2.,-2.],\
        '39':[ 1., 2., 3., 4., 5., 6.],\
        '40':[-2., 1., 4.,-3., 6.,-5.],\
        '41':[ 3.,-5.,-1., 6., 2.,-4.],\
        '42':[-4.,-6., 5., 1.,-3., 2.],\
        '43':[ 5., 4., 6.,-2.,-1.,-3.],\
        '44':[-6., 3.,-2., 5.,-4., 1.]}
        
        self.Ls_str={                                     \
        '01':'(  eta,  eta,  eta,  0.0,  0.0,  0.0)',\
        '02':'(  eta,  0.0,  0.0,  0.0,  0.0,  0.0)',\
        '03':'(  0.0,  eta,  0.0,  0.0,  0.0,  0.0)',\
        '04':'(  0.0,  0.0,  eta,  0.0,  0.0,  0.0)',\
        '05':'(  0.0,  0.0,  0.0, 2eta,  0.0,  0.0)',\
        '06':'(  0.0,  0.0,  0.0,  0.0, 2eta,  0.0)',\
        '07':'(  0.0,  0.0,  0.0,  0.0,  0.0, 2eta)',\
        '08':'(  eta,  eta,  0.0,  0.0,  0.0,  0.0)',\
        '09':'(  eta,  0.0,  eta,  0.0,  0.0,  0.0)',\
        '10':'(  eta,  0.0,  0.0, 2eta,  0.0,  0.0)',\
        '11':'(  eta,  0.0,  0.0,  0.0, 2eta,  0.0)',\
        '12':'(  eta,  0.0,  0.0,  0.0,  0.0, 2eta)',\
        '13':'(  0.0,  eta,  eta,  0.0,  0.0,  0.0)',\
        '14':'(  0.0,  eta,  0.0, 2eta,  0.0,  0.0)',\
        '15':'(  0.0,  eta,  0.0,  0.0, 2eta,  0.0)',\
        '16':'(  0.0,  eta,  0.0,  0.0,  0.0, 2eta)',\
        '17':'(  0.0,  0.0,  eta, 2eta,  0.0,  0.0)',\
        '18':'(  0.0,  0.0,  eta,  0.0, 2eta,  0.0)',\
        '19':'(  0.0,  0.0,  eta,  0.0,  0.0, 2eta)',\
        '20':'(  0.0,  0.0,  0.0, 2eta, 2eta,  0.0)',\
        '21':'(  0.0,  0.0,  0.0, 2eta,  0.0, 2eta)',\
        '22':'(  0.0,  0.0,  0.0,  0.0, 2eta, 2eta)',\
        '23':'(  0.0,  0.0,  0.0, 2eta, 2eta, 2eta)',\
        '24':'( -eta,.5eta,.5eta,  0.0,  0.0,  0.0)',\
        '25':'(.5eta, -eta,.5eta,  0.0,  0.0,  0.0)',\
        '26':'(.5eta,.5eta, -eta,  0.0,  0.0,  0.0)',\
        '27':'(  eta, -eta,  0.0,  0.0,  0.0,  0.0)',\
        '28':'(  eta, -eta,  0.0, 2eta,  0.0,  0.0)',\
        '29':'(  eta, -eta,  0.0,  0.0,  0.0, 2eta)',\
        '30':'(  eta,  0.0, -eta,  0.0, 2eta,  0.0)',\
        '31':'(  0.0,  eta, -eta,  0.0,  0.0, 2eta)',\
        '32':'(  eta,  eta, -eta, 2eta, 2eta, 2eta)',\
        '33':'(  eta,  0.0,  0.0, 2eta, 2eta,  0.0)',\
        '34':'(  0.0,  eta,  0.0, 2eta, 2eta,  0.0)',\
        '35':'(  eta,  eta,  0.0, 2eta, 2eta,  0.0)',\
        '36':'(  eta,  eta,  0.0, 2eta,  0.0,  0.0)',\
        '37':'(  eta,  eta, -eta,  0.0,  0.0,  0.0)',\
        '38':'(  eta,  eta,  eta,-2eta,-2eta,-2eta)',\
        '39':'( 1eta, 2eta, 3eta, 4eta, 5eta, 6eta)',\
        '40':'(-2eta, 1eta, 4eta,-3eta, 6eta,-5eta)',\
        '41':'( 3eta,-5eta,-1eta, 6eta, 2eta,-4eta)',\
        '42':'(-4eta,-6eta, 5eta, 1eta,-3eta, 2eta)',\
        '43':'( 5eta, 4eta, 6eta,-2eta,-1eta,-3eta)',\
        '44':'(-6eta, 3eta,-2eta, 5eta,-4eta, 1eta)'}
        
        self.LC_Dic = {              \
        'CI' :'Cubic I'        ,\
        'CII':'Cubic II'       ,\
        'HI' :'Hexagonal I'    ,\
        'HII':'Hexagonal II'   ,\
        'RI' :'Rhombohedral I' ,\
        'RII':'Rhombohedral II',\
        'TI' :'Tetragonal I'   ,\
        'TII':'Tetragonal II'  ,\
        'O'  :'Orthorhombic'   ,\
        'M'  :'Monoclinic'     ,\
        'N'  :'Triclinic'} 
        
    
    def set_eta(self, eta):
        if eta <= 0.1:
            print "eta = %f"%eta
            self.__eta = eta
        elif eta > 0.1:
            self.__eta = 0.1
            print "Warning: Maximum Lagrangian strain to high (should be in the range: 0.01<eta<0.1) --> Automatically set to 0.1"
        
    def get_eta(self):
        return self.__eta
    
    def set_sgn(self, sgn):
        self.__sgn = sgn
        
    def get_sgn(self):
        return self.__sgn
    
    def set_strainType(self, strainType = None):
        if strainType in self.__Lag_strain_list:
            self.__strainType = strainType
        elif strainType == None:
            self.__strainType = next(self.__Lag_strain_list_i)      #DEBUG!! Iterator does not work....
            
    def get_strainType(self):
        return self.__strainType
    
    def set_defMatrix(self):
        
        if (self.__eta==0.):
            if (self.mthd == 'Energy'): self.__eta = 0.0001
            if (self.mthd == 'Stress'): self.__eta = 0.00001

        Ls = np.zeros(6)
        for j in range(6):
            Ls[j] = self.Ls_Dic[self.__strainType][j]
            
        Lv = self.__eta*Ls
        if  self.__strainType == '08' and self.volumeconserving:
            Lv[0] = self.__eta*(self.__eta/2.+1.)
            Lv[1] = self.__eta*(self.__eta/2.-1.)
            Lv[2] = self.__eta**2./(1.-self.__eta**2.)*(1+0.5*self.__eta**2./(1.-self.__eta**2.))
        # Lagrangian strain to physical strain (eta = eps + 0.5*eps*esp) --------------------------
        eta_matrix      = np.zeros((3,3))

        eta_matrix[0,0] = Lv[0]
        eta_matrix[0,1] = Lv[5]/2.
        eta_matrix[0,2] = Lv[4]/2.
        
        eta_matrix[1,0] = Lv[5]/2.
        eta_matrix[1,1] = Lv[1]
        eta_matrix[1,2] = Lv[3]/2.

        eta_matrix[2,0] = Lv[4]/2.
        eta_matrix[2,1] = Lv[3]/2.
        eta_matrix[2,2] = Lv[2]

        norm       = 1.0

        eps_matrix = eta_matrix
        if (np.linalg.norm(eta_matrix) > 0.7):
            sys.exit('\n     ... Oops ERROR: Too large deformation!\n') 

        while( norm > 1.e-10 ):
            x          = eta_matrix - np.dot(eps_matrix, eps_matrix)/2.
            norm       = np.linalg.norm(x - eps_matrix)      
            eps_matrix = x
            
        i_matrix   = np.array([[1., 0., 0.],
                            [0., 1., 0.], 
                            [0., 0., 1.]])
        self.__defMatrix = i_matrix + eps_matrix
        #M_new      = np.dot(M_old, def_matrix)
        
        
    def get_defMatrix(self):
        return self.__defMatrix
    
    def set_strainList(self):
        SGN = self.__sgn
        if (1 <= SGN and SGN <= 2):      # Triclinic
            LC = 'N'
            if (self.order == 2): ECs = 21
            if (self.order == 3): ECs = 56  
        
        elif(3 <= SGN and SGN <= 15):    # Monoclinic
            LC = 'M'
            if (self.order == 2): ECs = 13
            if (self.order == 3): ECs = 32 
        
        elif(16 <= SGN and SGN <= 74):   # Orthorhombic
            LC = 'O'
            if (self.order == 2): ECs =  9
            if (self.order == 3): ECs = 20 
        
        elif(75 <= SGN and SGN <= 88):   # Tetragonal II
            LC = 'TII'
            if (self.order == 2): ECs =  7
            if (self.order == 3): ECs = 16
          
        elif(89 <= SGN and SGN <= 142):  # Tetragonal I
            LC = 'TI'
            if (self.order == 2): ECs =  6
            if (self.order == 3): ECs = 12  
        
        elif(143 <= SGN and SGN <= 148): # Rhombohedral II 
            LC = 'RII'
            if (self.order == 2): ECs =  7
            if (self.order == 3): ECs = 20
        
        elif(149 <= SGN and SGN <= 167): # Rhombohedral I
            LC = 'RI'
            if (self.order == 2): ECs =  6
            if (self.order == 3): ECs = 14
        
        elif(168 <= SGN and SGN <= 176): # Hexagonal II
            LC = 'HII'
            if (self.order == 2): ECs =  5
            if (self.order == 3): ECs = 12
        
        elif(177 <= SGN and SGN <= 194): # Hexagonal I
            LC = 'HI'
            if (self.order == 2): ECs =  5
            if (self.order == 3): ECs = 10
        
        elif(195 <= SGN and SGN <= 206): # Cubic II
            LC = 'CII'
            if (self.order == 2): ECs =  3
            if (self.order == 3): ECs =  8
        
        elif(207 <= SGN and SGN <= 230): # Cubic I
            LC = 'CI'
            if (self.order == 2): ECs =  3
            if (self.order == 3): ECs =  6
        else: sys.exit('\n     ... Oops ERROR: WRONG Space-Group Number !?!?!?    \n')
        
        if (self.mthd == 'Energy'):
            if (self.order == 2):
                if (LC == 'CI' or \
                    LC == 'CII'):
                    Lag_strain_list = ['01','08','23']
                if (LC == 'HI' or \
                    LC == 'HII'):
                    Lag_strain_list = ['01','26','04','03','17']
                if (LC == 'RI'):
                    Lag_strain_list = ['01','08','04','02','05','10']
                if (LC == 'RII'):
                    Lag_strain_list = ['01','08','04','02','05','10','11']
                if (LC == 'TI'):
                    Lag_strain_list = ['01','26','27','04','05','07']
                if (LC == 'TII'):
                    Lag_strain_list = ['01','26','27','28','04','05','07']
                if (LC == 'O'):
                    Lag_strain_list = ['01','26','25','27','03','04','05','06','07']
                if (LC == 'M'):
                    Lag_strain_list = ['01','25','24','28','29','27','20','12','03','04','05','06','07']
                if (LC == 'N'):
                    Lag_strain_list = ['02','03','04','05','06','07','08','09','10','11',\
                                       '12','13','14','15','16','17','18','19','20','21','22']
        
            if (self.order == 3):
                if (LC == 'CI'):
                    Lag_strain_list = ['01','08','23','32','10','11']
                if (LC == 'CII'):
                    Lag_strain_list = ['01','08','23','32','10','11','12','09']
                if (LC == 'HI'):
                    Lag_strain_list = ['01','26','04','03','17','30','08','02','10','14']
                if (LC == 'HII'):
                    Lag_strain_list = ['01','26','04','03','17','30','08','02','10','14','12','31']
                if (LC == 'RI'):
                    Lag_strain_list = ['01','08','04','02','05','10','11','26','09','03','17','34','33','35']
                if (LC == 'RII'):
                    sys.exit('\n     ... Oops SORRY: Not implemented yet. \n')
                if (LC == 'TI'):
                    sys.exit('\n     ... Oops SORRY: Not implemented yet. \n')
                if (LC == 'TII'):
                    sys.exit('\n     ... Oops SORRY: Not implemented yet. \n')
                if (LC == 'O'):
                    sys.exit('\n     ... Oops SORRY: Not implemented yet. \n')
                if (LC == 'M'):
                    sys.exit('\n     ... Oops SORRY: Not implemented yet. \n')
                if (LC == 'N'):
                    sys.exit('\n     ... Oops SORRY: Not implemented yet. \n')
        
        if (self.mthd == 'Stress'):
            if (self.order == 2):
                if (LC == 'CI' or \
                    LC == 'CII'):
                    Lag_strain_list = ['36']
                if (LC == 'HI' or \
                    LC == 'HII'):
                    Lag_strain_list = ['36','38']
                if (LC == 'RI' or \
                    LC == 'RII'):
                    Lag_strain_list = ['36','38']
                if (LC == 'TI' or \
                    LC == 'TII'):
                    Lag_strain_list = ['36','38']
                if (LC == 'O'):
                    Lag_strain_list = ['36','38','40']
                if (LC == 'M'):
                    Lag_strain_list = ['36','37','38','39','40']
                if (LC == 'N'):
                    Lag_strain_list = ['36','37','38','39','40','41']
        
            if (self.order == 3):
                if (LC == 'CI'):
                    sys.exit('\n     ... Oops SORRY: Not implemented yet. \n')
                if (LC == 'CII'):
                    sys.exit('\n     ... Oops SORRY: Not implemented yet. \n')
                if (LC == 'HI'):
                    sys.exit('\n     ... Oops SORRY: Not implemented yet. \n')
                if (LC == 'HII'):
                    sys.exit('\n     ... Oops SORRY: Not implemented yet. \n')
                if (LC == 'RI'):
                    sys.exit('\n     ... Oops SORRY: Not implemented yet. \n')
                if (LC == 'RII'):
                    sys.exit('\n     ... Oops SORRY: Not implemented yet. \n')
                if (LC == 'TI'):
                    sys.exit('\n     ... Oops SORRY: Not implemented yet. \n')
                if (LC == 'TII'):
                    sys.exit('\n     ... Oops SORRY: Not implemented yet. \n')
                if (LC == 'O'):
                    sys.exit('\n     ... Oops SORRY: Not implemented yet. \n')
                if (LC == 'M'):
                    sys.exit('\n     ... Oops SORRY: Not implemented yet. \n')
                if (LC == 'N'):
                    sys.exit('\n     ... Oops SORRY: Not implemented yet. \n')

        self.__Lag_strain_list   = Lag_strain_list
        self.__Lag_strain_list_i = iter(Lag_strain_list)
        
    def get_strainList(self):
        return self.__Lag_strain_list
    
    def get_strainList_iter(self):
        return self.__Lag_strain_list_i
    
    # object properties definition
    strainList      = property(fget = get_strainList      , fset= set_strainList)
    strainList_iter = property(fget = get_strainList_iter , fset= set_strainList)
    defMatrix       = property(fget = get_defMatrix       , fset= set_defMatrix )
    strainType      = property(fget = get_strainType      , fset= set_strainType)
    sgn             = property(fget = get_sgn             , fset= set_sgn       )
    eta             = property(fget = get_eta             , fset= set_eta       )
    
class NECs(object):
    def __init__(self, SGN):
        self.__SGN = SGN
        self.set_ECs()
        
    def set_ECs(self):
        if (1 <= self.__SGN and self.__SGN <= 2):      # Triclinic
            LC = 'N'
            if (self.order == 2): ECs = 21
            if (self.order == 3): ECs = 56  
        
        elif(3 <= self.__SGN and self.__SGN <= 15):    # Monoclinic
            LC = 'M'
            if (self.order == 2): ECs = 13
            if (self.order == 3): ECs = 32 
        
        elif(16 <= self.__SGN and self.__SGN <= 74):   # Orthorhombic
            LC = 'O'
            if (self.order == 2): ECs =  9
            if (self.order == 3): ECs = 20 
        
        elif(75 <= self.__SGN and self.__SGN <= 88):   # Tetragonal II
            LC = 'TII'
            if (self.order == 2): ECs =  7
            if (self.order == 3): ECs = 16
          
        elif(89 <= self.__SGN and self.__SGN <= 142):  # Tetragonal I
            LC = 'TI'
            if (self.order == 2): ECs =  6
            if (self.order == 3): ECs = 12  
        
        elif(143 <= self.__SGN and self.__SGN <= 148): # Rhombohedral II 
            LC = 'RII'
            if (self.order == 2): ECs =  7
            if (self.order == 3): ECs = 20
        
        elif(149 <= self.__SGN and self.__SGN <= 167): # Rhombohedral I
            LC = 'RI'
            if (self.order == 2): ECs =  6
            if (self.order == 3): ECs = 14
        
        elif(168 <= self.__SGN and self.__SGN <= 176): # Hexagonal II
            LC = 'HII'
            if (self.order == 2): ECs =  5
            if (self.order == 3): ECs = 12
        
        elif(177 <= self.__SGN and self.__SGN <= 194): # Hexagonal I
            LC = 'HI'
            if (self.order == 2): ECs =  5
            if (self.order == 3): ECs = 10
        
        elif(195 <= self.__SGN and self.__SGN <= 206): # Cubic II
            LC = 'CII'
            if (self.order == 2): ECs =  3
            if (self.order == 3): ECs =  8
        
        elif(207 <= self.__SGN and self.__SGN <= 230): # Cubic I
            LC = 'CI'
            if (self.order == 2): ECs =  3
            if (self.order == 3): ECs =  6
        else: sys.exit('\n     ... Oops ERROR: WRONG Space-Group Number !?!?!?    \n')
        
        self.__ECs = ECs
        self.__LC  = LC
        
    def get_ECs(self):
        return self.__ECs
    
    def get_LC(self):
        return self.__LC
        
    