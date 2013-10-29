#!/usr/bin/env python
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
#%%%--------------------------------- ElaStic@vasp-setup ----------------------------------%%%#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
#
# AUTHORS:
# Rostam Golesorkhtabar and Pasquale Pavone 
# r.golesorkhtabar@mcl.at
# (modified by Thomas Dengg) 
# DATE:
# Sun Jan 01 00:00:00 2012
#
# SYNTAX:
# python ElaStic@vasp-setup.py
#        ElaStic@vasp-setup
# 
# EXPLANATION:
# 
#__________________________________________________________________________________________________
print'\
\n     +-----------------------------------------------------------------+\
\n     |*****************************************************************|\
\n     |*                                                               *|\
\n     |*                WELCOME TO THE ElaStic@vasp                *|\
\n     |*        ElaStic Version 1.0.0, Release Date: 2012-01-01        *|\
\n     |*                                                               *|\
\n     |*****************************************************************|\
\n     +-----------------------------------------------------------------+'
#__________________________________________________________________________________________________

from lxml  import etree as ET
from sys   import stdin
from numpy import *
import numpy as np
import os.path
import shutil
import glob
import math
import sys
import os

import poscarToSgroup


#%%%--- DICTIONARIS ---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Ls_Dic={                       \
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

Ls_str={                                     \
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

LC_Dic = {              \
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
#--------------------------------------------------------------------------------------------------

#%%%--- Reading the method of the elastic constants calculations ---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#print '\n     Energy  ---=>  1    \
#       \n     Stress  ---=>  2    '
#num = input('>>>> Please choose the method of the calculation (choose 1 or 2): ')
#if (num != 1 and num != 2):
#    sys.exit("\n     ... Oops ERROR: Choose '1' or '2' \n")
#if (num == 1 ): mthd = 'Energy'
#if (num == 2 ): mthd = 'Stress'
mthd = 'Energy'
#--------------------------------------------------------------------------------------------------

#%%%--- Reading the order of the elastic constants ---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
print '\n     2nd  ---=>  2    \
       \n     3rd  ---=>  3    '
ordr = input('>>>> Please choose the order of the elastic constant (choose \'2\' or \'3\'): ')

if (ordr != 2 and ordr != 3 ):
    sys.exit("\n     ... Oops ERROR: Choose '2' or '3' \n")
#--------------------------------------------------------------------------------------------------

#%%%--- Checking the input file exist ---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
INF = raw_input('\n>>>> Please enter the vasp POSCAR file name: ')

if (os.path.exists(INF) == False):
    sys.exit('\n    ... Oops ERROR: There is NO file with "'+ INF +'" name !?!?!?    \n')
#--------------------------------------------------------------------------------------------------

o_poscar = poscarToSgroup.POS(INF)
poscar = o_poscar.read_pos() 				# Generate sgroup.out from POSCAR file                    ###MOD
o_poscar.write_sgroup(poscar)				# --"--
os.system('sgroup sgroup.in 1> sgroup.out 2> sgroup.err')
#%%%--- Calculate Space-group number and classify it ---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

os.system('rm -f sgroup.in ')

if (os.path.getsize('sgroup.err') != 0):
    fer  = open('sgroup.err', 'r')
    lines= fer.readlines()
    print '\n     ... Oops '+ lines[0]
    for i in range(1, len(lines)):
        print '                 '+ lines[i]
    fer.close()
    sys.exit()
else: os.system('rm -f sgroup.err')

SGf   = open('sgroup.out', 'r')
SGlins= SGf.readlines()
SGf.close()

for i in range(len(SGlins)):
    if (SGlins[i].find('Number and name of space group:') >= 0):
        SGN = int(float(SGlins[i].split()[6]))
        SGN_explanation=SGlins[i].strip()
        break

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
    if (ordr == 2): ECs =  3
    if (ordr == 3): ECs =  6
else: sys.exit('\n     ... Oops ERROR: WRONG Space-Group Number !?!?!?    \n')

if (ordr == 2): order = 'second'
if (ordr == 3): order = 'third'
print '\n     '+ SGN_explanation +'\
       \n     '+ LC_Dic[LC] +' structure in the Laue classification.\
       \n     This structure has '+ str(ECs) +' independent '+ order +'-order elastic constants.'
#--------------------------------------------------------------------------------------------------

#%%%--- Reading the maximum Lagrangian strain ---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if (mthd == 'Energy'):
    mdr = input('\n>>>> Please enter the maximum Lagrangian strain '\
                '\n     The suggested value is between 0.030 and 0.150: ')
if (mthd == 'Stress'):
    mdr = input('\n>>>> Please enter the maximum Lagrangian strain '\
                '\n     The suggested value is between 0.0010 and 0.0050: ')

if (1 < mdr or mdr < 0):
    sys.exit('\n     ... Oops ERROR: The maximum Lagrangian strain is out of range !!!!!!\n')

mdr = round(mdr, 3)
print '     The maximum Lagrangian strain is '+ str(mdr) + '\n'
#--------------------------------------------------------------------------------------------------

#%%%--- Reading the number of the distorted structures ---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
NoP = input('>>>> Please enter the number of the distorted structures [odd number > 4]: ')
NoP = int(abs(NoP))

if (NoP < 5):
    sys.exit('\n     ... Oops ERROR: The NUMBER of the distorted structures < 5 !!!!!!    \n')
if (99 < NoP):
    sys.exit('\n     ... Oops ERROR: The NUMBER of the distorted structures > 99 !!!!!!   \n')

if (NoP%2 == 0):
    NoP   += 1
print '     The number of the distorted structures is '+ str(NoP) + '\n'

ptn = int((NoP-1)/2)

if (mthd == 'Energy'): interval = 0.0001
if (mthd == 'Stress'): interval = 0.00001

if (mdr/ptn <= interval):
    sys.exit('     ... Oops ERROR: The interval of the strain values is < '+ str(interval) +\
           '\n                     Choose a larger maximum Lagrangian strain'\
           '\n                     or a less number of distorted structures.\n')
#--------------------------------------------------------------------------------------------------
"""
#%%%--- Reading the input file ---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
INOBJ= open(INF, 'r')
doc  = ET.parse(INOBJ)
root = doc.getroot()
#--------------------------------------------------------------------------------------------------

#%%-- Reading the scale, stretch, and base vectors from the input file and calculate the volume -%%
scale = map(float,doc.xpath('/input/structure/crystal/@scale'))
if (scale==[]):
    sys.exit('\n     ... Oops ERROR: There is NO scale in '+ INF +' file !?!?!?    \n')

stretchstr = doc.xpath('/input/structure/crystal/@stretch')
if (stretchstr==[]):
    stretch=[1.,1.,1.]
else: stretch=np.array(map(float,stretchstr[0].split()))

basevectsn = doc.xpath('//basevect/text()')
bv = []
for basevect in basevectsn:
    bv.append(map(float,basevect.split()))
"""
bv = [poscar["vlatt_1"],poscar["vlatt_2"],poscar["vlatt_3"]]
M_old= np.array(bv)
D    = np.linalg.det(M_old)
V0   = abs(poscar['scale']**3*D)
#--------------------------------------------------------------------------------------------------

#%%%--- Writing the INFO_ElaStic file ---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
INFO = open('INFO_ElaStic','w')
print >>INFO, 'Order of elastic constants      =', ordr         ,\
            '\nMethod of calculation           =', mthd         ,\
            '\nDFT code name                   = exciting'      ,\
            '\nSpace-group number              =', SGN          ,\
            '\nVolume of equilibrium unit cell =', V0, '[a.u^3]',\
            '\nMaximum Lagrangian strain       =', mdr          ,\
            '\nNumber of distorted structures  =', NoP
INFO.close
#--------------------------------------------------------------------------------------------------

#%%%--- Directory management ---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
OLDlist = glob.glob('Dst??_old')
for Dstn_old in OLDlist:
    shutil.rmtree(Dstn_old)

Dstlist = glob.glob('Dst??')
for Dstn in Dstlist:
    os.rename(Dstn, Dstn+'_old')

if (os.path.exists('Structures_exciting_old')):
    shutil.rmtree( 'Structures_exciting_old')

if (os.path.exists('Structures_exciting')):
    os.rename(     'Structures_exciting', 'Structures_exciting_old')
#--------------------------------------------------------------------------------------------------

if (mthd == 'Energy'):
    if (ordr == 2):
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

    if (ordr == 3):
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

if (mthd == 'Stress'):
    if (ordr == 2):
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

    if (ordr == 3):
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

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
###------------------------------------- Structures maker --------------------------------------###
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
fdis = open('Distorted_Parameters','w')
cont1= 0
for i in Lag_strain_list:
    Ls_list= Ls_Dic[i]

    cont1  = cont1 + 1
    if (cont1 < 10):
        Dstn = 'Dst0'+str(cont1)
    else:
        Dstn = 'Dst' +str(cont1)
    
    os.mkdir(Dstn)
    os.chdir(Dstn)

    print>>fdis, Dstn+', Lagrangian strain = ' + Ls_str[i]

    cont2 = 0
    for s in range(-ptn, ptn+1):
        r = mdr*s/ptn
        if (s==0):
            if (mthd == 'Energy'): r = 0.0001
            if (mthd == 'Stress'): r = 0.00001

        Ls = zeros(6)
        for i in range(6):
            Ls[i] = Ls_list[i]
        Lv = r*Ls
        # Lagrangian strain to physical strain (eta = eps + 0.5*eps*esp) --------------------------
        eta_matrix      = zeros((3,3))

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
        if (linalg.norm(eta_matrix) > 0.7):
            sys.exit('\n     ... Oops ERROR: Too large deformation!\n') 

        while( norm > 1.e-10 ):
            x          = eta_matrix - dot(eps_matrix, eps_matrix)/2.
            norm       = linalg.norm(x - eps_matrix)      
            eps_matrix = x

#--------------------------------------------------------------------------------------------------
        i_matrix   = array([[1., 0., 0.],
                            [0., 1., 0.], 
                            [0., 0., 1.]])
        def_matrix = i_matrix + eps_matrix
        M_new      = dot(M_old, def_matrix)

        cont2 = cont2 + 1
        if (cont2 < 10):
            Dstn_cont2 = Dstn+ '_0'+str(cont2)
        else:
            Dstn_cont2 = Dstn+ '_' +str(cont2)

        print>>fdis, Dstn_cont2 + ',  eta = ' + str(r)

        
        for j in range(3):
            bdummy = '%22.16f'%(M_new[j,0]) + '%22.16f'%(M_new[j,1]) + '%22.16f'%(M_new[j,2])+' '
            print>>fdis, 'V' + str(j+1) + ' --=> ' + bdummy
            poscar["vlatt_%s"%j] = [M_new[j,0],M_new[j,1],M_new[j,2]]
        print>>fdis

        os.mkdir(Dstn_cont2)
        os.chdir(Dstn_cont2)

        # Writing the structure file --------------------------------------------------------------
        fileName = Dstn_cont2 + 'POSCAR'             
        o_poscar.write_pos(poscar, fileName)
        #------------------------------------------------------------------------------------------
        os.chdir('../')
    os.chdir('../')
fdis.close()
os.system('mkdir Structures_vasp; cp Dst??/Dst??_??/Dst??_??POSCAR Structures_vasp/')
#--------------------------------------------------------------------------------------------------
