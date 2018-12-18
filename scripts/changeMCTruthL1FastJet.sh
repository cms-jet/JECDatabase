#! /bin/bash
# Script to copy L1FastJet files to MC (DATA)
# usage
# ./changeMCTruthL1FastJet.sh L1FastJet_SOURCE L1FastJet_DESTINATION
# created by A.Karavdina
FROM=$1
TO=$2
#Jet collection

for jet_coll in AK4PF AK4PFchs AK8PF AK8PFchs 

do
#How it's called in files from MCTruth analyser
     Name_L1FastJet="Summer16_07Aug2017GH_V13_Data_L1FastJet_"$jet_coll".txt"

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
