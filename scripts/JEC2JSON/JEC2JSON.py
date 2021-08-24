import ROOT
import numpy as np
import argparse
import logging
import re
import os

parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("inputTXT", help = "base name of JEC txt-files (e.g. Summer19UL16APV_V2_MC); L1/L2/L3/L2L3Residual PFCHS corrections will be merged into a single JSON")
parser.add_argument("-o", "--Output", help = "define path for output JSON (default: input path + \".json\")")
parser.add_argument("-a", "--AlgoType", default="AK4PFchs", help = "define jet type for which JSON is created")
args = parser.parse_args()
baseInputName = os.path.basename(args.inputTXT)


output=args.inputTXT+".json"
if args.Output!=None: output= args.output
print("Will convert {} JEC files to \n {} \n L1/L2/L3/L2L3Residual corrections for {} jets  will be merged into a single JSON".format(args.inputTXT, output, args.AlgoType))

correctionLevels = ["L1FastJet",
                    "L2Relative",
                    "L3Absolute",
                    "L2L3Residual",
                ]
correctionLevels = ["{}_{}".format(corr,args.AlgoType) for corr in correctionLevels]

for lvl in correctionLevels:
    print("{}_{}.txt".format(args.inputTXT,lvl))
#exit(0)
JECParamsIndiv = [ROOT.JetCorrectorParameters("{}_{}.txt".format(args.inputTXT,lvl),"")  for lvl in correctionLevels]


def build_formula(jcparams,recordi):
    formula = jcparams.definitions().formula()
    formula = formula.replace("TMath::Log","log")
    parameters = [float(str(np.single(p))) for p in jcparams.record(recordi).parameters()]
    #parameters = [p for p in jcparams.record(recordi).parameters()]
    parametersForm = parameters[2*jcparams.definitions().nParVar():]
    for i in reversed(range(0,len(parametersForm))):
        formula=formula.replace("[{}]".format(i),"[{}]".format(i+2*jcparams.definitions().nParVar()))
    possibleVariables = ["x","y","z","t"]
    for i in range(0,jcparams.definitions().nParVar()):
        #toreplace = "(?<![A-z])([xyzt])(?![A-z])"
        toreplace = "(?<![A-z]){}(?![A-z])".format(possibleVariables[i])
        replacement = "max(min({var},[{upbound}]),[{lowbound}])".format(var=possibleVariables[i],lowbound=i*2,upbound=i*2+1)
        formula = re.sub(toreplace,replacement,formula)
        logging.debug(formula)
    #clamping not implemented, yet. Clamping of observables defined in first 2*nParVar parameters
    variables = [jcparams.definitions().parVar(i) for i in range(0,jcparams.definitions().nParVar())]
    logging.debug(variables)
    return Formula.parse_obj({
        "nodetype": "formula",
        "expression": formula,
        "parser": "TFormula",
        "parameters": parameters, # parametersForm,
        "variables": variables, #was e.g. ["JetPt"],
    })


def recurseThroughBinningToFormula(jcparams, binvari, recordi):
    if binvari>=jcparams.definitions().nBinVar():
        return build_formula(jcparams,recordi) #"formula and params"
    logging.info("start recusing binvar {}".format(jcparams.definitions().binVar(binvari)))
    logging.debug("collecting edges via neighbours...")
    edges = []
    edgeidx = []
    findnext=recordi
    #stitch together first lowedge with all following upedges to get edge list
    edges.append(float(str(np.single(jcparams.record(findnext).xMin(binvari)))))
    logging.debug(np.single(jcparams.record(findnext).xMin(binvari)))
    while findnext>-1:
        edgeidx.append(findnext)
        edges.append(float(str(np.single(jcparams.record(findnext).xMax(binvari)))))
        findnext = jcparams.neighbourBin(findnext,binvari,True)
    logging.debug(edges, edgeidx)

    return Binning.parse_obj({
        "nodetype": "binning",
        "edges": edges,
        "input": jcparams.definitions().binVar(binvari),
        "content": [
            recurseThroughBinningToFormula(jcparams,binvari+1,ei) for ei in edgeidx
        ],
        #        "flow": "clamp", #JEC need a different kind of clamp (in formula)
#        "flow": "error", 
        "flow": 1.0, 
    })



from correctionlib.schemav2 import Correction, Binning, Category, Formula, CompoundCorrection

def getCompoundJEC(allInputs, corrLevels):
    compJEC = CompoundCorrection.parse_obj(
        {
            "name": "{}_{}_L1L2L3Res".format(baseInputName,args.AlgoType),
            "description": "compound correction created from {} by using https://github.com/cms-jet/JECDatabase/tree/master/scripts/JEC2JSON.py".format(baseInputName),
            "inputs": [
                {"name": item, "type": "real"} for item in allInputs
            ],
            "inputs_update": ["JetPt"],
            "input_op": "*",
            "output_op": "*",
            "output": {"name": "correction", "type": "real"},
            "stack": ["{}_{}".format(baseInputName, level) for level in corrLevels],
        }
    )
    logging.debug(compJEC)
    return compJEC

def getIndivCorrectionLevel(jcparams,inputs, corrLevel):
    corrJEC = Correction.parse_obj(
        {
            "version": 1,
            "name": "{}_{}".format(baseInputName, corrLevel),
            "description": "{} created from {} by using https://github.com/cms-jet/JECDatabase/tree/master/scripts/JEC2JSON.py".format(corrLevel, baseInputName),
            "inputs": [
                {"name": item, "type": "real"} for item in inputs
            ],
            "output": {"name": "correction", "type": "real"},
            "data": recurseThroughBinningToFormula(jcparams,0,0),
        }
    )
    logging.debug(corrJEC)
    return corrJEC


parsedCorrections = []
inputsAllLevels = set()
for idx,JECParams in enumerate(JECParamsIndiv):
     JECParams.printScreen()
     
     inputsneeded = set() #we only need the input variables set once, even if used multiple times, so filter out overlap 
     for i in range(0,JECParams.definitions().nParVar()): inputsneeded.add(JECParams.definitions().parVar(i)) 
     for i in range(0,JECParams.definitions().nBinVar()): inputsneeded.add(JECParams.definitions().binVar(i)) 
     inputsneeded = list(sorted(inputsneeded))
     inputsAllLevels.update(inputsneeded)
     logging.info("Inputs needed for binning and formula evaluation: ", inputsneeded)
     parsedCorrections.append(getIndivCorrectionLevel(JECParams,inputsneeded,correctionLevels[idx]))

inputsAllLevels = list(sorted(inputsAllLevels))



from correctionlib.schemav2 import CorrectionSet
import gzip

cset = CorrectionSet.parse_obj({
    "schema_version": 2,
    "corrections": [corr for corr in parsedCorrections],
    "compound_corrections": [getCompoundJEC(inputsAllLevels,correctionLevels)]
})

with open(output, "w") as fout:
    fout.write(cset.json(exclude_unset=True, indent=4))

with gzip.open("{}.gz".format(output), "wt") as fout:
    fout.write(cset.json(exclude_unset=True))
