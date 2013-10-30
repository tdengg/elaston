import vaspIO as vread
import os
import json
import copy
import sys
try:
    if sys.argv[1] == 'elastic':
        import ElaStic_vasp_setup
        elastic = True
    else: elastic = False
except:
    print 'Setting up directory structure for parameter convergence....'

def convert(inpt):
    if isinstance(inpt, dict):
        return {convert(key): convert(value) for key, value in inpt.iteritems()}
    elif isinstance(inpt, list):
        return [convert(element) for element in inpt]
    elif isinstance(inpt, unicode):
        return inpt.encode('utf-8')
    else:
        return inpt

def gen_subdirs(fileName, par, val, dic):
    files = ['POSCAR','INCAR','KPOINTS','POTCAR']
    for v in val:
        print "mkdir " + par + "_" + str(v)
        os.system("mkdir " + par.strip() + "_" + str(v))
        for f in files:
            if f != fileName: os.system("cp %s"%f + " %s"%par.strip() + "_%s"%v)
        temp = copy.deepcopy(dic)
        temp[par] = v
        
        if fileName == 'INCAR': vread.POS('INCAR').write_in(temp, "%s"%par.strip() + "_%s"%v + '/' +fileName)
        if fileName == 'POSCAR': vread.POS('POSCAR').write_pos(temp, "%s"%par.strip() + "_%s"%v + '/' +fileName)



o_poscar = vread.POS('POSCAR')
poscar = o_poscar.read_pos()

if type(convert(json.loads(str(poscar['scale'])))) == list:
    poscar['scale'] = convert(json.loads(str(poscar['scale'])))
    gen_subdirs('POSCAR','scale',poscar['scale'],poscar)
    

o_incar = vread.POS('INCAR')
incar = o_incar.read_in()

for par in incar.keys():
    if incar[par].startswith('[') and type(convert(json.loads(incar[par]))) == list: 
        incar[par] = convert(json.loads(incar[par]))
        gen_subdirs('INCAR', par,incar[par],incar)
        if elastic:
            for v in incar[par]:
                os.chdir("%s"%par.strip() + "_%s"%v)
                ElaStic_vasp_setup.SETUP()
                os.chdir("..")
