from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

class Plot3d(object):
    def __init__(self, X,Y,Z, title):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.title = title
    def plot(self):
        X = []
        Y = []
        Z = []
        fig = plt.figure()
        ax = fig.add_subplot(121, projection='3d')
        ax1 = fig.add_subplot(122)
        # Generate X array #
        for i in range(len(self.Y)): X.append(self.X)
        
        # Generate Y array #
        for i in range(len(self.Y)): 
            Y.append([])
            for j in range(len(self.X)): Y[i].append(self.Y[i])
        
        # Generate Z array #
        k = 1
        for i in range(len(self.Y)):
            Z.append([])
            for j in range(len(self.X)): 
                for subdirs in self.Z.values():
                    
                    if subdirs['ngridk'] == float(X[i][j]) and subdirs['swidth'] == float(Y[i][j]):
                        print X[i][j], Y[i][j]
                        print self.Z[str(k)][self.title]
                        Z[i].append(self.Z[str(k)][self.title]) 
                k+=1
        
        #X = [[6,10,15,18,21,25],[6,10,15,18,21,25],[6,10,15,18,21,25]]
        #Y = [[0.002,0.002,0.002,0.002,0.002,0.002],[0.01,0.01,0.01,0.01,0.01,0.01],[0.05,0.05,0.05,0.05,0.05,0.05]]
        #Z = [[154.73,-4.72,100.11,79.55,-11.85,812.45],[151.18,-21.51,104.63,78.93,383.18,808.11],[175.80,81.93,94.61,95.47,79.40,779.75]]
        X=np.array(X)
        Y=np.array(Y)
        Z=np.array(Z)
        print X, Y, Z
        ax.plot_wireframe(X, Y, Z)
        label = ["0.05","0.01","0.002"]
        for i in range(len(X)): ax1.plot(self.X,Z[i],label=label[i])
        ax1.legend()
        ax1.set_xlabel("ngrid")
        ax1.set_ylabel("GPa")
        ax.set_xlabel("ngrid")
        ax.set_ylabel("swidth")
        ax.set_zlabel("GPa")
        plt.title(self.title)
        plt.show()
if __name__ == "__main__": Plot3d([6,10,15,18,21,25],[0.05,0.01,0.002],{},'').plot()