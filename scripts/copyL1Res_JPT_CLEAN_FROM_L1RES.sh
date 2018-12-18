#! /bin/bash
# [temporary] scrip to copy unchanges L1Res and JPT files
# usage
# ./copyL1Res_JPT.sh
# created by A.Karavdina
#DATA
for path in Summer16_23Sep2016BCD Summer16_23Sep2016EF Summer16_23Sep2016G Summer16_23Sep2016H
do
    #Calo and JPT jets
    #echo "path = " $path
    # for file in L1FastJet_AK4Calo L1FastJet_AK4JPT L1JPTOffset_AK4JPT L2L3Residual_AK4Calo L2L3Residual_AK4JPT L2Relative_AK4Calo L2Relative_AK4JPT L2Residual_AK4Calo L2Residual_AK4JPT L3Absolute_AK4Calo L3Absolute_AK4JPT 
    for file in Uncertainty_AK4Calo Uncertainty_AK4JPT UncertaintySources_AK4Calo UncertaintySources_AK4JPT
    do
	cp ${path}V4_DATA/${path}V4_DATA_${file}.txt ${path}V5_DATA/${path}V5_DATA_${file}.txt
    done

    for file in L1FastJet_AK4PFchs L1FastJet_AK4PFPuppi L1FastJet_AK4PF L1FastJet_AK8PFchs L1FastJet_AK8PFPuppi L1FastJet_AK8PF
       cp ${path}V6_MC/${path}V6_MC_${file}.txt ${path}V7_DATA/${path}V7_DATA_${file}.txt
    done
done

#MC

#L1Res output: L1RC
pathMC=Summer16_23Sep2016
#for file in L1RC_AK4PFchs L1RC_AK4PF L1RC_AK8PFchs L1RC_AK8PF
for file in UncertaintySources_AK4Calo UncertaintySources_AK4JPT Uncertainty_AK4Calo Uncertainty_AK4JPT
do
    cp ${pathMC}V4_MC/${pathMC}V4_MC_${file}.txt ${pathMC}V5_MC/${pathMC}V5_MC_${file}.txt
done


echo "Done"
