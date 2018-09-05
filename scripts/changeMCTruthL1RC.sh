#! /bin/bash
# Script to copy L1RC files to MC (DATA)
# usage
# ./changeMCTruthL1RC.sh L1RC_SOURCE L1RC_DESTINATION
FROM=$1
TO=$2
#Jet collection
#jet_coll="AK4PFchs"
#jet_coll="AK4PFPuppi"
#jet_coll="AK4PF"


#for jet_coll in AK4PF AK4PFchs AK4PFPuppi AK8PF AK8PFchs AK8PFPuppi 
for jet_coll in AK4PF AK4PFchs AK8PF AK8PFchs 
#for jet_coll in AK4PF AK4PFchs
do
#How it's called in files from MCTruth analyser
    Name_L1FastJet="Fall17_17Nov2017F_V22_DATA_L1RC_"$jet_coll".txt"
 #     Name_L1FastJet="Fall17_25nsV1_MC_L1RC_"$jet_coll".txt"
#    Name_L1FastJet="Summer16_07Aug2017GH_V13_DATA_L1RC_"$jet_coll".txt"
#     Name_L1FastJet="Fall17_17Nov2017F_V22_DATA_L1RC_"$jet_coll".txt"

    
#How it should be called
    Name_L1FastJet_official=${TO}_L1RC_$jet_coll".txt"

#tar -zxvf ${FROM}.tar.gz
    f=${FROM}
    t=${TO}

    echo "Cloning $f to $t"
    echo "File name $f/$Name_L1RC"
# #cp -r $f $t
    cp $f/${Name_L1FastJet} $t/${Name_L1FastJet_official}

    echo "Check the file: "$t/${Name_L1FastJet_official}
    echo "Done"
done
