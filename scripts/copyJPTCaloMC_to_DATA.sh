#! /bin/bash
# [temporary] scrip to copy unchanges L1Res and JPT files
# usage
# ./copyL1Res_JPT.sh
#DATA
path_src=/afs/desy.de/user/k/karavdia/Downloads/L1L2L3_JPT_Calo_14June2017/
name_src=Summer16_03Feb2017_V1_MC
for path in Summer16_03Feb2017H_V4 Summer16_03Feb2017H_V5 Summer16_03Feb2017H_V6 Summer16_03Feb2017G_V4 Summer16_03Feb2017G_V5 Summer16_03Feb2017G_V6 Summer16_03Feb2017EF_V4 Summer16_03Feb2017EF_V5 Summer16_03Feb2017EF_V6 Summer16_03Feb2017BCD_V4 Summer16_03Feb2017BCD_V5 Summer16_03Feb2017BCD_V6
do
    #Calo and JPT jets
    #echo "path = " $path
    for file in L1FastJet_AK4Calo L1FastJet_AK4JPT L1JPTOffset_AK4JPT L2Relative_AK4Calo L2Relative_AK4JPT L3Absolute_AK4Calo L3Absolute_AK4JPT
    do
	cp ${path_src}/${name_src}_${file}.txt ${path}_DATA/${path}_DATA_${file}.txt
    done
done

echo "Done"
