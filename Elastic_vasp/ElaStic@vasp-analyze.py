#!/usr/bin/env python
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
#%%% -------------------------------- ElaStic@exciting-analyze ------------------------------- %%%#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
#
# AUTHORS:
# Rostam Golesorkhtabar and Pasquale Pavone 
# r.golesorkhtabar@gmail.com
# 
# DATE:
# Sun Jan 01 00:00:00 2012
#
# SYNTAX:
# python ElaStic@exciting-analyze.py
#        ElaStic@exciting-analyze



# 
# EXPLANATION:
# 
#__________________________________________________________________________________________________

from sys   import stdin
from numpy import *
from math import *
import numpy as np
import subprocess
import warnings
import os.path
import shutil
import copy
import math
import sys
import os
import lxml.etree as et

#%%%%%%%%--- CONSTANTS ---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#_e     = 1.602176565e-19              # elementary charge
#Bohr   = 5.291772086e-11              # a.u. to meter
#Ryd2eV = 13.605698066                 # Ryd to eV
#cnvrtr = (_e*Ryd2eV)/(1e9*Bohr**3)    # Ryd/[a.u.^3] to GPa
#--------------------------------------------------------------------------------------------------
_e     = 1.602176565e-19
Angstroem = 1.e-10
cnvrtr = (_e)/(1e9*Angstroem**3)    # ev/[Anstroem^3] to GPa

#%%%--- SUBROUTINS AND FUNCTIONS ---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def sortlist(lst1, lst2):
    temp = copy.copy(lst1)

    lst3 = []
    lst4 = []

    temp.sort()

    for i in range(len(lst1)):
        lst3.append(lst1[lst1.index(temp[i])])
        lst4.append(lst2[lst1.index(temp[i])])

    return lst3, lst4
#--------------------------------------------------------------------------------------------------

#%%%--- Reading the INFO_ElaStic file ---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
INFO=open('INFO_ElaStic', 'r')

l1  = INFO.readline()
ordr= int(l1.split()[-1])

if (ordr != 2 and ordr != 3):
    sys.exit('\n     ... Oops ERROR: The order of the elastic constant is NOT clear !?!?!?'\
             '\n                     Something is WRONG in the "INFO_ElaStic" file.\n')

l2  = INFO.readline()
mthd= l2.split()[-1]

if (mthd != 'Stress' and mthd != 'Energy'):
    sys.exit('\n     ... Oops ERROR: The method of the calculation is NOT clear !?!?!?'\
             '\n                     Something is WRONG in the "INFO_ElaStic" file.\n')

l3  = INFO.readline()
cod = l3.split()[-1]

l4  = INFO.readline()
SGN = int(l4.split()[-1])

l5  = INFO.readline()
V0  = float(l5.split()[-2])

l6  = INFO.readline()
mdr = float(l6.split()[-1])

l7  = INFO.readline()
NoP = int(l7.split()[-1])

INFO.close()
#--------------------------------------------------------------------------------------------------

#%%%--- Calculating the Space-Group Number and classifying it ---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if (1 <= SGN and SGN <= 2):      # Triclinic
    LC = 'N'
    if (ordr == 2): ECs = 21
    if (ordr == 3): ECs = 56  

elif(3 <= SGN and SGN <= 15):    # Monoclinic
    LC = 'M'
    if (ordr == 2): ECs = 13
    if (ordr == 3): ECs = 32 

elif(16 <= SGN and SGN <= 74):   # Orthorhombic
    LC = 'O'
    if (ordr == 2): ECs =  9
    if (ordr == 3): ECs = 20 

elif(75 <= SGN and SGN <= 88):   # Tetragonal II
    LC = 'TII'
    if (ordr == 2): ECs =  7
    if (ordr == 3): ECs = 16
  
elif(89 <= SGN and SGN <= 142):  # Tetragonal I
    LC = 'TI'
    if (ordr == 2): ECs =  6
    if (ordr == 3): ECs = 12  

elif(143 <= SGN and SGN <= 148): # Rhombohedral II 
    LC = 'RII'
    if (ordr == 2): ECs =  7
    if (ordr == 3): ECs = 20

