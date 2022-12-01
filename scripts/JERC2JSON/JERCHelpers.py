import ROOT
import numpy as np
import argparse
import logging
import re
import os
from statistics import mean, median, stdev

JEC2016preVFP=[
"Summer19UL16APV_RunBCD_V7_DATA",
"Summer19UL16APV_RunEF_V7_DATA",
"Summer19UL16APV_V7_MC",
]

JER2016preVFP=[
"Summer20UL16APV_JRV3_MC",
]
JEC2016postVFP=[
"Summer19UL16_RunFGH_V7_DATA",
"Summer19UL16_V7_MC",
]

JER2016postVFP=[
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
"Summer19UL17_JRV2_MC",
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

resolutionLevels = ["PtResolution",
#                    "EtaResolution", 
#                    "PhiResolution",
                    "ScaleFactor"
                ]

correctionLevels = ["L1FastJet",
                    "L2Relative",
                    "L3Absolute",
                    "L2L3Residual",
                ]


inputDescriptionMap={
    "JetPt":"pT of the jet before specific correction (for JER: after all corrections applied)",
    "JetA":"area of the jet",
    "JetEta":"pseudorapidity of the jet",
    "Rho":"energy density rho (as measure of PU)",
    "systematic":"systematics: nom, up, down",
}
inputTypeMap={
    "JetPt"  :"real",
    "JetA":"real",
    "JetEta" :"real",
    "Rho"    :"real",
    "systematic":"string",
}

def doSpecialCases(jcparams,recordi): #uncertainties and JER Scale Factors
    CorrectionLevel = jcparams.definitions().level()
    #print(CorrectionLevel)
    parameters = [float(str(np.single(p))) for p in jcparams.record(recordi).parameters()]
    variables = [jcparams.definitions().parVar(i) for i in range(0,jcparams.definitions().nParVar())]
    if CorrectionLevel=="JECSource":
        edges = parameters[::3] #pt 
        upvar = parameters[1::3] #upvars
        assert(len(variables)==1)
        return Binning.parse_obj({
            "nodetype": "binning",
            "edges": edges,
            "input": variables[0],
            "content": [
            FormulaRef.parse_obj({
                "nodetype": "formularef",
                "index": "0",
                "parameters": [(upvar[idx+1]-upvar[idx])/(edges[idx+1]-edges[idx]), (upvar[idx]*edges[idx+1]-upvar[idx+1]*edges[idx])/(edges[idx+1]-edges[idx]),edges[0],edges[-1]], # linear interpolation
            }) for idx in range(len(edges)-1)
            ],
            "flow": "clamp",
        })
    if CorrectionLevel=="ScaleFactor": #only for binned SFs for now (no parametrization, just nom/up/down)
        assert(len(parameters)==3)
        return Category.parse_obj(
            {
                "nodetype": "category",
                "input": "systematic",
                "content": [
                    {"key": "nom", "value": float(parameters[0])},
                    {"key": "up", "value": float(parameters[2])},
                    {"key": "down", "value": float(parameters[1])},
                ],
            }    )

        

def build_formula(jcparams,recordi):
    formula = jcparams.definitions().formula()
    if formula=='""' or formula=="None":
        return doSpecialCases(jcparams,recordi)
    formula = formula.replace("TMath::Log","log")
    formula = formula.replace("TMath::Max","max")
    formula = formula.replace("TMath::Power","pow")
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
    logging.debug("start recusing binvar {}".format(jcparams.definitions().binVar(binvari)))
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
    logging.debug(" ".join(map(str, edges + edgeidx)))

    return Binning.parse_obj({
        "nodetype": "binning",
        "edges": edges,
        "input": jcparams.definitions().binVar(binvari),
        "content": [
            recurseThroughBinningToFormula(jcparams,binvari+1,ei) for ei in edgeidx
        ],
        #        "flow": "clamp", #JEC need a different kind of clamp (in formula)
#        "flow": "error", 
        "flow": 1.0 if jcparams.definitions().level()!="JECSource" else -999., 
    })



from correctionlib.schemav2 import Correction, Binning, Category, Formula, FormulaRef, CompoundCorrection
from correctionlib import schemav2 as schema

def getCompoundJEC(allInputs, corrLevels, baseInputName, AlgoType):
    compJEC = CompoundCorrection.parse_obj(
        {
            "name": "{}_L1L2L3Res_{}".format(baseInputName,AlgoType),
            "description": "compound correction created from {} by using https://github.com/cms-jet/JECDatabase/tree/master/scripts/JERC2JSON/createJSONs.py".format(baseInputName),
            "inputs": [
                {"name": item, "type": inputTypeMap[item], "description" : inputDescriptionMap[item]} for item in allInputs
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

def getIndivCorrectionLevel(jcparams,inputs, corrLevel, baseInputName, AlgoType):
    systInputs = []
    if corrLevel=="ScaleFactor":
        systInputs.append({"name": "systematic", "type": "string", "description": "systematics: nom, up, down"})
    corrJEC = Correction.parse_obj(
        {
            "version": 1,
            "name": "{}_{}_{}".format(baseInputName, corrLevel, AlgoType),
            "description": "{} for {} created from {} by using https://github.com/cms-jet/JECDatabase/tree/master/scripts/JERC2JSON/createJSONs.py".format(corrLevel, AlgoType, baseInputName),
            "inputs": [
                {"name": item, "type": inputTypeMap[item], "description" : inputDescriptionMap[item]} for item in inputs
            ]+systInputs,
            "generic_formulas": [] if corrLevel=="ScaleFactor" else [
                schema.Formula(
                    nodetype="formula",
                    expression="[0]*max(min(x,[3]),[2])+[1]",
                    parser="TFormula",
                    variables=["JetPt"],
                ),
            ],
            "output": {"name": "correction", "type": "real"},
            "data": recurseThroughBinningToFormula(jcparams,0,0),
        }
    )
    logging.debug(corrJEC)
    return corrJEC


def getCorrection(pt,eta,rho,area,corrector=None):
    if corrector == None: raise RuntimeError('Configuration not supported')
    corrector.setJetEta(eta)
    corrector.setJetPt(pt)
    corrector.setJetA(area)
    corrector.setRho(rho)
    corr = corrector.getCorrection()
    return corr

def getResolution(pt,eta,rho,corrector=None):
    if corrector == None: raise RuntimeError('Configuration not supported')
    params_resolution = ROOT.PyJetParametersWrapper()
    params_resolution.setJetEta(eta)
    params_resolution.setJetPt(pt)
    params_resolution.setRho(rho)
    corr = corrector.getResolution(params_resolution)
    return corr

def getScaleFactor(pt,eta,syst,corrector=None):
    if corrector == None: raise RuntimeError('Configuration not supported')
    params_sf_and_uncertainty = ROOT.PyJetParametersWrapper()
    params_sf_and_uncertainty.setJetEta(eta)
    params_sf_and_uncertainty.setJetPt(pt)
    idx=0
    if syst=="up": idx=2
    elif syst=="down": idx=1
    elif syst=="nom": idx=0
    else: raise RuntimeError('systematic variation not supported')
    corr = corrector.getScaleFactor(params_sf_and_uncertainty,idx)
    return corr

def getUncertainty(pt,eta,corrector=None):
    if corrector == None: raise RuntimeError('Configuration not supported')
    corrector.setJetEta(eta)
    corrector.setJetPt(pt)
    corr = corrector.getUncertainty(True)
    return corr

def testCMSSWVsCorrectionlib(correctionInputs,CMSSWcorrector,libcorrector,testVariant="Correction"):
    reldifferences = []
    inputsneeded = [ bla.name for bla in libcorrector.inputs]
    deviationsFound = False
    logpath="logs/{}.txt".format(libcorrector.name)
    if os.path.isfile(logpath):
        os.remove(logpath) #clear log-file for testing.
    for test in correctionInputs:
        CMSSWresult = -1
        if testVariant=="Uncertainty":
            CMSSWresult = getUncertainty(test["JetPt"],
                                        test["JetEta"],
                                        CMSSWcorrector)
        elif testVariant=="Correction":
            CMSSWresult = getCorrection(test["JetPt"],
                                        test["JetEta"],
                                        test["Rho"],
                                        test["JetA"],
                                        CMSSWcorrector)
        elif testVariant=="Resolution":
            CMSSWresult = getResolution(test["JetPt"],
                                        test["JetEta"],
                                        test["Rho"],
                                        CMSSWcorrector)
        elif testVariant=="ScaleFactor":
            CMSSWresult = getScaleFactor(test["JetPt"],
                                        test["JetEta"],
                                        test["systematic"],
                                        CMSSWcorrector)
        evaluateList = [test[key] for key in inputsneeded]
        JSONresult = libcorrector.evaluate(*evaluateList)
        reldifference= 100*(JSONresult-CMSSWresult)/CMSSWresult
        absdifference= abs(JSONresult-CMSSWresult)
        reldifferences.append(reldifference)
#        if abs(reldifference)>1e-4: 
        if abs(reldifference)>1e-2 or absdifference>1e-3: 
            print("pt {} eta{} rho {} JetA {}; JSON: {}; CMSSW: {}; relative difference [%] (100*(J-C)/C): {}".format(test["JetPt"], test["JetEta"], test["Rho"], test["JetA"], JSONresult, CMSSWresult, 100*(JSONresult-CMSSWresult)/CMSSWresult))
            deviationsFound = True
            with open(logpath, "a") as file_object:
                file_object.write("pt {} eta{} rho {} JetA {}; JSON: {}; CMSSW: {}; relative difference [%] (100*(J-C)/C): {}\n".format(test["JetPt"], test["JetEta"], test["Rho"], test["JetA"], JSONresult, CMSSWresult, 100*(JSONresult-CMSSWresult)/CMSSWresult))
        #print("pt {} eta{} rho {} JetA {}; JSON: {}; CMSSW: {}; relative difference [%] (100*(J-C)/C): {}".format(test["JetPt"], test["JetEta"], test["Rho"], test["JetA"], JSONresult, CMSSWresult, 100*(JSONresult-CMSSWresult)/CMSSWresult))    
    
    print("reldifferences max: {}; median: {}; mean: {}; stddev: {}; N: {}".format(max(reldifferences), median(reldifferences), mean(reldifferences),stdev(reldifferences), len(reldifferences)))
    if deviationsFound: 
        with open("testJSONlog.txt", "a") as file_object:
            file_object.write("{}\n".format(libcorrector.name))
        with open(logpath, "a") as file_object:
            file_object.write("reldifferences max: {}; median: {}; mean: {}; stddev: {}; N: {}".format(max(reldifferences), median(reldifferences), mean(reldifferences),stdev(reldifferences), len(reldifferences)))


