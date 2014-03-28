import os
import sys
import lxml.etree as et


root = os.getcwd()

dlist = sorted(os.listdir('.'))
dirlist = []
for i in dlist:
    if 'scale' in i: dirlist.append(i)
    
print dirlist
index = 0
for dir in dirlist:
    if os.path.isdir(dir) and 'scale' in dir:
        
        
        os.chdir(dir)
        if not os.path.exists('Dst03'):
            os.system('mv Dst02 Dst03')
            os.system('mv Dst01 Dst02')
        os.system('mkdir Dst01')
        
        dlist2 = sorted(os.listdir('.'))
        dirlist2 = []
        for i in dlist2:
            if 'Dst' in i: dirlist2.append(i)
            
        for dir2 in dirlist2:
            if os.path.isdir(dir2) and 'Dst' in dir2:
                
                os.chdir(dir2)
                dirname = os.path.basename(os.getcwd())
                
                if dirname == 'Dst01':
                    for i in range(21):
                        if i<9: 
                            os.system('mkdir Dst01_0%s'%str(i+1))
                        else: 
                            os.system('mkdir Dst01_%s'%str(i+1))
                            
                dlist3 = sorted(os.listdir('.'))
                print dlist3
                dirlist3 = []
                for i in dlist3:
                    if 'Dst' in i: dirlist3.append(i)
                print dirlist3    
                j=0
                for dir3 in dirlist3:
                    if os.path.isdir(dir3) and 'Dst' in dir3:
                        
                        if dirname == 'Dst01':
                            os.chdir(dir3)
                            if os.path.isfile(root+'/'+dirlist[index-10+j]+'/F_TV'):
                                os.system('cp '+root+'/%s/F_TV .'%dirlist[index-10+j])
                                os.system('cp '+root+'/%s/vasprun.xml .'%dirlist[index-10+j])
                                print 'cp '+root+'/%s/F_TV .'%dirlist[index-10+j]
                                
                            else:
                                #print 'cp '+root+'/%s/F_TV .'%dirlist[index-10+j]
                                print 'F_TV not found'
                            os.chdir('..')
                        else:
                            if not dir3 == dirname+'_0'+str(j+1):
                                if j<9: os.system('mv '+dir3+' '+dirname+'_0'+str(j+1))
                                else: os.system('mv '+dir3+' '+dirname+'_'+str(j+1))
                            
                        j+=1
                        
                        
                        ###########################################################
                        
                        ###########################################################
                        
                os.chdir('..')
        index+=1        
        os.chdir('..')
