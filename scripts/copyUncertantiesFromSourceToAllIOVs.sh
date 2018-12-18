#! /bin/bash
# scrip to copy uncertainty and uncertainty sources from the source file to all IOVs (data) and all jet collections (for the moment uncertainty estimated for AK4CHS only)
# usage
# ./copyUncertantiesFromSourceToAllIOVs.sh
# created by A.Karavdina

#Some local path with txt files
source_path=/afs/cern.ch/user/k/kirschen/public/forJERC/SystUncertWorkInProgress/Fall17_17Nov2017_V31_Uncertainties_V1/
source_uncer_name=Fall17_07Nov2017_V31_DATA_Uncertainty_AK4PFchs.txt
source_uncer_source_name=Fall17_07Nov2017_V31_DATA_UncertaintySources_AK4PFchs.txt

# #DATA
# #Change the JEC version here!
for path in Fall17_09May2018F_V3
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

# #MC
for path in Fall17_17Nov2017_V32
do
     for file in Uncertainty_AK4PFchs Uncertainty_AK4PFPuppi Uncertainty_AK4PF Uncertainty_AK8PFchs Uncertainty_AK8PFPuppi Uncertainty_AK8PF 
    do
	cp ${source_path}/${source_uncer_name} ${path}_MC/${path}_MC_${file}.txt
     done
    for file in UncertaintySources_AK4PFchs UncertaintySources_AK4PFPuppi UncertaintySources_AK4PF UncertaintySources_AK8PFchs UncertaintySources_AK8PFPuppi UncertaintySources_AK8PF 
    do
	cp ${source_path}/${source_uncer_source_name} ${path}_MC/${path}_MC_${file}.txt
    done
done

echo "Done"
