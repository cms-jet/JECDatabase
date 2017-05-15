#! /bin/bash
# script to copy new L1Res files
# usage
# ./copyL1Res.sh

#DATA
path_in=/nfs/dust/cms/user/karavdia/Summer16_03Feb2017_V0_L1Res/up_Summer16_23Sep2016V8/Run
path_out=/afs/desy.de/user/k/karavdia/JECDatabase/textFiles/Summer16_03Feb2017
for period in BCD EF G H 
do
    for jet in AK4 AK8 
    do
	for corr in L1FastJet_${jet}PFchs L1FastJet_${jet}PF L1RC_${jet}PFchs L1RC_${jet}PF 
	do 
	    cp ${path_in}${period}/${jet}/Summer16_23Sep2016${period}V8_DATA_${corr}.txt ${path_out}${period}_V0_DATA/Summer16_03Feb2017${period}_V0_DATA_${corr}.txt  
	    echo ${path_out}${period}_V0_DATA/Summer16_03Feb2017${period}_V0_DATA_${corr}.txt    
	done
    done
done

#For RunH bug in the naming
for period in H
do
    for jet in AK4 
    do
	for corr in L1FastJet_${jet}PFchs L1FastJet_${jet}PF L1RC_${jet}PFchs L1RC_${jet}PF  
	do
	    cp ${path_in}${period}/${jet}/Summer16_23Sep2016V${period}8_DATA_${corr}.txt ${path_out}${period}_V0_DATA/Summer16_03Feb2017${period}_V0_DATA_${corr}.txt 
	    echo ${path_out}${period}_V0_DATA/Summer16_03Feb2017${period}_V0_DATA_${corr}.txt    
	done
    done
done

echo "Done"
