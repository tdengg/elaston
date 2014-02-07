#!/usr/bin/env python
#%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%#
#%!%!% ---------------------------------- ElaStic_Analyze ---------------------------------- %!%!%#
#%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%#
# AUTHOR:
# Rostam Golesorkhtabar
# r.golesorkhtabar@gmail.com
# 
# DATE:
# Sun Jan 01 00:00:00 2012 
#
# SYNTAX:
# python ElaStic_Analyze.py
#        ElaStic_Analyze
# 
# EXPLANATION:
# 
#__________________________________________________________________________________________________

import sys
import os

#%!%!%--- Checking the "INFO_ElaStic" file exist ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%
if (os.path.exists('INFO_ElaStic') == False):
    sys.exit('\n.... Oops ERROR: Where is the "INFO_ElaStic" file !?!?!?    \n')
#--------------------------------------------------------------------------------------------------

#%!%!%--- Reading the "INFO_ElaStic" file ---%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!
INFO=open('INFO_ElaStic', 'r')

l1  = INFO.readline()
ordr= int(l1.split()[-1])

if (ordr != 2 and ordr != 3):
    sys.exit('\n.... Oops ERROR: The order of the elastic constant is NOT clear !?!?!?'\
             '\n                 Something is WRONG in the "INFO_ElaStic" file.\n')

l2  = INFO.readline()
mthd= l2.split()[-1]

if (mthd != 'Stress' and mthd != 'Energy'):
    sys.exit('\n.... Oops ERROR: The method of the calculation is NOT clear !?!?!?'\
             '\n                 Something is WRONG in the "INFO_ElaStic" file.\n')

INFO.close()
#--------------------------------------------------------------------------------------------------

if (mthd == 'Energy'): import ElaStic_Analyze_Energy
if (mthd == 'Stress'): import ElaStic_Analyze_Stress
