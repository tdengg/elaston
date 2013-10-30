import os
import search_dir
import lxml.etree as et
print os.system("pwd")

search_dir.SearchDir(["POSCAR"],"./", True)

tree = et.parse('conv_ngrid/calc_filelist.xml')
paths = tree.xpath('//dir/@path')
calchome = os.getcwd()
for path in paths:
    os.chdir(path)
    os.system('$VASPHOME/vasp.5.3/vasp')
    os.chdir(calchome)