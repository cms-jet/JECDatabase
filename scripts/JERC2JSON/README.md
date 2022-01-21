# JSON JECs

This is a selection of scripts to transform the JEC txt files to the generic X-POG JSON format and perform a basic validation of the transformation.

## Installation

We need a recent CMSSW (>=11_2) for Python3-support in the associated ROOT and [correctionlib](https://github.com/nsmith-/correctionlib) for the JSON scale factor library. Ideally one uses a post July 12X-release, which includes the fix addressing https://github.com/cms-sw/cmssw/issues/34381

At the time of writing this recipe works fine:
```bash
cmsrel CMSSW_12_1_1
cd CMSSW_12_1_1/src
cmsenv
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools # for tests
python3 -m pip install --user git+https://github.com/cms-nanoAOD/correctionlib.git #latest version from master
cd $CMSSW_BASE/src
scram b
#to get a snapshot of the current version of the scripts without checking out the [HUGE] JECDatabase
wget https://github.com/cms-jet/JECDatabase/raw/master/scripts/JEC2JSON/JER2JSON.py
wget https://github.com/cms-jet/JECDatabase/raw/master/scripts/JEC2JSON/JEC2JSON.py
wget https://github.com/cms-jet/JECDatabase/raw/master/scripts/JEC2JSON/JERCHelpers.py
wget https://github.com/cms-jet/JECDatabase/raw/master/scripts/JEC2JSON/createJSONs.py
wget https://github.com/cms-jet/JECDatabase/raw/master/scripts/JEC2JSON/testJERCJSON.py
wget https://github.com/cms-jet/JECDatabase/raw/master/scripts/JEC2JSON/miniDemo.py
```

## Usage

The tool collection expects the JER/JEC files to be available as tarballs from the JEC/JR-databases on github. You can modify the behavior by editing JERCHelpers.py and creatJSONs.py, giving the list of parameters to be merged into subcategory, and then "per-year" files. An example to create the 2018_JERC_JSON file is given below. Uncertainty sources are only saved for the MC-tag.
```
######################
#JERCHelpers.py part #
######################
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

######################
#createJSONs.py part #
######################
createSingleYearJSON(JER2018,JEC2018,algosToConsider,"2018_JERC_All")
```

To create the JSON-files and summary html files for all three years for AK4PFchs and AK8PFPuppi you may simply run
```bash
python3 createJSONs.py
```

## Example usage CMMSW vs. JSON with created files (see also directly minimalDemo.py)
After running the creation of JSON files the example below runs out of the box. If txt-files/JSON files reside elsewhere you can still adapt to your need from the minimal examples here, always showing the CMSSW and corretionlib way. For the CMSSW-resolution objects we rely on the python bindings provided by NanoAODTools.
```
import ROOT
import correctionlib._core as core
jec,algo,lvl,unc=("Summer19UL16_V7_MC","AK4PFchs","L2Relative","Total")
pt,eta,rho,area=(100.,0.,15.,.5)
print("\JEC Parameters: ", jec, algo, lvl, unc,  pt, eta, rho, area)

print("\n\nSingle JEC level:\n===================")
#CMSSW (JEC,single)
print("Opening {}/{}_{}_{}.txt".format(jec,jec,lvl,algo))
vPar = ROOT.vector(ROOT.JetCorrectorParameters)()
vPar.push_back(ROOT.JetCorrectorParameters("{}/{}_{}_{}.txt".format(jec,jec,lvl,algo),""))
JetCorrector = ROOT.FactorizedJetCorrector(vPar)
JetCorrector.setJetEta(eta)
JetCorrector.setJetPt(pt)
print("CMSSW result: {}".format(JetCorrector.getCorrection()))

#JSON (JEC,single)
cset = core.CorrectionSet.from_file("2016_JERC_All.json.gz")
print("JSON access to: {}_{}_{}".format(jec, lvl, algo))
sf=cset["{}_{}_{}".format(jec, lvl, algo)]
print([input.name for input in sf.inputs])
print("JSON result: {}".format(sf.evaluate(*[eta,pt])))


print("\n\nCompound JEC:\n===================")
correctionLevels = ["L1FastJet",
                    "L2Relative",
                    "L3Absolute",
                    "L2L3Residual",
                ]
#CMSSW (JEC,compound)
vPar = ROOT.vector(ROOT.JetCorrectorParameters)()
for level in correctionLevels: vPar.push_back(ROOT.JetCorrectorParameters("{}/{}_{}_{}.txt".format(jec,jec,level,algo),""))
CompoundJetCorrector = ROOT.FactorizedJetCorrector(vPar)
CompoundJetCorrector.setJetEta(eta)
CompoundJetCorrector.setJetPt(pt)
CompoundJetCorrector.setJetA(area)
CompoundJetCorrector.setRho(rho)
print("CMSSW result: {}".format(CompoundJetCorrector.getCorrection()))


#JSON (JEC,compound)
sf=cset.compound["{}_{}_{}".format(jec, "L1L2L3Res", algo)]
print([input.name for input in sf.inputs])
print("JSON result: {}".format(sf.evaluate(*[area,eta,pt,rho])))


print("\n\n JECSource:\n===========")
#CMSSW (JECSource)
TotalUncertainty=ROOT.JetCorrectionUncertainty(ROOT.JetCorrectorParameters("{}/{}_UncertaintySources_{}.txt".format(jec,jec,algo),unc))
TotalUncertainty.setJetEta(eta)
TotalUncertainty.setJetPt(pt)
print("CMSSW result: {}".format(TotalUncertainty.getUncertainty(True)))

#JSON (JECSource)
sf=cset["{}_{}_{}".format(jec, unc, algo)]
print([input.name for input in sf.inputs])
print("JSON result: {}".format(sf.evaluate(*[eta,pt])))


jer,algo,syst=("Summer20UL16_JRV3_MC","AK4PFchs","nom")
pt,eta,rho=(100.,0.,15.)
print("\n\n JER parameters: ", jer, algo, lvl, syst,  pt, eta)

print("\n\n JER SF:\n=========")
#CMSSW (JER scale factor)
jerSF_and_Uncertainty = ROOT.PyJetResolutionScaleFactorWrapper("{}/{}_SF_{}.txt".format(jer,jer,algo))
params_sf_and_uncertainty = ROOT.PyJetParametersWrapper()
params_sf_and_uncertainty.setJetEta(eta)
params_sf_and_uncertainty.setJetPt(pt)
idx=0
if syst=="up": idx=2
elif syst=="down": idx=1
elif syst=="nom": idx=0
else: raise RuntimeError('systematic variation not supported')
print("CMSSW result: {}".format(jerSF_and_Uncertainty.getScaleFactor(params_sf_and_uncertainty,idx)))

#JSON (JER scale factor)
sf=cset["{}_ScaleFactor_{}".format(jer, algo)]
print([input.name for input in sf.inputs])
print("JSON result: {}".format(sf.evaluate(*[eta,syst])))


print("\n\n PtResolution:\n==============")
ResolutionChoice="PtResolution"
#CMSSW (JER Resolution)
jerobj = ROOT.PyJetResolutionWrapper("{}/{}_{}_{}.txt".format(jer,jer,ResolutionChoice,algo))
params_resolution = ROOT.PyJetParametersWrapper()
params_resolution.setJetEta(eta)
params_resolution.setJetPt(pt)
params_resolution.setRho(rho)
print("CMSSW result: {}".format(jerobj.getResolution(params_resolution)))


#JSON (JER scale factor)
sf=cset["{}_{}_{}".format(jer, ResolutionChoice, algo)]
print([input.name for input in sf.inputs])
print("JSON result: {}".format(sf.evaluate(*[eta,pt,rho])))
```



## Known issues/caveats remaining after arrival of schema v2
- Small inconsistency for JR-factors at (eta) bin edges due to inconistent handling (JEC and JSON uniform vs. JR code including lower and upper edge of bins). Addressed in a PR to CMSSW (https://github.com/cms-sw/cmssw/pull/36759)
- Single vs. double floating point precision related differences in JEC-calculation (CMSSW JetCorrectorParameters uses C-floats) - differences generally very small
- correctionlib doesn't support TMath::XXX namespace. Currently only implemented replacement for "TMath::Log/Power/Max"-->"log/pow/max", but there are other occurences of TMath in [very] old JEC txt-files. More replacements can be added as the conversion happens and TMath::XXX shouldgenerally be avoided in new JEC txt files.
## Possible next improvements
- Uncertainty sources takes up a lot of space. Needs formularef to emulate uncertainty-code interpolation for each pt/eta-bin + many sources. Close to 50MB for all sources when JSON not compressed
- Use formularef also for regular JEC, if applicable


