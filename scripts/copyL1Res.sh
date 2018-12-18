#! /bin/bash
# script to copy new L1Res files
# usage
# ./copyL1Res.sh
# created by A.Karavdina

#DATA
path_in=~/JEC_tmp/L1Res/2016/Summer16_07Aug2017_AK8/Summer16_07Aug2017_AK8/
path_out=/nfs/dust/cms/user/karavdia/JECDatabase/textFiles/Summer16_07Aug2017
prefix=Summer16_07Aug2017
version=V9 #destination
for period in BCD EF GH

do
    for jet in AK4 AK8 
    do
	for corr in L1FastJet_${jet}PFchs L1FastJet_${jet}PF
	do 
	    cp ${path_in}/${period}/${prefix}${period}_Data_${corr}.txt ${path_out}${period}_${version}_DATA/${prefix}${period}_${version}_DATA_${corr}.txt  
	    echo ${path_out}${period}_${version}_DATA/${prefix}${period}_${version}_DATA_${corr}.txt   
 
	    diff ${path_out}${period}_${version}_DATA/${prefix}${period}_${version}_DATA_${corr}.txt ${path_in}/${period}/${prefix}${period}_Data_${corr}.txt
	done
    done
done

echo "Done"
