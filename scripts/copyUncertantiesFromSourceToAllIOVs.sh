#! /bin/bash
# [temporary] scrip to copy uncertainty and uncertainty sources from the source file to all IOVs (data) and all jet collections (for the moment uncertainty estimated for AK4CHS only)
# usage
# ./copyUncertantiesFromSourceToAllIOVs.sh

#Some local path with txt files
source_path=/afs/cern.ch/user/k/kirschen/public/
source_uncer_name=Fall17_07Nov2017_V6M_DATA_UncertaintySources_AK4PFchs.txt
source_uncer_source_name=Fall17_07Nov2017_V6M_DATA_UncertaintySources_AK4PFchs.txt

#Change the JEC version here!
for path in Fall17_17Nov2017B_V6 Fall17_17Nov2017C_V6 Fall17_17Nov2017D_V6 Fall17_17Nov2017E_V6 Fall17_17Nov2017F_V6
do
     for file in Uncertainty_AK4PFchs Uncertainty_AK4PFPuppi Uncertainty_AK4PF Uncertainty_AK8PFchs Uncertainty_AK8PFPuppi Uncertainty_AK8PF 
    do
	cp ${source_path}/${source_uncer_name} ${path}_DATA/${path}_DATA_${file}.txt
     done
       for file in UncertaintySources_AK4PFchs UncertaintySources_AK4PFPuppi UncertaintySources_AK4PF UncertaintySources_AK8PFchs UncertaintySources_AK8PFPuppi UncertaintySources_AK8PF 
    do
	cp ${source_path}/${source_uncer_source_name} ${path}_DATA/${path}_DATA_${file}.txt
    done
done

#MC

# #L1Res output: L1RC
# pathMC=Summer16_23Sep2016
# for file in Uncertainty_AK4PFchs Uncertainty_AK4PFPuppi Uncertainty_AK4PF Uncertainty_AK8PFchs Uncertainty_AK8PFPuppi Uncertainty_AK8PF UncertaintySources_AK4PFchs UncertaintySources_AK4PFPuppi UncertaintySources_AK4PF UncertaintySources_AK8PFchs UncertaintySources_AK8PFPuppi UncertaintySources_AK8PF
# do
#     cp ${pathMC}V4_MC/${pathMC}V4_MC_${file}.txt ${pathMC}V5_MC/${pathMC}V5_MC_${file}.txt
# done
echo "Done"
