import os
import lxml.etree as et
workdir = os.getcwd()
import search_vasprun
os.chdir(workdir)

search_vasprun.SearchDir(["POSCAR"],"./", True)

tree = et.parse('calc_filelist.xml')
paths = tree.xpath('//dir/@path')
calchome = os.getcwd()
for path in paths:
    os.chdir(path)
    
    os.system('$VASPHOME/vasp.5.3/vasp')
    os.chdir(calchome)