import poscarToSgroup as vread
import os
import json
import copy

def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def gen_subdirs(fileName, par, val, dict):
    files = ['POSCAR','INCAR','KPOINTS','POTCAR']
    for v in val:
        print "mkdir " + par + "_" + str(v)
        os.system("mkdir " + par.strip() + "_" + str(v))
        for f in files:
            if f != fileName: os.system("cp %s"%f + " %s"%par.strip() + "_%s"%v)
        temp = copy.deepcopy(dict)
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
    

