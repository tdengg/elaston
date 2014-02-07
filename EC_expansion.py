import numpy as np
import lxml.etree as et
import matplotlib.pyplot as plt

class ECS(object):
    
    def __init__(self):
        
        _e     = 1.602176565e-19              # elementary charge
        Bohr   = 5.291772086e-11              # a.u. to meter
        Ryd2eV = 13.605698066                 # Ryd to eV
        Angstroem = 1.e-10                    # Angstroem to meter
        #ToGPa  = (_e*Ryd2eV)/(1e9*Bohr**3)    # Ryd/[a.u.^3] to GPa
        self.vToGPa  = (_e)/(1e9*Angstroem**3)   # eV/[Angstroem^3] to GPa
        
        
        #alpha = 1
        #gamma = 1
        #beta  = 1
        #lamb  = 1
        
        
        vaspout = et.parse("vasprun.xml")
        self.V = float(vaspout.xpath("//i[@name='volume']/text()")[0])
        
        self.pos = [map(float, i.split()) for i in vaspout.xpath("//structure[@name='finalpos']/varray[@name='positions']/v/text()")]
            
        self.basis = [map(float, i.split()) for i in vaspout.xpath("//structure[@name='finalpos']/crystal/varray[@name='basis']/v/text()")]
        self.basis = np.array(self.basis)
        self.hessian = [map(float, i.split()) for i in vaspout.xpath("//varray[@name='hessian']/v/text()")]
        self.eigval = [map(float, i.split()) for i in vaspout.xpath("//v[@name='eigenvalues']/text()")]
        #self.eigvec  = [map(float, i.split()) for i in vaspout.xpath("//varray[@name='eigenvectors']/v/text()")]
        self.s = 1#len(self.basis)
        #print len(self.eigvec[0]), len(self.eigval[0]), len(self.hessian)
        self.n = len(self.pos)
        self.n = self.n/self.s
        self.m = int(self.n**(1/3.))
        self.latt = np.abs(self.basis[0][0]*2.)
        self.FC = self.read_FC()
        
        self.pos = [np.dot(np.array(self.basis),pos) for pos in np.array(self.pos)]
        
        #FC_matrix:
        self.FC_matrix = []
        for i in range(self.n):
            
            for k in range(3):
                self.FC_matrix.append([])
                
                for j in range(self.n):
                    
                    self.FC_matrix[3*i+k].extend(self.FC[(i+1,j+1)][k])
                    
        
        self.C0 = np.linalg.inv(np.array(self.FC_matrix))
        
        
        print self.br(0, 0, 0, 0)*self.vToGPa/self.V
        #C11 = 1./self.V * (self.sq_br(alpha, beta, gamma, lamb) + self.sq_br(beta, gamma, alpha, lamb) - self.sq_br(beta, lamb, alpha, gamma))# + self.br(alpha, gamma, beta, lamb))
        #C11 = C11* self.vToGPa
        #self.plot_FC()
        #alpha = 0
        #gamma = 0
        #beta  = 1
        #lamb  = 1
        #C22 = 1./self.V * (self.sq_br(alpha, beta, gamma, lamb) + self.sq_br(beta, gamma, alpha, lamb) - self.sq_br(beta, lamb, alpha, gamma))# + self.br(alpha, gamma, beta, lamb))
        
        
        print '########################################'
        print "%10f %10f %10f %10f %10f %10f"%(self.Cij(0,0,0,0), self.Cij(0,0,1,1), self.Cij(0,0,2,2), self.Cij(0,0,1,2), self.Cij(0,0,2,0), self.Cij(0,0,0,1))
        print "%10f %10f %10f %10f %10f %10f"%(self.Cij(1,1,0,0), self.Cij(1,1,1,1), self.Cij(1,1,2,2), self.Cij(1,1,1,2), self.Cij(1,1,2,0), self.Cij(1,1,0,1))
        print "%10f %10f %10f %10f %10f %10f"%(self.Cij(2,2,0,0), self.Cij(2,2,1,1), self.Cij(2,2,2,2), self.Cij(2,2,1,2), self.Cij(2,2,2,0), self.Cij(2,2,0,1))
        print "%10f %10f %10f %10f %10f %10f"%(self.Cij(1,2,0,0), self.Cij(1,2,1,1), self.Cij(1,2,2,2), self.Cij(1,2,1,2), self.Cij(1,2,2,0), self.Cij(1,2,0,1))
        print "%10f %10f %10f %10f %10f %10f"%(self.Cij(2,0,0,0), self.Cij(2,0,1,1), self.Cij(2,0,2,2), self.Cij(2,0,1,2), self.Cij(2,0,2,0), self.Cij(2,0,0,1))
        print "%10f %10f %10f %10f %10f %10f"%(self.Cij(0,1,0,0) ,self.Cij(0,1,1,1), self.Cij(0,1,2,2), self.Cij(0,1,1,2), self.Cij(0,1,2,0), self.Cij(0,1,0,1))
        
    def Cij(self, alpha,gamma,beta,lamb):
        Cij = 1./self.V * (self.sq_br(alpha, beta, gamma, lamb) + self.sq_br(beta, gamma, alpha, lamb) - self.sq_br(beta, lamb, alpha, gamma))# + self.br(alpha, gamma, beta, lamb))
        return Cij* self.vToGPa
        
    def sq_br(self, alpha, beta, gamma, lamb):
        br = 0.
        #for k1 in range(self.s):
            #for k2 in range(self.s):
        for l3 in range(int((self.n)**(1/3.))):
            for l2 in range(int((self.n)**(1/3.))):
                for l1 in range(int((self.n)**(1/3.))):
                    for k1 in range(self.s):
                    
                    ##lattice coordinates
                        
                        #print self.n**(1/3.), l1,l2,l3,int(l1+1 + self.n**(1/3.)*(l2)+(self.n**(1/3.))**2*(l3))
                        x_g = self.pos[int(l1 + self.n**(1/3.)*(l2) + (self.n**(1/3.))**2*(l3))+k1*(self.n)][gamma]#+self.basis[k1][gamma]-self.basis[k2][gamma]
                        x_l = self.pos[int(l1 + self.n**(1/3.)*(l2) + (self.n**(1/3.))**2*(l3))+k1*(self.n)][lamb]#+self.basis[k1][lamb]-self.basis[k2][lamb]
                        #print x_g,x_l
                    ##cartesian coordinates
                    #if gamma == 0:   kg = np.array([1.,0.,0.])
                    #elif gamma == 1: kg = np.array([0.,1.,0.])
                    #elif gamma == 2: kg = np.array([0.,0.,1.])
                    
                    #x_g = max(self.pos[l]+self.basis[k1]-self.basis[k2]*kg)
                    
                    #if lamb == 0:    kl = np.array([1.,0.,0.])
                    #elif lamb == 1:  kl = np.array([0.,1.,0.])
                    #elif lamb == 2:  kl = np.array([0.,0.,1.])
                    
                    #x_l = max(self.pos[l]+self.basis[k1]-self.basis[k2]*kl)
                        
                        br = br - 0.5 * self.FC[(1,1+int(l1 + self.n**(1/3.)*(l2) + (self.n**(1/3.))**2*(l3))+k1*(self.n))][alpha][beta]*x_g*x_l
                    
        return br
        
    def br(self, alpha, gamma, beta, lamb):
        br = 0.
        for k1 in range(self.s):
            for k2 in range(self.s):
                for my in range(3):
                    for ny in range(3):
                        if k1 and k2 == 0:
                            continue
                        else:
                            br = br - self.C0[3*k1+my][3*k2+ny]*self.sum_k3(my, alpha, gamma, k1)*self.sum_k3(ny, beta, lamb, k2)
        return  br
    
    
    def sum_k3(self, my,alpha,gamma,k1):
        summ = 0.
        for k3 in range(self.s):
            for l in range(self.n):
                x_g = self.pos[l][gamma] + self.basis[k1][gamma] - self.basis[k3][gamma]
                summ = summ + self.FC[(1,1+l)][my][alpha]*x_g
                #summ = summ + self.hessian[3*k1+my][3*k3+alpha]*x
        
        return summ

    def read_FC(self):
        FC_file = open('FORCE_CONSTANTS')
        FC = {}
        lines = FC_file.readlines()
        i = 1
        for l in lines:
            
            if i==1:    natoms = l
            elif (i-2)%4 == 0: 
                
                k1,k2 = map(int, l.split())
                FC[(k1,k2)] = []
            else:
                FC[(k1,k2)].append(map(float,l.split()))
            i+=1
        
        return FC
    
    def plot_FC(self):
        rdiag_x = []
        edge_x = []
        diag_x = []
        rdiag_x1 = []
        edge_x1 = []
        diag_x1 = []
        cell = []
        i=1
        while i <= self.m:
            j=1
            cell.append(i)
            while j <= self.s:
                if j == 2:
                    edge_x1.append(self.FC[1,i+(j-1)*self.n][0][0])
                    rdiag_x1.append(self.FC[(1,(i*(1+self.m+self.m**2) - self.m - self.m**2)+(j-1)*self.n)][0][0])
                    diag_x1.append(self.FC[(1,i+self.m*(i-1)+(j-1)*self.n)][0][0])
                elif j == 1:
                    edge_x.append(self.FC[1,i+(j-1)*self.n][0][0])
                    rdiag_x.append(self.FC[(1,(i*(1+self.m+self.m**2) - self.m - self.m**2)+(j-1)*self.n)][0][0])
                    diag_x.append(self.FC[(1,i+self.m*(i-1)+(j-1)*self.n)][0][0])
                j+=1
            i+=1
            print len(cell), len(rdiag_x)
        plt.plot(cell, rdiag_x)
        plt.plot(cell, rdiag_x1,'.-')
        
        #plt.plot(cell, edge_x)
        #plt.plot(cell, edge_x1,'.-')
        
        #plt.plot(cell, diag_x)
        #plt.plot(cell, diag_x1,'.-')
        plt.show()
        return
        
if __name__ == "__main__":
    ECS()

