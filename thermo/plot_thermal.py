import matplotlib.pyplot as plt
import os
import collections
import numpy as np
import lxml.etree as et

class PLOT_THERMAL(object):
	def __init__(self, dir, style='-'):
		self.dir = dir
		self._lname = None
		self.style = style
		self.conv = 96.47244

	def get_data(self):
		f = []
		l = []
		dic = {}
		
		for d in os.listdir(self.dir):
			
			if 'scale_' in d:
				
				l = float(d.lstrip('scale_'))
				
				try:
					vrun = et.parse(self.dir+'/'+d+'/vasprun.xml')
					dic[l] = {}
					dic[l]['file'] = open(self.dir+'/'+d+'/F_TV').readlines()
					dic[l]['vasprun'] = vrun
				except:
					continue
				
				
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
			dic[out]['E0'] = float(dic[out]['vasprun'].xpath("//scstep[last()]/energy/i[@name = 'e_0_energy']")[0].text)
			#plt.plot(T,F)
			
			j+=1
		return dic
	
	def free_ene(self,dic, trange, E0):
		
		#ax = plt.subplot(111)
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
				
				ydata.append(dic[out]['F'][ind]/self.conv + E0[i] + 13.5)
				i+=1
			#polyfit:
			coeff = np.polyfit(xdata,ydata,3)
			p = np.poly1d(coeff)
			polyx = np.linspace(min(xdata),max(xdata),1000)
			
			#ax.plot(xdata,ydata,'+')
			#ax.plot(polyx,p(polyx))
			minl.append(np.roots(p.deriv())[1])
			minF.append(p(np.roots(p.deriv())[1]))
			
			#polyfit F-T
			coeff = np.polyfit(minl,minF,21)
			p = np.poly1d(coeff)
			polyx = np.linspace(min(minl),max(minl),1000)
	
			#ax.plot(polyx,p(polyx))
			#ax.plot(minl,minF,'o')
		
		
		
		print self._lname
		#polyfit thermal expansion:
		
		coeff = np.polyfit(trange,minl,4)
		p = np.poly1d(coeff)
		polyx = np.linspace(min(trange),max(trange),1000)
		
		#ax1 = plt.plot(polyx,p(polyx))
		#ax1 = plt.plot(trange,minl,'o')
		
		#thermal expansion/T
		
		alpha = []
		for i in range(len(trange)-1):
			alpha.append((minl[i+1]-minl[i])/(trange[i+1]-trange[i])/minl[0]*10**6.)
		plt.plot(trange[:-1], alpha, label = self._lname, lw=2., ls=self.style)
	
	@property
	def lname(self):
		return self._lname
	@lname.setter
	def lname(self, value):
		self._lname = value
		
			
