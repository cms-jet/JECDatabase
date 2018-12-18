#! /bin/bash
# [tmp] Script to copy L2L3Residuals files after the global fit to the JEC version
# usage
# ./copyL2L3Res.sh L2L3Res_SOURCE_DIR L2L3Res_DESTINATION_DIR 
# created by A.Karavdina
FROM=$1
TO=$2

Name_L2L3Res="GlobalFitOutput_L2L3Residuals_B.txt"

Name_L2Res_official=${TO}_L2Residual
Name_L2L3Res_official=${TO}_L2L3Residual

f=${FROM}
t=${TO}


echo "Cloning $f to $t"
echo "File name $f/$Name_L2L3Res"
# #cp -r $f $t
cp $f/${Name_L2L3Res} $t/${Name_L2Res_official}_AK4PFchs.txt
cp $f/${Name_L2Rest} $t/${Name_L2Res_official}_AK4PFPuppi.txt
cp $f/${Name_L2L3Res} $t/${Name_L2Res_official}_AK4PF.txt
cp $f/${Name_L2L3Res} $t/${Name_L2Res_official}_AK4JPT.txt
cp $f/${Name_L2L3Res} $t/${Name_L2Res_official}_AK4Calo.txt
cp $f/${Name_L2L3Res} $t/${Name_L2Res_official}_AK8PFchs.txt
cp $f/${Name_L2L3Res} $t/${Name_L2Res_official}_AK8PFPuppi.txt
cp $f/${Name_L2L3Res} $t/${Name_L2Res_official}_AK8PF.txt

cp  $t/${Name_L2Res_official}_AK4PFchs.txt $t/${Name_L2L3Res_official}_AK4PFchs.txt
cp  $t/${Name_L2Res_official}_AK4PFchs.txt $t/${Name_L2L3Res_official}_AK4PFPuppi.txt
cp  $t/${Name_L2Res_official}_AK4PFchs.txt $t/${Name_L2L3Res_official}_AK4PF.txt
cp  $t/${Name_L2Res_official}_AK4PFchs.txt $t/${Name_L2L3Res_official}_AK4JPT.txt
cp  $t/${Name_L2Res_official}_AK4PFchs.txt $t/${Name_L2L3Res_official}_AK4Calo.txt
cp  $t/${Name_L2Res_official}_AK4PFchs.txt $t/${Name_L2L3Res_official}_AK8PFchs.txt
cp  $t/${Name_L2Res_official}_AK4PFchs.txt $t/${Name_L2L3Res_official}_AK8PFPuppi.txt
cp  $t/${Name_L2Res_official}_AK4PFchs.txt $t/${Name_L2L3Res_official}_AK8PF.txt

echo "Check the file: "$t/${Name_L2L3Res_official}_AK4PFchs.txt

echo "Done"
