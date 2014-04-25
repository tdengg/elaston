import sys
import vaspIO
import os


class Sgroup(object):
    def __init__(self, poscar):
        self.i = 0
        self.__sgn = None
        self.poscar = poscar
        self.set_sgroup()
        
    def set_sgroup(self):
        
        o_poscar = vaspIO.POS('POSCAR')
        o_poscar.write_sgroup(self.poscar)                # --"--
        os.system('sgroup sgroup.in 1> sgroup.out 2> sgroup.err')
        #%%%--- Calculate Space-group number and classify it ---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        os.system('less sgroup.in ')
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
        self.__sgn = SGN
    
    def get_sgroup(self):
        return self.__sgn
        
    sgn = property(fget=get_sgroup, fset=set_sgroup) 