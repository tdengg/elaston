import matplotlib.pyplot as plt
import lxml.etree as et
import json



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