#!/bin/bash



number=1

if [ "$1" = "i" ]; then
	while [ $number -lt 19 ]; do
	
    		cp ./ElaStic_2nd.in $number
    	
    		number=$((number + 1))
	done
fi

if [ "$1" = "a" ]; then
	while [ $number -lt 19 ]; do
    		cd $number
		ElaStic@exciting-analyze.py
		cd ..
    	
    		number=$((number + 1))
	done
fi

if [ "$1" = "r" ]; then
	while [ $number -lt 19 ]; do
    		cd $number
		ElaStic@exciting-result.py
		cd ..
    	
    		number=$((number + 1))
	done
fi
       
if [ "$1" = "grep" ]; then
	while [ $number -lt 19 ]; do
    		cd $number
		grep 'Voigt Young' ElaStic_2nd.out >> ../young.out
		cd ..
    	
    		number=$((number + 1))
	done
fi
