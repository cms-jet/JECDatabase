#! /bin/bash

# Create a tarball for a list of JEC text files

#CORRECTIONS="L1FastJet L2Relative L3Absolute L2L3Residual Uncertainty" # for Summer16_25nsV1_MC
CORRECTIONS="L1RC L1JPTOffset L1FastJet L2Relative L2Residual L3Absolute L2L3Residual Uncertainty UncertaintySources"
#CORRECTIONS="L1RC L1FastJet L2Relative L3Absolute L2L3Residual Uncertainty UncertaintySources"

#P=$1!

#Gl= ../textFiles/_
for P in ../textFiles/Fall17_17Nov2017F_V11C_DATA/ ../textFiles/Fall17_17Nov2017F_V8a_DATA/ ../textFiles/Fall17_17Nov2017F_V8b_DATA/ ../textFiles/Fall17_17Nov2017F_V8c_DATA/  ../textFiles/Fall17_17Nov2017F_V8d_DATA/ ../textFiles/Fall17_17Nov2017F_V9_DATA/ ../textFiles/Fall17_17Nov2017_V8_L1fix_MC/

do

    if [ ! -d "$P" ]; then
	echo "$P does not exists"
	#exit 1
	continue
    fi

    ERA=`basename $P`
    
    echo "Creating tarball for ${ERA}..."
    
    pushd $P &> /dev/null
    
    TARBALL=${ERA}.tar.gz
    
    CMD=""
    for C in $CORRECTIONS; do
	CMD=${ERA}_${C}*" $CMD"
    done
    
    tar -hzcf ${TARBALL} ${CMD}
    
    popd &> /dev/null
    
    echo "Done. File saved as ${P}/${TARBALL}"
    
    mv ${P}/${TARBALL} ../tarballs/.
    ls -lh ../tarballs/${TARBALL}
    #echo ${P}/
    rm -r ${P}/
done