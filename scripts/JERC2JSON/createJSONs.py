import subprocess
import shutil
import itertools
import os

from JERCHelpers import *


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
    
print(JER2016,JEC2016)
print(JER2017,JEC2017)
print(JER2018,JEC2018)

#JEC2016,JEC2017,JEC2018=[],[],[] 
#JER2016,JER2017,JER2018=[],[],[] 
createSingleYearJSON(JER2016,JEC2016,algosToConsider,"2016_JERC_All")
createSingleYearJSON(JER2017,JEC2017,algosToConsider,"2017_JERC_All")
createSingleYearJSON(JER2018,JEC2018,algosToConsider,"2018_JERC_All")