elif(149 <= SGN and SGN <= 167): # Rhombohedral I
    LC = 'RI'
    if (ordr == 2): ECs =  6
    if (ordr == 3): ECs = 14

elif(168 <= SGN and SGN <= 176): # Hexagonal II
    LC = 'HII'
    if (ordr == 2): ECs =  5
    if (ordr == 3): ECs = 12

elif(177 <= SGN and SGN <= 194): # Hexagonal I
    LC = 'HI'
    if (ordr == 2): ECs =  5
    if (ordr == 3): ECs = 10

elif(195 <= SGN and SGN <= 206): # Cubic II
    LC = 'CII'
    if (ordr == 2): ECs =  3
    if (ordr == 3): ECs =  8

elif(207 <= SGN and SGN <= 230): # Cubic I
    LC = 'CI'
    if (ordr == 2): ECs = 3
    if (ordr == 3): ECs = 6

else: sys.exit('\n     ... Oops ERROR: WRONG Space-Group Number !?!?!?    \n')
if mthd == 'Energy':
#--------------------------------------------------------------------------------------------------
######################################### Enegy based calculations ################################
#%%%--- Reading the energies ---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    xmlf = open('Energy.xml', 'w')
    root = et.Element("Energy_Strain")
    
    for i in range(1, ECs+1):
        if (i<10):
            Dstn = 'Dst0'+ str(i)
        else: 
            Dstn = 'Dst' + str(i)
        if (os.path.exists(Dstn) == False):
            sys.exit('     ... Oops ERROR: Where is the '+ Dstn +' directory !?!?!?    \n')    
        os.chdir(Dstn)
    
        f = open(Dstn+'_Energy.dat', 'w')
        ##### xml-output #####
        selm = et.SubElement(root, Dstn)
        ######################
        for j in range(1, NoP+1):
            if (j<10):
                Dstn_num = Dstn +'_0'+str(j)
            else:
                Dstn_num = Dstn +'_' +str(j)
    
            if (os.path.exists(Dstn_num)): 
                os.chdir(Dstn_num)
    
                if (os.path.exists('vasprun.xml')):
                    print "Open vasp output file: " + os.getcwd() + '/vasprun.xml'
                    vaspout = et.parse('vasprun.xml')
                    elem = vaspout.xpath("//scstep[last()]/energy/i[@name = 'e_0_energy']")
                    energy = float(elem[0].text)
                    
    
                s = j-(NoP+1)/2
                r = 2*mdr*s/(NoP-1)
                if (s==0): r=0.0001
    
                if (r>0):
                    strain ='+%12.10f'%r
                else:
                    strain = '%13.10f'%r
                print >>f, strain,'   ', energy
                ##### xml-output ####
                entry = et.SubElement(selm, Dstn_num)
                entry.set('strain', str(strain))
                entry.set('energy', str(energy))
                entry.set('dst', str(i))
                entry.set('number', str(j))
                #####################
                os.chdir('../')
        f.close()
        
        os.chdir('../')
    xmlf.write(et.tostring(root, pretty_print=True))
    xmlf.close()
    #--------------------------------------------------------------------------------------------------
    
    warnings.simplefilter('ignore', np.RankWarning)
    
    #%%%--- Directory management ---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if (os.path.exists('Energy-vs-Strain_old')):
        shutil.rmtree( 'Energy-vs-Strain_old')   
    
    if (os.path.exists('Energy-vs-Strain')):
        os.rename(     'Energy-vs-Strain','Energy-vs-Strain_old')
    
    os.mkdir('Energy-vs-Strain')
    os.chdir('Energy-vs-Strain')
    
    os.system('cp -f ../Dst??/Dst??_Energy.dat .')
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
    ### --------------- Calculating the second derivative and Cross-Validation error -------------- ###
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
    CONV = cnvrtr * factorial(ordr)*2.
    
    for i in range(1, ECs+1):
        if (i<10):
            Dstn = 'Dst0'+str(i)
        else:
            Dstn = 'Dst' +str(i)
    
        if (ordr == 2):
            fD = open(Dstn+'_d2E.dat', 'w')
        if (ordr == 3):
            fD = open(Dstn+'_d3E.dat', 'w')
    
        fE = open(Dstn+'_CVe.dat', 'w')
        print >> fD, '# Max. eta    SUM(Cij) \n#'
        print >> fE, '# Max. eta    Cross-Validation error   \n#'
    
        for j in range(ordr+4, ordr-1, -2):
            if  (j == 2): nth = '2nd'
            elif(j == 3): nth = '3rd'
            else:
                nth = str(j) + 'th'
    
            print >> fD, '\n# '+ nth +' order fit.'
            print >> fE, '\n# '+ nth +' order fit.'
    
            # Reading the input files -----------------------------------------------------------------
            eta_ene= open(Dstn+'_Energy.dat', 'r')
    
            nl     = 0
            strain = []
            energy = []
            while (nl < NoP):
                line = eta_ene.readline()
                if (line == ''): break 
                line = line.strip().split()
                if (len(line) == 2): 
                    nl +=1
                    eta, ene = line
                    strain.append(float(eta))
                    energy.append(float(ene)) 
                elif (len(line) == 0): pass
                else:
                    sys.exit('\n     ... Oops ERROR: Strain and Energy are NOT defined correctly in "'+\
                             Dstn+'_Energy.dat" !?!?!?\n')
    
            eta_ene.close()
            strain, energy = sortlist(strain, energy)
            strain0 = copy.copy(strain)
            energy0 = copy.copy(energy)
    
           # ------------------------------------------------------------------------------------------
            while (len(strain) > j): 
                emax  = max(strain)
                emin  = min(strain)
                emax  = max(abs(emin),abs(emax))
                coeffs= polyfit(strain, energy, j)
                if (ordr == 2):
                    Cij  = coeffs[j-2]*CONV/V0         # in GPa unit 
                if (ordr == 3):
                    Cij  = coeffs[j-3]*CONV/V0 * 0.001 # in TPa unit
    
                print >>fD, '%13.10f'%emax, '%18.6f'%Cij
    
                if (abs(strain[0]+emax) < 1.e-7):
                    strain.pop(0); energy.pop(0)
                if (abs(strain[len(strain)-1]-emax) < 1.e-7):
                    strain.pop()
                    energy.pop()
    
            # Cross-Validation error calculations -----------------------------------------------------
            strain = copy.copy(strain0)
            energy = copy.copy(energy0)
            while (len(strain) > j+1): 
                emax = max(strain)
                emin = min(strain)
                emax = max(abs(emin),abs(emax))
    
                S = 0
                for k in range(len(strain)):
                    Y      = energy[k]
                    etatmp = []
                    enetmp = []
    
                    for l in range(len(strain)):
                        if (l==k): pass
                        else:            
                            etatmp.append(strain[l])
                            enetmp.append(energy[l])
    
                    Yfit = polyval(polyfit(etatmp,enetmp, j), strain[k])
                    S    = S + (Yfit-Y)**2
    
                CV = sqrt(S/len(strain))
                print >>fE, '%13.10f'%emax, CV
    
                if (abs(strain[0]+emax) < 1.e-7):
                    strain.pop(0)
                    energy.pop(0)
                if (abs(strain[len(strain)-1]-emax) < 1.e-7):
                    strain.pop()
                    energy.pop()
        fD.close()
        fE.close()
        
        # Plotting ------------------------------------------------------------------------------------
        if (os.path.exists('Grace.par') == False):
            os.system("ls $EXCITINGSCRIPTS")
            os.system("cp -fv /home/MCL/t.dengg/bin/exciting/excitingscripts/Grace.par .")
    	print os.getcwd()
    
        Gf    = open('Grace.par', 'r')
        Glines= Gf.readlines()
        Gf.close()
    
        TMP = []
        if (ordr == 2):
            for k in range(1, 45):
                TMP.append(Glines[k])
    
        if (ordr == 3):
            for k in range(48, 92):
                TMP.append(Glines[k])
    
        for k in range(164, 219):
            TMP.append(Glines[k])
    
        TMP.insert(99,'    s2 legend  " n = '+str(ordr+0)+'"\n')
        TMP.insert(91,'    s1 legend  " n = '+str(ordr+2)+'"\n')
        TMP.insert(83,'    s0 legend  " n = '+str(ordr+4)+'"\n')
        TMP.insert(46,'    subtitle "Plot for '+ Dstn +' deformation, n = Order of polynomial fit"\n')
    
        GdE = open(Dstn+'_d'+str(ordr)+'E.par', 'w')
        for l in range(len(TMP)):
            print >>GdE, TMP[l],
        GdE.close()
    
        os.system('xmgrace '+ Dstn +'_d'+str(ordr)+'E.dat -param '+Dstn+'_d'+str(ordr)+\
                  'E.par -saveall '+Dstn+'_d'+str(ordr)+'E.agr &')
    
        TMP = []
        for k in range(154, 162):
            TMP.append(Glines[k])
    
        for k in range(164, 219):
            TMP.append(Glines[k])
    
        TMP.insert(63,'    s2 legend  " n = '+str(ordr+0)+'"\n')
        TMP.insert(55,'    s1 legend  " n = '+str(ordr+2)+'"\n')
        TMP.insert(47,'    s0 legend  " n = '+str(ordr+4)+'"\n')
        TMP.insert(10,'    subtitle "Plot for '+ Dstn +' deformation, n = Order of polynomial fit"\n')
    
        CVe = open(Dstn+'_CVe.par', 'w')
        for k in range(len(TMP)):
            print >>CVe, TMP[k],
        CVe.close()
    
        os.system('xmgrace '+ Dstn +'_CVe.dat -param '+ Dstn +'_CVe.par -saveall '+ Dstn +'_CVe.agr &')
    
    os.chdir('../')
    
    # Writing the ElaStic_???.in file -----------------------------------------------------------------
    
    if (ordr == 2): orth  = '2nd'
    if (ordr == 3): orth  = '3rd'
    
    fri = open('ElaStic_'+ orth +'.in', 'w')            
    for i in range(1, ECs+1):
        if (i<10):
            Dstn = 'Dst0'+str(i)
        else:
            Dstn = 'Dst' +str(i)
        print >>fri, Dstn+'    eta_max    Fit_order'
    fri.close()
    #--------------------------------------------------------------------------------------------------
    os.system('rm -f Energy-vs-Strain/Grace.par')

