#! /bin/bash
# [tmp] Script to copy L2Residuals and L2L3Residuals files from AK4CHS to the rest
# usage
# ./copyL2Res_AK4CHS_to_All.sh JEC_Folder 
# created by A.Karavdina
FROM=$1
#TO=$2
#How it should be called
Name_L2Res_official=${FROM}_L2Residual
Name_L2L3Res_official=${FROM}_L2L3Residual

#tar -zxvf ${FROM}.tar.gz
f=${FROM}

#echo "Cloning $f to $t"
echo "File name $f/$Name_L2Res"
# #cp -r $f $t
#cp $f/${Name_L2Res}_AK4PFchs.txt $f/${Name_L2Res_official}_AK4PFchs.txt
cp $f/${Name_L2Res_official}_AK4PFchs.txt $f/${Name_L2Res_official}_AK4PFPuppi.txt
cp $f/${Name_L2Res_official}_AK4PFchs.txt $f/${Name_L2Res_official}_AK4PF.txt
cp $f/${Name_L2Res_official}_AK4PFchs.txt $f/${Name_L2Res_official}_AK4JPT.txt
cp $f/${Name_L2Res_official}_AK4PFchs.txt $f/${Name_L2Res_official}_AK4Calo.txt
cp $f/${Name_L2Res_official}_AK4PFchs.txt $f/${Name_L2Res_official}_AK8PFchs.txt
cp $f/${Name_L2Res_official}_AK4PFchs.txt $f/${Name_L2Res_official}_AK8PFPuppi.txt
cp $f/${Name_L2Res_official}_AK4PFchs.txt $f/${Name_L2Res_official}_AK8PF.txt

cp $f/${Name_L2L3Res_official}_AK4PFchs.txt $f/${Name_L2L3Res_official}_AK4PFPuppi.txt
cp $f/${Name_L2L3Res_official}_AK4PFchs.txt $f/${Name_L2L3Res_official}_AK4PF.txt
cp $f/${Name_L2L3Res_official}_AK4PFchs.txt $f/${Name_L2L3Res_official}_AK4JPT.txt
cp $f/${Name_L2L3Res_official}_AK4PFchs.txt $f/${Name_L2L3Res_official}_AK4Calo.txt
cp $f/${Name_L2L3Res_official}_AK4PFchs.txt $f/${Name_L2L3Res_official}_AK8PFchs.txt
cp $f/${Name_L2L3Res_official}_AK4PFchs.txt $f/${Name_L2L3Res_official}_AK8PFPuppi.txt
cp $f/${Name_L2L3Res_official}_AK4PFchs.txt $f/${Name_L2L3Res_official}_AK8PF.txt

echo "Check the file: "$f/${Name_L2L3Res_official}_AK8PFchs.txt

echo "Done"
