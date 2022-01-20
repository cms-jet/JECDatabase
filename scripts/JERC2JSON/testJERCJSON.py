import ROOT
import correctionlib._core as core
from correctionlib import schemav2 as schema
import argparse
import textwrap
from statistics import mean, median, stdev
import itertools
import os
import correctionlib

from JERCHelpers import *

print(correctionlib.__version__)

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    epilog=textwrap.dedent('''\
    Default behavior without arguments:
    Run over all the configs defined in JERCHelpers.py and check all inputs:
       For JEC: L1/L2/L3/L2L3Residual + compound corrections + uncertainties (for MC only) will be tested against the merged JSON of each year
       For JER: Eta/Pt/Phi Resolution and ScaleFactor will be tested against the merged JSON of each year
         '''))
parser.add_argument("-i","--inputTXT", 
                    help = "(optional) base name of JEC or JER txt-files (e.g. Summer19UL16APV_V2_MC or Summer19UL16APV_JRV3_MC); For JEC: L1/L2/L3/L2L3Residual + compound corrections + uncertainties (for MC only) will be tested against a given JSON; For JER: Eta/Pt/Phi Resolution and ScaleFactor will be tested against a given JSON")
parser.add_argument("-j", "--inputJSON", help = " (optional) define path for input JSON")
parser.add_argument("-a", "--AlgoType", default="AK4PFchs", help = "(optional) define jet type for which JSON is created")
args = parser.parse_args()

pts  = [-1.] + [(10**(x)) for x in range(-1,5)]
etas = [-10.,-5.191, -4.889, -2.,0.,1.305, 2.99, 3., 3.01, 5.191, 5.192]
rhos = [-1., 5., 10., 50.]
jetas = [-1., 0.5,1.,5.]
systs = ["nom","up","down"]

#smaller subsets for checks to speed up the checks
#pts  =  [(10**(x)) for x in range(-1,4)]
#pts  =  [1.,7.,8.,9.,10.,11.,100.,1000.,5000.,6000.,7000.,10000.]
#etas = [-4.889, -2.,0.,1.305, 3., 5.191]
#etas = [-3.01,-3.,-2.99,2.99,3.,3.01]
#rhos = [5.]
#jetas = [1.]

correctionInputList = []

for pt in pts:
    for eta in etas:
        for rho in rhos:
            for jeta in jetas:
                for syst in systs:
                    correctionInputList.append(
                        {
                            "JetPt":float(pt),
                            "JetEta":eta,
                            "Rho":rho,
                            "JetA":jeta,
                            "systematic":syst,
                        })


def testSingleYearJSON(jerList, jecList, algosToConsider, combinedJsonName):
    jerAlgoList = list(itertools.product(jerList, algosToConsider))
    jecAlgoList = list(itertools.product(jecList, algosToConsider))
    print(jerAlgoList, jecAlgoList)
    cset = core.CorrectionSet.from_file(combinedJsonName)

    for p in jecAlgoList:
        jec,algo=p
        print(jec, algo)
        for lvl in correctionLevels: print("Opening {}/{}_{}_{}.txt".format(jec,jec,lvl,algo))
        JECParamsIndiv = [ROOT.JetCorrectorParameters("{}/{}_{}_{}.txt".format(jec,jec,lvl,algo),"")  for lvl in correctionLevels]
        for idx,JECParams in enumerate(JECParamsIndiv):
            print("JSON access to: {}_{}_{}".format(jec, correctionLevels[idx], algo))
            sf=cset["{}_{}_{}".format(jec, correctionLevels[idx], algo)]
            vPar = ROOT.vector(ROOT.JetCorrectorParameters)()
            vPar.push_back(JECParams)
            JetCorrector = ROOT.FactorizedJetCorrector(vPar)
            
            print("Comparing correctionlib vs. CMSSW for {}_{}_{}:".format(jec, correctionLevels[idx], algo))
            testCMSSWVsCorrectionlib(correctionInputList,JetCorrector,sf)    

        #compound
        sf = cset.compound["{}_L1L2L3Res_{}".format(jec,algo)]
        vPar = ROOT.vector(ROOT.JetCorrectorParameters)()
        for JECParams in JECParamsIndiv: vPar.push_back(JECParams)
        JetCorrector = ROOT.FactorizedJetCorrector(vPar)
        print("Comparing correctionlib vs. CMSSW for {}:".format(sf.name))
        testCMSSWVsCorrectionlib(correctionInputList,JetCorrector,sf,testVariant="Correction")

        #Uncertainty (only total checked for consistency)
        if "MC" in jec:
            TotalUncertainty=ROOT.JetCorrectionUncertainty(ROOT.JetCorrectorParameters("{}/{}_UncertaintySources_{}.txt".format(jec,jec,algo),"Total"))
            sf = cset["{}_Total_{}".format(jec,algo)]
            print("Comparing correctionlib vs. CMSSW for {}:".format(sf.name))
            testCMSSWVsCorrectionlib(correctionInputList,TotalUncertainty,sf,testVariant="Uncertainty")    
    
    for p in jerAlgoList:
        jer,algo=p
        for lvl in resolutionLevels:
            print("Opening {}/{}_{}_{}.txt".format(jer,jer,lvl,algo))
            
            if "ScaleFactor" in lvl:
                print("Testing ScaleFactor")
                jerSF_and_Uncertainty = ROOT.PyJetResolutionScaleFactorWrapper("{}/{}_SF_{}.txt".format(jer,jer,algo))
                sf = cset["{}_ScaleFactor_{}".format(jer,algo)]
                testCMSSWVsCorrectionlib(correctionInputList,jerSF_and_Uncertainty,sf,testVariant="ScaleFactor")
                
            else:
                jerobj = ROOT.PyJetResolutionWrapper("{}/{}_{}_{}.txt".format(jer,jer,lvl,algo))
                sf = cset["{}_{}_{}".format(jer,lvl,algo)]
                testCMSSWVsCorrectionlib(correctionInputList,jerobj,sf,testVariant="Resolution")



if os.path.isfile("testJSONlog.txt"):
    os.remove("testJSONlog.txt") #clear log-file for testing.

if args.inputTXT is not None and args.inputJSON is not None:
    print("Will check individual correction instead of full-scale test of JSON")
    if "_JRV" in args.inputTXT:
        testSingleYearJSON([args.inputTXT], [], [args.AlgoType], args.inputJSON)
    else:
        testSingleYearJSON([], [args.inputTXT], [args.AlgoType], args.inputJSON)
    exit(0)
    


testSingleYearJSON(JER2016,JEC2016,algosToConsider,"2016_JERC_All.json.gz")
testSingleYearJSON(JER2017,JEC2017,algosToConsider,"2017_JERC_All.json.gz")
testSingleYearJSON(JER2018,JEC2018,algosToConsider,"2018_JERC_All.json.gz")



#exit(0)

#Summer19UL16APV_RunBCD_V7_DATA_UncertaintySources_AK4PFchs.txt


#print("Testing resolution")


#import correctionlib.highlevel

#uncsetforJSON = correctionlib.highlevel.CorrectionSet("merged.json")

#with gzip.open("mergedNew.json.gz", "wt") as fout:
#    fout.write(uncsetforJSON.json(exclude_unset=True))
