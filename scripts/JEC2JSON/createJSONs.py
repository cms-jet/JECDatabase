import subprocess
import shutil
import itertools
import os

JEC2016=[
"Summer19UL16APV_RunBCD_V7_DATA",
"Summer19UL16APV_RunEF_V7_DATA",
"Summer19UL16APV_V7_MC",
"Summer19UL16_RunFGH_V7_DATA",
"Summer19UL16_V7_MC",
]

JER2016=[
"Summer20UL16APV_JRV3_MC",
"Summer20UL16_JRV3_MC"
]

JEC2017=[
"Summer19UL17_V5_MC",
"Summer19UL17_RunB_V5_DATA",
"Summer19UL17_RunC_V5_DATA",
"Summer19UL17_RunD_V5_DATA",
"Summer19UL17_RunE_V5_DATA",
"Summer19UL17_RunF_V5_DATA",
]

JER2017=[
"Summer19UL17_JRV3_MC",
]

JEC2018=[
"Summer19UL18_V5_MC",
"Summer19UL18_RunA_V5_DATA",
"Summer19UL18_RunB_V5_DATA",
"Summer19UL18_RunC_V5_DATA",
"Summer19UL18_RunD_V5_DATA",
]

JER2018=[
"Summer19UL18_JRV2_MC",
]

algosToConsider=[
"AK4PFchs",
"AK8PFPuppi"
]

def createSingleYearJSON(jerList, jecList, algosToConsider, outputName):
    jerAlgoList = list(itertools.product(jerList, algosToConsider))
    jecAlgoList = list(itertools.product(jecList, algosToConsider))


    for p in jecAlgoList:
        jec,algo=p
        subprocess.run(["wget","-q","-O","{}.tar.gz".format(jec), "https://github.com/cms-jet/JECDatabase/raw/master/tarballs/{}.tar.gz".format(jec)])
        shutil.unpack_archive("{}.tar.gz".format(jec),jec)
        subprocess.run(["python3", "JEC2JSON.py", "-a",algo, jec])
    
    for p in jerAlgoList:
        jer,algo=p
        subprocess.run(["wget", "-q", "-O","{}.tar.gz".format(jer), "https://github.com/cms-jet/JRDatabase/raw/master/tarballs/{}.tar.gz".format(jer)])
        shutil.unpack_archive("{}.tar.gz".format(jer),jer)
        subprocess.run(["python3", "JER2JSON.py", "-a",algo,jer])
    
    print("Done generating individual jsons. Will merge into single year files now")
    
    command = " ".join(["python3", "-m", "correctionlib.cli", "merge"] + ["{}_{}.json.gz".format(comp[0],comp[1]) for comp in (jerAlgoList+jecAlgoList)] + [">", "{}.json".format(outputName)])
    print(command)
    
    os.system(command)#subprocess seems to not work with long command?
    os.system("python3 -m correctionlib.cli --html {}.html summary {}.json".format(outputName,outputName))
    os.system("gzip {}.json".format(outputName))
#    subprocess.run([command])
#    subprocess.run(["python3", "-m", "correctionlib.cli", "merge"] + ["{}_{}.json.gz".format(comp[0],comp[1]) for comp in (jerAlgoList+jecAlgoList)] + [">", "{}.json".format(outputName)])
    

createSingleYearJSON(JER2016,JEC2016,algosToConsider,"2016_JERC_All")
createSingleYearJSON(JER2017,JEC2017,algosToConsider,"2017_JERC_All")
createSingleYearJSON(JER2018,JEC2018,algosToConsider,"2018_JERC_All")

