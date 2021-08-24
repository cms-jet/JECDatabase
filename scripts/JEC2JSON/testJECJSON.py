import ROOT
import correctionlib._core as core
from correctionlib import schemav2 as schema
import argparse
from statistics import mean, median, stdev
import os

parser = argparse.ArgumentParser()
parser.add_argument("inputTXT", help = "base name of JEC txt-files (e.g. Summer19UL16APV_V2_MC); L1/L2/L3/L2L3Residual PFCHS corrections will be merged into a single JSON")
parser.add_argument("-i", "--inputJSON", help = "define path for input JSON (default: inputTXT + \".json\")")
parser.add_argument("-a", "--AlgoType", default="AK4PFchs", help = "define jet type for which JSON is created")
args = parser.parse_args()
inputJSON = args.inputTXT + ".json"
if args.inputJSON!=None: inputJSON= args.inputJSON
baseInputName = os.path.basename(args.inputTXT)


correctionLevels = ["L1FastJet",
                    "L2Relative",
                    "L3Absolute",
                    "L2L3Residual",
                ]
correctionLevels = ["{}_{}".format(corr,args.AlgoType) for corr in correctionLevels]

for lvl in correctionLevels:
    print("{}_{}.txt".format(args.inputTXT,lvl))

def getCorrection(pt,eta,rho,area,corrector=None):
    if corrector == None: raise RuntimeError('Configuration not supported')
    corrector.setJetEta(eta)
    corrector.setJetPt(pt)
    corrector.setJetA(area)
    corrector.setRho(rho)
    corr = corrector.getCorrection()
    return corr

def testCMSSWVsCorrectionlib(correctionInputs,CMSSWcorrector,libcorrector):
    reldifferences = []
    inputsneeded = [ bla.name for bla in libcorrector.inputs]
    for test in correctionInputs:
        CMSSWresult = getCorrection(test["JetPt"],
                                    test["JetEta"],
                                    test["Rho"],
                                    test["JetA"],
                                    JetCorrector)
        evaluateList = [test[key] for key in inputsneeded]
        JSONresult = libcorrector.evaluate(*evaluateList)
        reldifference= 100*(JSONresult-CMSSWresult)/CMSSWresult
        reldifferences.append(reldifference)
        if abs(reldifference)>1e-4: print("pt {} eta{} rho {} JetA {}; JSON: {}; CMSSW: {}; relative difference [%] (100*(J-C)/C): {}".format(test["JetPt"], test["JetEta"], test["Rho"], test["JetA"], JSONresult, CMSSWresult, 100*(JSONresult-CMSSWresult)/CMSSWresult))    
        #print("pt {} eta{} rho {} JetA {}; JSON: {}; CMSSW: {}; relative difference [%] (100*(J-C)/C): {}".format(test["JetPt"], test["JetEta"], test["Rho"], test["JetA"], JSONresult, CMSSWresult, 100*(JSONresult-CMSSWresult)/CMSSWresult))    
    
    print("reldifferences max: {}; median: {}; mean: {}; stddev: {}".format(max(reldifferences), median(reldifferences), mean(reldifferences),stdev(reldifferences)))


pts  = [-1.] + [(10**(x)) for x in range(-1,5)]
etas = [-10.,-5.191, -4.889, -2.,0.,1.305, 3., 5.191, 5.192]
rhos = [-1., 5., 10., 50.]
jetas = [-1., 0.5,1.,5.]

correctionInputList = []

for pt in pts:
    for eta in etas:
        for rho in rhos:
            for jeta in jetas:
                correctionInputList.append(
                    {
                        "JetPt":float(pt),
                        "JetEta":eta,
                        "Rho":rho,
                        "JetA":jeta,
                    })



#exit(0)
JECParamsIndiv = [ROOT.JetCorrectorParameters("{}_{}.txt".format(args.inputTXT,lvl),"")  for lvl in correctionLevels]

cset = core.CorrectionSet.from_file(inputJSON)

for idx,JECParams in enumerate(JECParamsIndiv):
    sf=cset["{}_{}".format(baseInputName, correctionLevels[idx])]
    vPar = ROOT.vector(ROOT.JetCorrectorParameters)()
    vPar.push_back(JECParams)
    JetCorrector = ROOT.FactorizedJetCorrector(vPar)
    
    print("Comparing correctionlib vs. CMSSW for {}_{}:".format(baseInputName, correctionLevels[idx]))
    testCMSSWVsCorrectionlib(correctionInputList,JetCorrector,sf)    
    


sf = cset.compound["{}_{}_L1L2L3Res".format(baseInputName,args.AlgoType)]
vPar = ROOT.vector(ROOT.JetCorrectorParameters)()
for JECParams in JECParamsIndiv: vPar.push_back(JECParams)
#vPar.push_back(JECParamsIndiv[0])
#vPar.push_back(JECParamsIndiv[1])
#vPar.push_back(JECParamsIndiv[2])
JetCorrector = ROOT.FactorizedJetCorrector(vPar)
print("Comparing correctionlib vs. CMSSW for {}:".format(sf.name))
testCMSSWVsCorrectionlib(correctionInputList,JetCorrector,sf)    




