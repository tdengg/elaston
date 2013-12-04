#!/bin/bash
#
EXECUTABLE=$VASPHOME/vasp.5.3/vasp

label=`ls -d Dst??`
for Dstn in $label ; do
    cd $Dstn
    Dstn_num_list=`ls -d ${Dstn}_??`
    for Dstn_num in $Dstn_num_list ; do
        cd $Dstn_num/
        cp -f $Dstn_num POSCAR
	cp ../../POTCAR .
	cp ../../KPOINTS .
	cp ../../INCAR .
        echo
        echo '        +--------------------------------------+'
        echo '        | SCF calculation of "'${Dstn_num}'" starts |'
        echo '        +--------------------------------------+'
        time $EXECUTABLE | tee output.screen
        date
        cd ../
    done
    cd ../
done
