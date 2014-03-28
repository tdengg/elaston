#!/usr/bin/env python
#%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%#
#%!%!% ----------------------------------- ElaStic_Setup ----------------------------------- %!%!%#
#%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%!%#
#
# AUTHOR:
# Rostam Golesorkhtabar
# r.golesorkhtabar@gmail.com
# 
# DATE: 
# Sun Jan 01 00:00:00 2012
#
# SYNTAX:
# python ElaStic_Setup.py
#        ElaStic_Setup
# 
# EXPLANATION:
# 
#__________________________________________________________________________________________________

import sys
import os
print'\
\n     +-----------------------------------------------------------------+\
\n     |*****************************************************************|\
\n     |*                                                               *|\
\n     |*                  WELCOME TO THE ElaStic CODE                  *|\
\n     |*        ElaStic Version 1.0.0, Release Date: 2012-01-01        *|\
\n     |*                                                               *|\
\n     |*****************************************************************|\
\n     +-----------------------------------------------------------------+'

print '\
\n     Which DFT code would you like to apply for the calculations? \
\n     exciting  ---------=>  1                                     \
\n     WIEN2k    ---------=>  2                                     \
\n     Quantum ESPRESSO --=>  3                                     \
\n     VASP      ---------=>  4'

#num = input('>>>> Please choose (1, 2, 3 or 4): ')
num = 4
if (num != 1 and num != 2 and num != 3 and num !=4 ):
    sys.exit('\n.... Oops ERROR: Choose 1, 2, 3, or 4 \n')

if (num == 1): cod = 'exciting'
if (num == 2): cod = 'WIEN2k'
if (num == 3): cod = 'ESPRESSO'
if (num == 4): cod = 'VASP'

if (cod == 'exciting'): os.system('ElaStic_Setup_exciting'   )
if (cod == 'WIEN2k'  ): os.system('ElaStic_Setup_WIEN2k'     )
if (cod == 'ESPRESSO'): os.system('ElaStic_Setup_ESPRESSO'   )
if (cod == 'VASP'    ): 
    import ElaStic_Setup_VASP
    ElaStic_Setup_VASP.SETUP()