#! /bin/bash
# Script to copy L1FastJet files to MC (DATA)
# usage
# ./changeMCTruthL1FastJet.sh L1FastJet_SOURCE L1FastJet_DESTINATION
FROM=$1
TO=$2
#Jet collection
#jet_coll="AK4PFchs"
#jet_coll="AK4PFPuppi"
#jet_coll="AK4PF"


#for jet_coll in AK4PF AK4PFchs AK4PFPuppi AK8PF AK8PFchs AK8PFPuppi 
for jet_coll in AK4PF AK4PFchs AK8PF AK8PFchs 
do
#How it's called in files from MCTruth analyser
     Name_L1FastJet="Fall17_25nsV1_MC_L1FastJet_"$jet_coll".txt"
#    Name_L1FastJet="Summer18_25nsV1_MC_L1FastJet_"$jet_coll".txt"
#    Name_L1FastJet="bias2SelectionPow_25nsV1_MC_L1FastJet_"$jet_coll".txt"
    
#How it should be called
    Name_L1FastJet_official=${TO}_L1FastJet_$jet_coll".txt"

#tar -zxvf ${FROM}.tar.gz
    f=${FROM}
    t=${TO}

    echo "Cloning $f to $t"
    echo "File name $f/$Name_L1FastJet"
# #cp -r $f $t
    cp $f/${Name_L1FastJet} $t/${Name_L1FastJet_official}

    echo "Check the file: "$t/${Name_L1FastJet_official}
    echo "Done"
done
