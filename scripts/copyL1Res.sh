#! /bin/bash
# script to copy new L1Res files
# usage
# ./copyL1Res.sh

#DATA
path_in=~/JEC_tmp/L1Res/Fall17_17Nov2017_V1/Fall17_17Nov2017_V1/
path_out=/afs/desy.de/user/k/karavdia/JECDatabase/textFiles/Fall17_17Nov2017
for period in B C D E F
#for period in B
do
    for jet in AK4 AK8 
    do
	for corr in L1FastJet_${jet}PFchs L1FastJet_${jet}PF L1RC_${jet}PFchs L1RC_${jet}PF 
	do 
	    cp ${path_in}/${jet}/Run${period}/Fall17_17Nov2017${period}_V1_DATA_${corr}.txt ${path_out}${period}_V3_DATA/Fall17_17Nov2017${period}_V3_DATA_${corr}.txt  
	    echo ${path_out}${period}_V3_DATA/Fall17_17Nov2017${period}_V3_DATA_${corr}.txt   
 
	    diff ${path_out}${period}_V3_DATA/Fall17_17Nov2017${period}_V3_DATA_${corr}.txt ${path_in}/${jet}/Run${period}/Fall17_17Nov2017${period}_V1_DATA_${corr}.txt
	done
    done
done

# #For RunH bug in the naming
# for period in H
# do
#     for jet in AK4 
#     do
# 	for corr in L1FastJet_${jet}PFchs L1FastJet_${jet}PF L1RC_${jet}PFchs L1RC_${jet}PF  
# 	do
# 	    cp ${path_in}${period}/${jet}/Fall17_17Nov2017V${period}8_DATA_${corr}.txt ${path_out}${period}_V0_DATA/Summer16_03Feb2017${period}_V0_DATA_${corr}.txt 
# 	    echo ${path_out}${period}_V0_DATA/Summer16_03Feb2017${period}_V0_DATA_${corr}.txt    
# 	done
#     done
# done

echo "Done"
