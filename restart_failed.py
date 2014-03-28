import lxml.etree as et
import os

dirlist = os.listdir('.')
ersum = 0
calcsum = 0
for dir in dirlist:
    if os.path.isdir(dir) and 'scale' in dir:
        
        
        os.chdir(dir)
        dirlist2 = os.listdir('.')
        for dir2 in dirlist2:
            if os.path.isdir(dir2) and 'Dst' in dir2:
                
                os.chdir(dir2)
                dirlist3 = os.listdir('.')
                for dir3 in dirlist3:
                    if os.path.isdir(dir3) and 'Dst' in dir3:
                        
                        os.chdir(dir3)
                        ###########################################################
                        try:
                            tree = et.parse('vasprun.xml')
                            tree.xpath("//scstep[last()]/energy/i[@name = 'e_fr_energy']")
                            print 'OK'
                        except:
                            #os.system('cp ../../../job_W.sh .')
                            print 'recalculating: ',os.getcwd()
                            os.system('~/bin/vasp_rom/vasp.5.3/vasp')
                            
                            #os.system('qsub job_W.sh')
                        ###########################################################
                        os.chdir('..')
                os.chdir('..')
                
        os.chdir('..')
