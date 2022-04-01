import ROOT
import numpy as np
import argparse
import logging
import re
import os

from JERCHelpers import *

parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("inputTXT", help = "base name of JEC txt-files (e.g. Summer19UL16APV_V2_MC); L1/L2/L3/L2L3Residual PFCHS corrections will be merged into a single JSON")
parser.add_argument("-o", "--Output", help = "define path for output JSON (default: input path + \".json\")")
parser.add_argument("-a", "--AlgoType", default="AK4PFchs", help = "define jet type for which JSON is created")
args = parser.parse_args()
baseInputName = os.path.basename(args.inputTXT)


output="{}_{}.json".format(args.inputTXT,args.AlgoType)
if args.Output!=None: output= args.output
print("Will convert {} JEC files to \n {} \n L1/L2/L3/L2L3Residual corrections for {} jets  will be merged into a single JSON".format(args.inputTXT, output, args.AlgoType))

correctionLevelsWithAlgo = ["{}_{}".format(corr,args.AlgoType) for corr in correctionLevels]

JECParamsIndiv = []
for lvl in correctionLevels:
    print("{}_{}_{}.txt".format(args.inputTXT,lvl,args.AlgoType))
    JECParamsIndiv.append(ROOT.JetCorrectorParameters("{}/{}_{}_{}.txt".format(args.inputTXT,args.inputTXT,lvl,args.AlgoType),""))
#exit(0)
#JECParamsIndiv = [ROOT.JetCorrectorParameters("{}_{}_{}.txt".format(args.inputTXT,lvl,args.AlgoType),"")  for lvl in correctionLevels]

SourceSections = []
if "MC" in args.inputTXT: #only provide uncertainty sources for MC
    with open('{}/{}_UncertaintySources_{}.txt'.format(args.inputTXT,args.inputTXT,args.AlgoType),'r') as f:
        #  SourceSections = ["{}_{}".format(line.strip().strip('[]'),args.AlgoType) for line in f if line.startswith('[')]
        SourceSections = [line.strip().strip('[]') for line in f if line.startswith('[')]


vPar = {}#ROOT.vector(ROOT.JetCorrectorParameters)()
for source in SourceSections:
    vPar[source]=ROOT.JetCorrectorParameters('{}/{}_UncertaintySources_{}.txt'.format(args.inputTXT,args.inputTXT,args.AlgoType),source)

from correctionlib.schemav2 import Correction, Binning, Category, Formula, FormulaRef, CompoundCorrection
from correctionlib import schemav2 as schema

uncertaintiesParsed=[]
for source in SourceSections:
    inputsneeded = set() #we only need the input variables set once, even if used multiple times, so filter out overlap 
    for i in range(0,vPar[source].definitions().nParVar()): inputsneeded.add(vPar[source].definitions().parVar(i)) 
    for i in range(0,vPar[source].definitions().nBinVar()): inputsneeded.add(vPar[source].definitions().binVar(i)) 
    inputsneeded = list(sorted(inputsneeded))
    uncertaintiesParsed.append(getIndivCorrectionLevel(vPar[source],inputsneeded,source,baseInputName, args.AlgoType))


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
     parsedCorrections.append(getIndivCorrectionLevel(JECParams,inputsneeded,correctionLevels[idx],baseInputName, args.AlgoType))

inputsAllLevels = list(sorted(inputsAllLevels))



from correctionlib.schemav2 import CorrectionSet
import gzip

cset = CorrectionSet.parse_obj({
    "schema_version": 2,
    "corrections": [corr for corr in parsedCorrections] + uncertaintiesParsed,
    "compound_corrections": [getCompoundJEC(inputsAllLevels,correctionLevelsWithAlgo,baseInputName, args.AlgoType)]
})




with open(output, "w") as fout:
    fout.write(cset.json(exclude_unset=True, indent=4))

with gzip.open("{}.gz".format(output), "wt") as fout:
    fout.write(cset.json(exclude_unset=True))
