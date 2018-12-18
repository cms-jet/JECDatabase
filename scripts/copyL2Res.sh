#! /bin/bash
# Script to copy L2Residuals files and add L3Residuals part
# usage
# ./copyL2Res.sh L2Res_SOURCE L2Res_DESTINATION L3Res_par0 L3Res_par1 L3Res_par2
# created by A.Karavdina
FROM=$1
TO=$2

#How it's called in files from L2Res analyser

#MPF with loglin
Name_L2Res="Fall17_17Nov2017_MPF_LOGLIN_L2Residual_pythia8_AK4PFchs.txt" 

L3Res_new=$3" "$4" "$5
echo "Following L3Residuals are going to be used: $L3Res_new"
echo "$Name_L2Res"

#How it should be called
Name_L2Res_official=${TO}_L2Residual
Name_L2L3Res_official=${TO}_L2L3Residual


f=${FROM}
t=${TO}



echo "Cloning $f to $t"
echo "File name $f/$Name_L2Res"
# #cp -r $f $t
cp $f/${Name_L2Res} $t/${Name_L2Res_official}_AK4PFchs.txt
cp $f/${Name_L2Res} $t/${Name_L2Res_official}_AK4PFPuppi.txt
cp $f/${Name_L2Res} $t/${Name_L2Res_official}_AK4PF.txt
cp $f/${Name_L2Res} $t/${Name_L2Res_official}_AK4JPT.txt
cp $f/${Name_L2Res} $t/${Name_L2Res_official}_AK4Calo.txt
cp $f/${Name_L2Res} $t/${Name_L2Res_official}_AK8PFchs.txt
cp $f/${Name_L2Res} $t/${Name_L2Res_official}_AK8PFPuppi.txt
cp $f/${Name_L2Res} $t/${Name_L2Res_official}_AK8PF.txt

L3Res_default="1 0.0000 0.0"
echo "Change dummy L3Res ($L3Res_default) to real $L3Res_new values"
cp  $t/${Name_L2Res_official}_AK4PFchs.txt $t/${Name_L2L3Res_official}_AK4PFchs.txt
sed -i "s/${L3Res_default}/${L3Res_new}/g" $t/${Name_L2L3Res_official}_AK4PFchs.txt
cp  $t/${Name_L2Res_official}_AK4PFchs.txt $t/${Name_L2L3Res_official}_AK4PFPuppi.txt
sed -i "s/${L3Res_default}/${L3Res_new}/g" $t/${Name_L2L3Res_official}_AK4PFPuppi.txt
cp  $t/${Name_L2Res_official}_AK4PFchs.txt $t/${Name_L2L3Res_official}_AK4PF.txt
sed -i "s/${L3Res_default}/${L3Res_new}/g" $t/${Name_L2L3Res_official}_AK4PF.txt
cp  $t/${Name_L2Res_official}_AK4PFchs.txt $t/${Name_L2L3Res_official}_AK4JPT.txt
sed -i "s/${L3Res_default}/${L3Res_new}/g" $t/${Name_L2L3Res_official}_AK4JPT.txt
cp  $t/${Name_L2Res_official}_AK4PFchs.txt $t/${Name_L2L3Res_official}_AK4Calo.txt
sed -i "s/${L3Res_default}/${L3Res_new}/g" $t/${Name_L2L3Res_official}_AK4Calo.txt
cp  $t/${Name_L2Res_official}_AK4PFchs.txt $t/${Name_L2L3Res_official}_AK8PFchs.txt
sed -i "s/${L3Res_default}/${L3Res_new}/g" $t/${Name_L2L3Res_official}_AK8PFchs.txt
cp  $t/${Name_L2Res_official}_AK4PFchs.txt $t/${Name_L2L3Res_official}_AK8PFPuppi.txt
sed -i "s/${L3Res_default}/${L3Res_new}/g" $t/${Name_L2L3Res_official}_AK8PFPuppi.txt
cp  $t/${Name_L2Res_official}_AK4PFchs.txt $t/${Name_L2L3Res_official}_AK8PF.txt
sed -i "s/${L3Res_default}/${L3Res_new}/g" $t/${Name_L2L3Res_official}_AK8PF.txt

echo "Check the file: "$t/${Name_L2L3Res_official}_AK4PFchs.txt
echo "Done"
