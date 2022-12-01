import ROOT
import numpy as np
import argparse
import logging
import re
import os

from JERCHelpers import *

parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("inputTXT", help = "base name of JER txt-files (e.g. Summer20UL16_JRV3_MC); Pt/Eta/PhiRes and SFs will be merged into a single JSON file")
parser.add_argument("-o", "--Output", help = "define path for output JSON (default: input path + \"_\" + algotype + \".json\")")
parser.add_argument("-a", "--AlgoType", default="AK4PFchs", help = "define jet type for which JSON is created")
parser.add_argument("-l", "--ExtraLoggingLevel", default="INFO", help = "choose level of additional logging file (default INFO; other useful choices: DEBUG)")args = parser.parse_args()
baseInputName = os.path.basename(args.inputTXT)

h1 = logging.FileHandler("WarningsAndErrors_JSONConversion.log"); h1.setLevel(logging.WARNING)
h2 = logging.FileHandler("EXTRA_JSONConversion.log"); h2.setLevel(args.ExtraLoggingLevel)
h3 = logging.StreamHandler(); h3.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        h1,h2,h3
    ]
)

output="{}_{}.json".format(args.inputTXT,args.AlgoType)
if args.Output!=None: output= args.output
print("Will convert {} JER files to \n {} \n Pt/Eta/Phi resolution and SFs for {} jets  will be merged into a single JSON".format(args.inputTXT, output, args.AlgoType))

#resolutionLevelsWithAlgo = ["{}_{}".format(corr,args.AlgoType) for corr in resolutionLevels]

for lvl in resolutionLevels:
    print("{}_{}_{}.txt".format(args.inputTXT,lvl,args.AlgoType))
#exit(0)


for lvl in resolutionLevels:
    with open("{}/{}_{}_{}.txt".format(args.inputTXT,args.inputTXT,"SF" if lvl=="ScaleFactor" else lvl,args.AlgoType)) as f:
        lines = f.readlines()
    if "Resolution" in lvl:
        lines[0] = lines[0].replace("Resolution", "Correction Resolution")
    elif "ScaleFactor" in lvl:
        lines[0] = lines[0].replace("ScaleFactor", "Correction ScaleFactor")
    else: raise ValueError('Only for processing JER-files (preprocessing of txt-files)')
    with open("{}_{}_{}.JSONtmptxt".format(args.inputTXT,lvl,args.AlgoType), "w") as f:
        f.writelines(lines)

JECParamsIndiv = [ROOT.JetCorrectorParameters("{}_{}_{}.JSONtmptxt".format(args.inputTXT,lvl,args.AlgoType),"")  for lvl in resolutionLevels]
for lvl in resolutionLevels:
    os.remove("{}_{}_{}.JSONtmptxt".format(args.inputTXT,lvl,args.AlgoType))

parsedCorrections = []
inputsAllLevels = set()
for idx,JECParams in enumerate(JECParamsIndiv):
     #JECParams.printScreen()
     inputsneeded = set() #we only need the input variables set once, even if used multiple times, so filter out overlap 
     for i in range(0,JECParams.definitions().nParVar()): inputsneeded.add(JECParams.definitions().parVar(i)) 
     for i in range(0,JECParams.definitions().nBinVar()): inputsneeded.add(JECParams.definitions().binVar(i)) 
     inputsneeded = list(sorted(inputsneeded))
     inputsAllLevels.update(inputsneeded)
     #if 
     logging.info("Inputs needed for binning and formula evaluation: ", inputsneeded)
     parsedCorrections.append(getIndivCorrectionLevel(JECParams,inputsneeded,resolutionLevels[idx],baseInputName, args.AlgoType))

inputsAllLevels = list(sorted(inputsAllLevels))



from correctionlib.schemav2 import CorrectionSet
import gzip

cset = CorrectionSet.parse_obj({
    "schema_version": 2,
    "corrections": [corr for corr in parsedCorrections],
})



with open(output, "w") as fout:
    fout.write(cset.json(exclude_unset=True, indent=4))

with gzip.open("{}.gz".format(output), "wt") as fout:
    fout.write(cset.json(exclude_unset=True))
