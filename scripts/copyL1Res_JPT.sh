#! /bin/bash
# [temporary] scrip to copy unchanges L1Res and JPT files
# usage
# ./copyL1Res_JPT.sh
#DATA
for path in Summer16_23Sep2016BCD Summer16_23Sep2016EF Summer16_23Sep2016G Summer16_23Sep2016H
do
    #Calo and JPT jets
    #echo "path = " $path
    for file in L1FastJet_AK4Calo L1FastJet_AK4JPT L1JPTOffset_AK4JPT L2L3Residual_AK4Calo L2L3Residual_AK4JPT L2Relative_AK4Calo L2Relative_AK4JPT L2Residual_AK4Calo L2Residual_AK4JPT L3Absolute_AK4Calo L3Absolute_AK4JPT 
    do
	cp ${path}V4_DATA/${path}V4_DATA_${file}.txt ${path}V5_DATA/${path}V5_DATA_${file}.txt
    done
    #L1Res output
    for file in L1RC_AK4PFchs L1RC_AK4PF L1RC_AK8PFchs L1RC_AK8PF L1FastJet_AK4PFchs L1FastJet_AK4PFPuppi L1FastJet_AK4PF L1FastJet_AK8PFchs L1FastJet_AK8PFPuppi L1FastJet_AK8PF 
    do
	cp ${path}V4_DATA/${path}V4_DATA_${file}.txt ${path}V5_DATA/${path}V5_DATA_${file}.txt
    done
    #L1Res SFs
    for file in DataMcSF_L1RC_AK4PFchs DataMcSF_L1RC_AK4PF DataMcSF_L1RC_AK8PFchs DataMcSF_L1RC_AK8PF
    do
	cp ${path}V4_DATA/${path}V4_${file}.txt ${path}V5_DATA/${path}V5_${file}.txt
    done
done

#MC
#L1Res output: L1RC
pathMC=Summer16_23Sep2016
for file in L1RC_AK4PFchs L1RC_AK4PF L1RC_AK8PFchs L1RC_AK8PF
do
    cp ${pathMC}V4_MC/${pathMC}V4_MC_${file}.txt ${pathMC}V5_MC/${pathMC}V5_MC_${file}.txt
done

# FROM=$1
# TO=$2
# Name_L2Res="Spring16_25ns_MPF_LOGLIN_L2Residual_pythia8_AK4PFchs.txt"
# L3Res_new=$3" "$4" "$5
# echo "Following L3Residuals are going to be used: $L3Res_new"
# echo "$Name_L2Res"
# Name_L2Res_official=${TO}_L2Residual
# Name_L2L3Res_official=${TO}_L2L3Residual

# #tar -zxvf ${FROM}.tar.gz
# f=${FROM}
# t=${TO}

# if [ ! -d "$f" ]; then
#     echo "Error: $f does not exist"
#     continue
# fi

# # if [ -d "$t" ]; then
# #     echo "Error: $t already exist"
# #     continue
# # fi

# echo "Cloning $f to $t"
# echo "File name $f/$Name_L2Res"
# #cp -r $f $t
# cp $f/${Name_L2Res} $t/${Name_L2Res_official}_AK4PFchs.txt
# cp $f/${Name_L2Res} $t/${Name_L2Res_official}_AK4PFPuppi.txt
# cp $f/${Name_L2Res} $t/${Name_L2Res_official}_AK4PF.txt
# cp $f/${Name_L2Res} $t/${Name_L2Res_official}_AK4JPT.txt
# cp $f/${Name_L2Res} $t/${Name_L2Res_official}_AK4Calo.txt
# cp $f/${Name_L2Res} $t/${Name_L2Res_official}_AK8PFchs.txt
# cp $f/${Name_L2Res} $t/${Name_L2Res_official}_AK8PFPuppi.txt
# cp $f/${Name_L2Res} $t/${Name_L2Res_official}_AK8PF.txt

# L3Res_default="1 0.0000 0.0"
# echo "Change dummy L3Res ($L3Res_default) to real $L3Res_new values"
# cp $f/${Name_L2Res} $t/${Name_L2L3Res_official}_AK4PFchs.txt
# sed -i "s/${L3Res_default}/${L3Res_new}/g" $t/${Name_L2L3Res_official}_AK4PFchs.txt
# cp $f/${Name_L2Res} $t/${Name_L2L3Res_official}_AK4PFPuppi.txt
# sed -i "s/${L3Res_default}/${L3Res_new}/g" $t/${Name_L2L3Res_official}_AK4PFPuppi.txt
# cp $f/${Name_L2Res} $t/${Name_L2L3Res_official}_AK4PF.txt
# sed -i "s/${L3Res_default}/${L3Res_new}/g" $t/${Name_L2L3Res_official}_AK4PF.txt
# cp $f/${Name_L2Res} $t/${Name_L2L3Res_official}_AK4JPT.txt
# sed -i "s/${L3Res_default}/${L3Res_new}/g" $t/${Name_L2L3Res_official}_AK4JPT.txt
# cp $f/${Name_L2Res} $t/${Name_L2L3Res_official}_AK4Calo.txt
# sed -i "s/${L3Res_default}/${L3Res_new}/g" $t/${Name_L2L3Res_official}_AK4Calo.txt
# cp $f/${Name_L2Res} $t/${Name_L2L3Res_official}_AK8PFchs.txt
# sed -i "s/${L3Res_default}/${L3Res_new}/g" $t/${Name_L2L3Res_official}_AK8PFchs.txt
# cp $f/${Name_L2Res} $t/${Name_L2L3Res_official}_AK8PFPuppi.txt
# sed -i "s/${L3Res_default}/${L3Res_new}/g" $t/${Name_L2L3Res_official}_AK8PFPuppi.txt
# cp $f/${Name_L2Res} $t/${Name_L2L3Res_official}_AK8PF.txt
# sed -i "s/${L3Res_default}/${L3Res_new}/g" $t/${Name_L2L3Res_official}_AK8PF.txt

# echo "Check the file: "$t/${Name_L2L3Res_official}_AK4PFchs.txt

# # pushd $t &> /dev/null

# # echo "Substituing $FROM to $TO in all files..."
# # find . \( -type l -o -type f \) |
# #     while read filename
# #     do
# #         if [ -L $filename ]; then
# #             target=`readlink $filename`
# #             ln -sf ${target//$FROM/$TO} $filename
# #         fi
	
# #         mv $filename ${filename//$FROM/$TO}
# #     done
    
# #     popd &> /dev/null
echo "Done"
