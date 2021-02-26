import ROOT
import correctionlib._core as core
from correctionlib import schemav2 as schema
import argparse
from statistics import mean, median, stdev

parser = argparse.ArgumentParser()
parser.add_argument("inputTXT", help = "path to input JEC txt-file")
parser.add_argument("-i", "--inputJSON", help = "define path for input JSON (default: inputTXT + \".json\")")
args = parser.parse_args()
inputJSON = args.inputTXT + ".json"
if args.inputJSON!=None: inputJSON= args.inputJSON


JECParams =  ROOT.JetCorrectorParameters(args.inputTXT,"")
#copied this from writeout, better to have input list exposed by correctionlib CorrectionSet 
inputsneeded = set() #we only need the input variables set once, even if used multiple times (binning and formula-input), so filter out overlap 
for i in range(0,JECParams.definitions().nParVar()): inputsneeded.add(JECParams.definitions().parVar(i)) 
for i in range(0,JECParams.definitions().nBinVar()): inputsneeded.add(JECParams.definitions().binVar(i)) 
inputsneeded = list(sorted(inputsneeded))
print(inputsneeded)

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



cset = core.CorrectionSet.from_file(inputJSON)
for corr in cset:
    print(corr)

sf = cset["JEC"]

vPar = ROOT.vector(ROOT.JetCorrectorParameters)()
vPar.push_back(JECParams)
JetCorrector = ROOT.FactorizedJetCorrector(vPar)
def getCorrection(pt,eta,rho,area,corrector=None):
    if corrector == None: raise RuntimeError('Configuration not supported')
    corrector.setJetEta(eta)
    corrector.setJetPt(pt)
    corrector.setJetA(area)
    corrector.setRho(rho)
    corr = corrector.getCorrection()
    return corr
    
correctionInputs= {
"JetPt":3.,
"JetEta":0.,
"Rho":10.,
"JetA":0.5,
}

reldifferences = []

for test in correctionInputList:
    CMSSWresult = getCorrection(test["JetPt"],
                                test["JetEta"],
                                test["Rho"],
                                test["JetA"],
                                JetCorrector)

    evaluateList = [test[key] for key in inputsneeded]
    JSONresult = sf.evaluate(*evaluateList)
    reldifference= 100*(JSONresult-CMSSWresult)/CMSSWresult
    reldifferences.append(reldifference)
    if abs(reldifference)>1e-4: print("pt {} eta{} rho {} JetA {}; JSON: {}; CMSSW: {}; relative difference [%] (100*(J-C)/C): {}".format(test["JetPt"], test["JetEta"], test["Rho"], test["JetA"], JSONresult, CMSSWresult, 100*(JSONresult-CMSSWresult)/CMSSWresult))    
    #print("pt {} eta{} rho {} JetA {}; JSON: {}; CMSSW: {}; relative difference [%] (100*(J-C)/C): {}".format(test["JetPt"], test["JetEta"], test["Rho"], test["JetA"], JSONresult, CMSSWresult, 100*(JSONresult-CMSSWresult)/CMSSWresult))    

print("reldifferences max: {}; median: {}; mean: {}; stddev: {}".format(max(reldifferences), median(reldifferences), mean(reldifferences),stdev(reldifferences)))




