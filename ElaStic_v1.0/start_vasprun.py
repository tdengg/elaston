import os
import lxml.etree as et
workdir = os.getcwd()
import search_vasprun
os.chdir(workdir)
print os.getcwd()+'/'
search_vasprun.SearchDir(['vasprun.xml'],workdir+'/', True)
os.chdir(workdir)
print os.getcwd()
tree = et.parse(workdir+'/calc_filelist.xml')
paths = tree.xpath('//dir/@path')
calchome = workdir
for path in paths:
    os.chdir(path)
    
    os.system('$VASPHOME/vasp.5.3/vasp')
    os.chdir(calchome)