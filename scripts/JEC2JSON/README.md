# JSON JECs

This is a selection of scripts to transform the JEC txt files to the generic X-POG JSON format and perform a basic validation of the transformation.

## Installation

We need a recent CMSSW (>=11_2) for Python3-support in the associated ROOT and [correctionlib](https://github.com/nsmith-/correctionlib) for the JSON scale factor library.

At the time of writing this recipe works fine:
```bash
cmsrel CMSSW_11_2_0_pre10
cd CMSSW_11_2_0_pre10/src
cmsenv
git clone --recursive git@github.com:nsmith-/correctionlib.git
#in case you haven't set up your github you may fall back to
#git clone --recursive https://github.com/nsmith-/correctionlib.git
cd correctionlib
#dirty local installation of the latest version (better to use a plain "python3 -m pip install correctionlib --user" once schemav2 is available there)
echo "version = '0.0.0'" > correctionlib/src/correctionlib/version.py
python3 -m pip install . --user
cd $CMSSW_BASE/src
scram b
#to get a snapshot of the current version of the scripts without checking out the [HUGE] JECDatabase
wget https://github.com/cms-jet/JECDatabase/raw/master/scripts/JEC2JSON/JEC2JSON.py
wget https://github.com/cms-jet/JECDatabase/raw/master/scripts/JEC2JSON/testJECJSON.py
```

## Usage

For a given JEC-txt file `JECDummy.txt`, the conversion works as follows:
```bash
python3 JEC2JSON.py JECDummy.txt
python3 testJECJSON.py JECDummy.txt
```
JEC2JSON.py will by default output a JECDummy.txt.json file.
testJECJSON.py will by default read in JECDummy.txt and JECDummy.txt.json

Example (assuming that JECDatabase is not checked out...):
```bash
cd $CMSSW_BASE/src
wget https://github.com/cms-jet/JECDatabase/raw/master/textFiles/Summer19UL16APV_V2_MC/Summer19UL16APV_V2_MC_L1FastJet_AK4PFchs.txt
wget https://github.com/cms-jet/JECDatabase/raw/master/scripts/JEC2JSON/JEC2JSON.py
wget https://github.com/cms-jet/JECDatabase/raw/master/scripts/JEC2JSON/testJECJSON.py
python3 JEC2JSON.py Summer19UL16APV_V2_MC_L1FastJet_AK4PFchs.txt
python3 testJECJSON.py Summer19UL16APV_V2_MC_L1FastJet_AK4PFchs.txt
#Expected output: Differences only for eta=5.191 bin edge
```

## Known issues/caveats
- No "factorized jet corrector" functionality, only individual correction levels so far
- Stub usage of "name" and "description" functionality (only dumping input JEC-txt-file)
- Single vs. double floating point precision related differences in JEC-calculation (CMSSW JetCorrectorParameters uses C-floats)
- Different behavior at least at the upper end of the last bin (JSON-evaluator: out of range; CMSSW: evaluated at last bin), e.g. eta=+5.191 for many JEC txt-files
