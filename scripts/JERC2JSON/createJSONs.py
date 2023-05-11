import subprocess
import shutil
import itertools
import os

from JERCHelpers import *


def createSingleYearJSON(jerList, jecList, algosToConsider, outputName):
    try:
        guessDesiredTargetDir=outputName.split("/")[0]
        if not os.path.exists(guessDesiredTargetDir): os.makedirs(guessDesiredTargetDir)
        print("Created output directory",guessDesiredTargetDir, "if not already done")
    except:
        print("Directory for output already created or not successfully guessed")
    
    jerAlgoList = list(itertools.product(jerList, algosToConsider))
    jecAlgoList = list(itertools.product(jecList, algosToConsider))
    
    if "2017_UL" in outputName: #manual fix as UL17_JRV2 only contains AK4PFchs SF/PtResolution
        jerAlgoList = list(itertools.product(jerList, ["AK4PFchs"]))
    
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
    

    JERSmearJSON = ["JERSmear.json.gz"]
    command = " ".join(["python3", "-m", "correctionlib.cli", "merge"] + ["{}_{}.json.gz".format(comp[0],comp[1]) for comp in (jerAlgoList+jecAlgoList)] + JERSmearJSON + [">", "{}.json".format(outputName)])

    
    print(command)#subprocess seems to not work with long command?
    print("python3 -m correctionlib.cli --html {}.html summary {}.json".format(outputName,outputName))
    print("rm {}.json.gz".format(outputName))
    print("gzip {}.json".format(outputName))
    os.system(command)#subprocess seems to not work with long command?
    os.system("python3 -m correctionlib.cli --html {}.html summary {}.json".format(outputName,outputName))
    os.system("rm {}.json.gz".format(outputName))
    os.system("gzip {}.json".format(outputName))

    jerAK4List = list(itertools.product(jerList, ["AK4PFchs"]))
    jecAK4List = list(itertools.product(jecList, ["AK4PFchs"]))
    outputNameAK4 = "{}/jet_jerc".format(outputName.split("/")[0])
    command = " ".join(["python3", "-m", "correctionlib.cli", "merge"] + ["{}_{}.json.gz".format(comp[0],comp[1]) for comp in (jerAK4List+jecAK4List)] + JERSmearJSON + [">", "{}.json".format(outputNameAK4)])
    print(command)#subprocess seems to not work with long command?
    print("python3 -m correctionlib.cli --html {}.html summary {}.json".format(outputNameAK4,outputNameAK4))
    print("rm {}.json.gz".format(outputNameAK4))
    print("gzip {}.json".format(outputNameAK4))
    os.system(command)#subprocess seems to not work with long command?
    os.system("python3 -m correctionlib.cli --html {}.html summary {}.json".format(outputNameAK4,outputNameAK4))
    os.system("rm {}.json.gz".format(outputNameAK4))
    os.system("gzip {}.json".format(outputNameAK4))

    jerAK8List = list(itertools.product(jerList, ["AK8PFPuppi"]))
    if "2017_UL" in outputName: #manual fix as UL17_JRV2 only contains AK4PFchs SF/PtResolution
        jerAK8List = []
    jecAK8List = list(itertools.product(jecList, ["AK8PFPuppi"]))
    outputNameAK8 = "{}/fatJet_jerc".format(outputName.split("/")[0])
    command = " ".join(["python3", "-m", "correctionlib.cli", "merge"] + ["{}_{}.json.gz".format(comp[0],comp[1]) for comp in (jerAK8List+jecAK8List)] + JERSmearJSON + [">", "{}.json".format(outputNameAK8)])
    print(command)#subprocess seems to not work with long command?
    print("python3 -m correctionlib.cli --html {}.html summary {}.json".format(outputNameAK8,outputNameAK8))
    print("rm {}.json.gz".format(outputNameAK8))
    print("gzip {}.json".format(outputNameAK8))
    os.system(command)#subprocess seems to not work with long command?
    os.system("python3 -m correctionlib.cli --html {}.html summary {}.json".format(outputNameAK8,outputNameAK8))
    os.system("rm {}.json.gz".format(outputNameAK8))
    os.system("gzip {}.json".format(outputNameAK8))



    
print(JER2016preVFP,JEC2016preVFP)
print(JER2016postVFP,JEC2016postVFP)
print(JER2017,JEC2017)
print(JER2018,JEC2018)

#JEC2016,JEC2017,JEC2018=[],[],[] 
#JER2016,JER2017,JER2018=[],[],[] 
createJSONForJERSmearingFunctionality()

createSingleYearJSON(JER2016preVFP, JEC2016preVFP,  algosToConsider,"2016preVFP_UL/UL16preVFP_jerc")
createSingleYearJSON(JER2016postVFP,JEC2016postVFP, algosToConsider,"2016postVFP_UL/UL16postVFP_jerc")
createSingleYearJSON(JER2017,       JEC2017,        algosToConsider,"2017_UL/UL17_jerc")
createSingleYearJSON(JER2018,       JEC2018,        algosToConsider,"2018_UL/UL18_jerc")

