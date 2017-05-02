#! /bin/bash
# [temporary] scrip to copy unchanges L1Res and JPT files
# usage
# ./copyL1Res_JPT.sh
#DATA
for path in Summer16_23Sep2016BCD Summer16_23Sep2016EF Summer16_23Sep2016G Summer16_23Sep2016H
do
    for file in Uncertainty_AK4PFchs Uncertainty_AK4PFPuppi Uncertainty_AK4PF Uncertainty_AK8PFchs Uncertainty_AK8PFPuppi Uncertainty_AK8PF UncertaintySources_AK4PFchs UncertaintySources_AK4PFPuppi UncertaintySources_AK4PF UncertaintySources_AK8PFchs UncertaintySources_AK8PFPuppi UncertaintySources_AK8PF
    do
	cp ${path}V4_DATA/${path}V4_DATA_${file}.txt ${path}V5_DATA/${path}V5_DATA_${file}.txt
    done
done

#MC

#L1Res output: L1RC
pathMC=Summer16_23Sep2016
for file in Uncertainty_AK4PFchs Uncertainty_AK4PFPuppi Uncertainty_AK4PF Uncertainty_AK8PFchs Uncertainty_AK8PFPuppi Uncertainty_AK8PF UncertaintySources_AK4PFchs UncertaintySources_AK4PFPuppi UncertaintySources_AK4PF UncertaintySources_AK8PFchs UncertaintySources_AK8PFPuppi UncertaintySources_AK8PF
do
    cp ${pathMC}V4_MC/${pathMC}V4_MC_${file}.txt ${pathMC}V5_MC/${pathMC}V5_MC_${file}.txt
done
echo "Done"
