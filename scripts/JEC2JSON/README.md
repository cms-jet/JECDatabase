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
```

## Usage

The tool selection expects the JER/JEC files to be available as tarballs from the JEC/JR-databases on github. You can modify the behavior by editing createJSONs.py, giving the list of parameters to be merged into subcategory, and then "per-year" files. An example to create the 2018_JERC_JSON file is given below. Uncertainty sources are only saved for the MC-tag.
```
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

createSingleYearJSON(JER2018,JEC2018,algosToConsider,"2018_JERC_All")
```

To create the JSON-files and summary html files for all three years for AK4PFchs and AK8PFPuppi you may simply run
```bash
python3 createJSONs.py
```

## Known issues/caveats remaining after arrival of schema v2
- Small inconsistency for JR-factors at (eta) bin edges due to inconistent handling (JEC and JSON uniform vs. JR code including lower and upper edge of bins). To be addressed in a PR
- Uncertainty sources takes up a lot of space. Needs formularef to emulate uncertainty-code interpolation for each pt/eta-bin + many sources. Close to 50MB for all sources when JSON not compressed
- Todo: Use formularef also for regular JEC, if applicable
- Single vs. double floating point precision related differences in JEC-calculation (CMSSW JetCorrectorParameters uses C-floats) - differences generally very small
- correctionlib doesn't support TMath::XXX namespace. Currently only implemented replacement for "TMath::Log"-->"log", but there are other occurences of TMath in [very] old JEC txt-files. More replacements can be added as the conversion happens and TMath::XXX shouldgenerally be avoided in new JEC txt files.


