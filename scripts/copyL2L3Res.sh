#! /bin/bash
# Script to copy L2L3Residuals files after the global fit to the JEC version
# usage
# ./copyL2L3Res.sh L2L3Res_SOURCE L2L3Res_DESTINATION 
FROM=$1
TO=$2

Name_L2L3Res="GlobalFitOutput_L2L3Residuals_B.txt"
#Name_L2L3Res="GlobalFitOutput_L2L3Residuals_C.txt"
#Name_L2L3Res="GlobalFitOutput_L2L3Residuals_D.txt"
#Name_L2L3Res="GlobalFitOutput_L2L3Residuals_E.txt"
#Name_L2L3Res="GlobalFitOutput_L2L3Residuals_F.txt"

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

# pushd $t &> /dev/null

# echo "Substituing $FROM to $TO in all files..."
# find . \( -type l -o -type f \) |
#     while read filename
#     do
#         if [ -L $filename ]; then
#             target=`readlink $filename`
#             ln -sf ${target//$FROM/$TO} $filename
#         fi
	
#         mv $filename ${filename//$FROM/$TO}
#     done
    
#     popd &> /dev/null
echo "Done"
