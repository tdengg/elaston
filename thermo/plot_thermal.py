import matplotlib.pyplot as plt
import os
import collections
import numpy as np

ax1=plt.subplot(131)
conv = 96.47244
E0 = [-12.9134126425926,-12.9561293683796,-12.9855977629167,-13.0024569074537,-13.00747908,-13.0012977288426,-12.9846557038889,-12.9581672949074,-12.9225093520833,-12.878249430787]
f = []
l = []
dic = {}
for d in os.listdir('./'):
	
	try:
		os.chdir(d)
		l = float(d.lstrip('scale_'))
		dic[l] = {}
		dic[l]['file'] = open('F_TV').readlines()
		
		os.chdir('..')
	except:
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
print dic

trange = [0,10,20,30,40,50,60,80,100,200,300,400,500,600,700,800,900,1000]
ndic = collections.OrderedDict(sorted(dic.items()))	#sort dictionary
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
	
	ax1.plot(xdata,ydata,'+')
	ax1.plot(polyx,p(polyx))
	minl.append(np.roots(p.deriv())[1])
	minF.append(p(np.roots(p.deriv())[1]))
	
#polyfit F-T
coeff = np.polyfit(minl,minF,21)
p = np.poly1d(coeff)
polyx = np.linspace(min(minl),max(minl),1000)

ax1.plot(polyx,p(polyx))
ax1.plot(minl,minF,'o')

#polyfit thermal expansion:
ax2 = plt.subplot(132)
coeff = np.polyfit(trange,minl,4)
p = np.poly1d(coeff)
polyx = np.linspace(min(trange),max(trange),1000)

ax2.plot(polyx,p(polyx))
ax2.plot(trange,minl,'o')

#thermal expansion/T
ax3 = plt.subplot(133)
alpha = []
for i in range(len(trange)-1):
	alpha.append((minl[i+1]-minl[i])/(trange[i+1]-trange[i])/minl[0])
ax3.plot(trange[:-1], alpha)
plt.show()
		
		
