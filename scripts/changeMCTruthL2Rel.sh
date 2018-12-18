#! /bin/bash
# Script to copy L2Relative files to MC (DATA)
# usage
# ./changeMCTruthL2Rel.sh L2Rel_SOURCE_DIR L2Rel_DESTINATION_DIR
# created by A.Karavdina
FROM=$1
TO=$2
#Jet collection
for jet_coll in AK4PF AK4PFchs AK4PFPuppi AK8PF AK8PFchs AK8PFPuppi 

do
#How it's called in files from MCTruth analyser
    Name_L2Rel="bias2SelectionPow_25nsV1_MC_L2Relative_"$jet_coll".txt"
    
#How it should be called
    Name_L2Rel_official=${TO}_L2Relative_$jet_coll".txt"

#tar -zxvf ${FROM}.tar.gz
    f=${FROM}
    t=${TO}

    echo "Cloning $f to $t"
    echo "File name $f/$Name_L2Rel"
# #cp -r $f $t
    cp $f/${Name_L2Rel} $t/${Name_L2Rel_official}

    echo "Check the file: "$t/${Name_L2Rel_official}
    echo "Done"
done
