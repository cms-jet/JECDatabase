prefix=Summer19UL16
version=V5_MC
data=V5_DATA

#cp -a Summer19UL16APV_RunBCD_V5_DATA Summer19UL16APV_RunBCD_V6_DATA
#cp -a Summer19UL16APV_RunEF_V5_DATA Summer19UL16APV_RunEF_V6_DATA
#cp -a Summer19UL16APV_RunBCDEF_V5_DATA Summer19UL16APV_RunBCDEF_V6_DATA
#cp -a Summer19UL16_RunFGH_V5_DATA Summer19UL16_RunFGH_V6_DATA
#rename s/V5/V6/g Summer19UL16*_Run*_V6_DATA/*

for iov in APV_RunBCD APV_RunEF APV_RunBCDEF _RunFGH
do
  if [[ $iov == *"APV"* ]]; then
    echo "mc=APV_${version}"
    mc=APV_${version}
  else
    echo "mc=_${version}"
    mc=_${version}
  fi
  echo "cd ~/hip/JECDatabase/textFiles/${prefix}${iov}_${data}"
  cd ~/hip/JECDatabase/textFiles/${prefix}${iov}_${data}
  echo "cp ../${prefix}${mc}/${prefix}${mc}_L2Relative_AK8PF${jet}.txt ${prefix}${iov}_${data}_L2Relative_AK8PF${jet}.txt"

  cp ${prefix}${iov}_${data}_L1RC_AK4PFchs.txt ${prefix}${iov}_${data}_L1RC_AK8PFchs.txt
  cp ${prefix}${iov}_${data}_DataMcSF_L1RC_AK4PFchs.txt ${prefix}${iov}_${data}_DataMcSF_L1RC_AK8PFchs.txt

  for jet in chs Puppi
  do
    cp ${prefix}${iov}_${data}_L1FastJet_AK4PF${jet}.txt ${prefix}${iov}_${data}_L1FastJet_AK8PF${jet}.txt
    cp ../${prefix}${mc}/${prefix}${mc}_L2Relative_AK8PF${jet}.txt ${prefix}${iov}_${data}_L2Relative_AK8PF${jet}.txt
    cp ${prefix}${iov}_${data}_L3Absolute_AK4PF${jet}.txt ${prefix}${iov}_${data}_L3Absolute_AK8PF${jet}.txt
    cp ${prefix}${iov}_${data}_L2Residual_AK4PF${jet}.txt ${prefix}${iov}_${data}_L2Residual_AK8PF${jet}.txt
    cp ${prefix}${iov}_${data}_L2L3Residual_AK4PF${jet}.txt ${prefix}${iov}_${data}_L2L3Residual_AK8PF${jet}.txt
    cp ${prefix}${iov}_${data}_Uncertainty_AK4PF${jet}.txt ${prefix}${iov}_${data}_Uncertainty_AK8PF${jet}.txt
    cp ${prefix}${iov}_${data}_UncertaintySources_AK4PF${jet}.txt ${prefix}${iov}_${data}_UncertaintySources_AK8PF${jet}.txt
  done

  cd -

done
