# JSON JECs

This is a selection of scripts to transform the JEC txt files to the generic X-POG JSON format and perform a basic validation of the transformation.

## Installation

We need a recent CMSSW (>=11_2) for Python3-support in the associated ROOT and [correctionlib](https://github.com/nsmith-/correctionlib) for the JSON scale factor library. Ideally one uses a post July 12X-release, which includes the fix addressing https://github.com/cms-sw/cmssw/issues/34381

At the time of writing this recipe works fine:
```bash
cmsrel CMSSW_12_1_0_pre1
cd CMSSW_12_1_0_pre1/src
cmsenv
python3 -m pip install --user git+https://github.com/cms-nanoAOD/correctionlib.git
cd $CMSSW_BASE/src
scram b
#to get a snapshot of the current version of the scripts without checking out the [HUGE] JECDatabase
wget https://github.com/cms-jet/JECDatabase/raw/master/scripts/JEC2JSON/JEC2JSON.py
wget https://github.com/cms-jet/JECDatabase/raw/master/scripts/JEC2JSON/testJECJSON.py
```

## Usage

For a given collection of JEC-txt files with the base name `JECDummy`, the algorithm type "AK4PFchs", and the correction levels ["L1FastJet", "L2Relative", "L3Absolute", "L2L3Residual"], the conversion works as follows:
```bash
python3 JEC2JSON.py JECDummy
python3 testJECJSON.py JECDummy
```
JEC2JSON.py will by default output a JECDummy.json file.
testJECJSON.py will by default read in JECDummy_[all correctionlevels]_[jet type=AK4PFchs].txt and JECDummy.json

Example (assuming that JECDatabase is not checked out...):
```bash
cd $CMSSW_BASE/src
wget https://github.com/cms-jet/JECDatabase/raw/master/textFiles/Summer19UL16APV_RunBCD_V7_DATA/Summer19UL16APV_RunBCD_V7_DATA_L1FastJet_AK4PFchs.txt
wget https://github.com/cms-jet/JECDatabase/raw/master/textFiles/Summer19UL16APV_RunBCD_V7_DATA/Summer19UL16APV_RunBCD_V7_DATA_L2Relative_AK4PFchs.txt
wget https://github.com/cms-jet/JECDatabase/raw/master/textFiles/Summer19UL16APV_RunBCD_V7_DATA/Summer19UL16APV_RunBCD_V7_DATA_L3Absolute_AK4PFchs.txt
wget https://github.com/cms-jet/JECDatabase/raw/master/textFiles/Summer19UL16APV_RunBCD_V7_DATA/Summer19UL16APV_RunBCD_V7_DATA_L2L3Residual_AK4PFchs.txt
wget https://github.com/cms-jet/JECDatabase/raw/master/scripts/JEC2JSON/JEC2JSON.py
wget https://github.com/cms-jet/JECDatabase/raw/master/scripts/JEC2JSON/testJECJSON.py
python3 JEC2JSON.py Summer19UL16APV_RunBCD_V7_DATA
python3 testJECJSON.py Summer19UL16APV_RunBCD_V7_DATA
#Expected output: Three differences on level of 10e-4 % level in L1FastJet and compound correction
#For pre-July2021 pre-12X releases many differences, but only for eta=5.191 bin edge, cf. https://github.com/cms-sw/cmssw/issues/34381
```

## Known issues/caveats
- ~~No "factorized jet corrector" functionality, only individual correction levels so far~~ - working with correctionlibv2 and extended JEC2JSON
- ~~Stub usage of "name" and "description" functionality (only dumping input JEC-txt-file)~~ - name built by combining base names and correction levels (+"_L1L2L3Res") such that one could merge multiple JSONS
- ~~Different behavior at least at the upper end of the last bin (JSON-evaluator: out of range; CMSSW: evaluated at last bin), e.g. eta=+5.191 for many JEC txt-files, cf. https://github.com/cms-sw/cmssw/issues/34381~~ - resolved in post July 2021 12X-releases by PR linked in issue
- Single vs. double floating point precision related differences in JEC-calculation (CMSSW JetCorrectorParameters uses C-floats) - differences generally very small
- correctionlib doesn't support TMath::XXX namespace. Currently only implemented replacement for "TMath::Log"-->"log", but there are other occurences of TMath in [very] old JEC txt-files. More replacements can be added as the conversion happens and TMath::XXX shouldgenerally be avoided in new JEC txt files.