if mthd == 'Stress':
#--------------------------------------------------------------------------------------------------
######################################## Stress based calculations ################################
#%%%--- Reading the stress ---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    xmlf = open('Stress.xml', 'w')
    root = et.Element("Stress_Strain")
    
    for i in range(1, ECs+1):
        if (i<10):
            Dstn = 'Dst0'+ str(i)
        else: 
            Dstn = 'Dst' + str(i)
        if (os.path.exists(Dstn) == False):
            sys.exit('     ... Oops ERROR: Where is the '+ Dstn +' directory !?!?!?    \n')    
        os.chdir(Dstn)
    
        f = open(Dstn+'_Stress.dat', 'w')
        ##### xml-output #####
        selm = et.SubElement(root, Dstn)
        ######################
        for j in range(1, NoP+1):
            if (j<10):
                Dstn_num = Dstn +'_0'+str(j)
            else:
                Dstn_num = Dstn +'_' +str(j)
    
            if (os.path.exists(Dstn_num)): 
                os.chdir(Dstn_num)
    
                if (os.path.exists('vasprun.xml')):
                    stress_m = []
                    print "Open vasp output file: " + os.getcwd() + '/vasprun.xml'
                    vaspout = et.parse('vasprun.xml')
                    stress_in = vaspout.xpath("//varray[@name = 'stress']/v")
                    for stress_i in stress_in: stress_m.append(map(float, (stress_i.text).split())) 
                    
    
                s = j-(NoP+1)/2
                r = 2*mdr*s/(NoP-1)
                if (s==0): r=0.0001
    
                if (r>0):
                    strain ='+%12.10f'%r
                else:
                    strain = '%13.10f'%r
                print >>f, strain,'   ', stress_m[i][j]
                ##### xml-output ####
                entry = et.SubElement(selm, Dstn_num)
                entry.set('strain', str(strain))
                entry.set('stress', str(stress_m[i][j]))
                entry.set('dst', str(i))
                entry.set('number', str(j))
                #####################
                os.chdir('../')
        f.close()
        
        os.chdir('../')
    xmlf.write(et.tostring(root, pretty_print=True))
    xmlf.close()
    #--------------------------------------------------------------------------------------------------
    
    warnings.simplefilter('ignore', np.RankWarning)
    
    #%%%--- Directory management ---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if (os.path.exists('Energy-vs-Strain_old')):
        shutil.rmtree( 'Energy-vs-Strain_old')   
    
    if (os.path.exists('Energy-vs-Strain')):
        os.rename(     'Energy-vs-Strain','Energy-vs-Strain_old')
    
    os.mkdir('Energy-vs-Strain')
    os.chdir('Energy-vs-Strain')
    
    os.system('cp -f ../Dst??/Dst??_Energy.dat .')
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
    ### --------------- Calculating the second derivative and Cross-Validation error -------------- ###
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
    CONV = cnvrtr * factorial(ordr)*2.
    
    for i in range(1, ECs+1):
        if (i<10):
            Dstn = 'Dst0'+str(i)
        else:
            Dstn = 'Dst' +str(i)
    
        if (ordr == 2):
            fD = open(Dstn+'_dSigma.dat', 'w')
        if (ordr == 3):
            fD = open(Dstn+'_d2Sigma.dat', 'w')
    
        fE = open(Dstn+'_CVs.dat', 'w')
        print >> fD, '# Max. eta    SUM(Cij) \n#'
        print >> fE, '# Max. eta    Cross-Validation error   \n#'
    
        for j in range(ordr+4, ordr-1, -2):
            if  (j == 1): nth = '2nd'
            elif(j == 2): nth = '3rd'
            else:
                nth = str(j) + 'th'
    
            print >> fD, '\n# '+ nth +' order fit.'
            print >> fE, '\n# '+ nth +' order fit.'
    
            # Reading the input files -----------------------------------------------------------------
            eta_ene= open(Dstn+'_Energy.dat', 'r')
    
            nl     = 0
            strain = []
            stress = []
            while (nl < NoP):
                line = eta_ene.readline()
                if (line == ''): break 
                line = line.strip().split()
                if (len(line) == 2): 
                    nl +=1
                    eta, ene = line
                    strain.append(float(eta))
                    stress.append(float(ene)) 
                elif (len(line) == 0): pass
                else:
                    sys.exit('\n     ... Oops ERROR: Strain and Energy are NOT defined correctly in "'+\
                             Dstn+'_Energy.dat" !?!?!?\n')
    
            eta_ene.close()
            strain, stress = sortlist(strain, stress)
            strain0 = copy.copy(strain)
            energy0 = copy.copy(stress)
    
           # ------------------------------------------------------------------------------------------
            while (len(strain) > j): 
                emax  = max(strain)
                emin  = min(strain)
                emax  = max(abs(emin),abs(emax))
                coeffs= polyfit(strain, stress, j)
                if (ordr == 1):
                    Cij  = coeffs[j-1]*CONV/V0         # in GPa unit 
                if (ordr == 2):
                    Cij  = coeffs[j-2]*CONV/V0 * 0.001 # in TPa unit
    
                print >>fD, '%13.10f'%emax, '%18.6f'%Cij
    
                if (abs(strain[0]+emax) < 1.e-7):
                    strain.pop(0); stress.pop(0)
                if (abs(strain[len(strain)-1]-emax) < 1.e-7):
                    strain.pop()
                    stress.pop()
    
            # Cross-Validation error calculations -----------------------------------------------------
            strain = copy.copy(strain0)
            stress = copy.copy(energy0)
            while (len(strain) > j+1): 
                emax = max(strain)
                emin = min(strain)
                emax = max(abs(emin),abs(emax))
    
                S = 0
                for k in range(len(strain)):
                    Y      = stress[k]
                    etatmp = []
                    enetmp = []
    
                    for l in range(len(strain)):
                        if (l==k): pass
                        else:            
                            etatmp.append(strain[l])
                            enetmp.append(stress[l])
    
                    Yfit = polyval(polyfit(etatmp,enetmp, j), strain[k])
                    S    = S + (Yfit-Y)**2
    
                CV = sqrt(S/len(strain))
                print >>fE, '%13.10f'%emax, CV
    
                if (abs(strain[0]+emax) < 1.e-7):
                    strain.pop(0)
                    stress.pop(0)
                if (abs(strain[len(strain)-1]-emax) < 1.e-7):
                    strain.pop()
                    stress.pop()
        fD.close()
        fE.close()
        
        # Plotting ------------------------------------------------------------------------------------
        if (os.path.exists('Grace.par') == False):
            os.system("ls $EXCITINGSCRIPTS")
            os.system("cp -fv /home/MCL/t.dengg/bin/exciting/excitingscripts/Grace.par .")
        print os.getcwd()
    
        Gf    = open('Grace.par', 'r')
        Glines= Gf.readlines()
        Gf.close()
    
        TMP = []
        if (ordr == 2):
            for k in range(1, 45):
                TMP.append(Glines[k])
    
        if (ordr == 3):
            for k in range(48, 92):
                TMP.append(Glines[k])
    
        for k in range(164, 219):
            TMP.append(Glines[k])
    
        TMP.insert(99,'    s2 legend  " n = '+str(ordr+0)+'"\n')
        TMP.insert(91,'    s1 legend  " n = '+str(ordr+2)+'"\n')
        TMP.insert(83,'    s0 legend  " n = '+str(ordr+4)+'"\n')
        TMP.insert(46,'    subtitle "Plot for '+ Dstn +' deformation, n = Order of polynomial fit"\n')
    
        GdE = open(Dstn+'_d'+str(ordr)+'E.par', 'w')
        for l in range(len(TMP)):
            print >>GdE, TMP[l],
        GdE.close()
    
        os.system('xmgrace '+ Dstn +'_d'+str(ordr)+'E.dat -param '+Dstn+'_d'+str(ordr)+\
                  'E.par -saveall '+Dstn+'_d'+str(ordr)+'E.agr &')
    
        TMP = []
        for k in range(154, 162):
            TMP.append(Glines[k])
    
        for k in range(164, 219):
            TMP.append(Glines[k])
    
        TMP.insert(63,'    s2 legend  " n = '+str(ordr+0)+'"\n')
        TMP.insert(55,'    s1 legend  " n = '+str(ordr+2)+'"\n')
        TMP.insert(47,'    s0 legend  " n = '+str(ordr+4)+'"\n')
        TMP.insert(10,'    subtitle "Plot for '+ Dstn +' deformation, n = Order of polynomial fit"\n')
    
        CVe = open(Dstn+'_CVe.par', 'w')
        for k in range(len(TMP)):
            print >>CVe, TMP[k],
        CVe.close()
    
        os.system('xmgrace '+ Dstn +'_CVe.dat -param '+ Dstn +'_CVe.par -saveall '+ Dstn +'_CVe.agr &')
    
    os.chdir('../')
    
    # Writing the ElaStic_???.in file -----------------------------------------------------------------
    
    if (ordr == 2): orth  = '2nd'
    if (ordr == 3): orth  = '3rd'
    
    fri = open('ElaStic_'+ orth +'.in', 'w')            
    for i in range(1, ECs+1):
        if (i<10):
            Dstn = 'Dst0'+str(i)
        else:
            Dstn = 'Dst' +str(i)
        print >>fri, Dstn+'    eta_max    Fit_order'
    fri.close()
    #--------------------------------------------------------------------------------------------------
    os.system('rm -f Energy-vs-Strain/Grace.par')
