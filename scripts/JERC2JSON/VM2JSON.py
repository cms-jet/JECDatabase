## Author: Garvita Agarwal   Created: 15th November 2022

import json
import correctionlib
import uproot
import correctionlib.schemav2 as schema
from correctionlib.schemav2 import CorrectionSet, Correction
import correctionlib.convert as convert
import gzip
import subprocess
import glob
import os

vetomaps = [ "Winter22Run3",
           # "Summer19UL18_V1"
           ]
rootFiles = {}

for p in vetomaps:
    subprocess.Popen("svn export --force https://github.com/cms-jet/JECDatabase/trunk/jet_veto_maps/{}".format(p), stdout=subprocess.PIPE, shell=True)
    filelist = glob.glob(p + "/*.root")
    keys = [filename.split(p+"/")[1].split(".root")[0].split("_v")[0] for filename in filelist]
    rootFiles[p] = dict(zip(keys, filelist))
print("Converting veto maps for the following into JSON: ", rootFiles)

def getContent(vetomaps, year, hname):
    file = uproot.open(vetomaps[year])
    h = file[hname].to_hist()
    X, Y = h.axes.edges
    values = list((h.values()).flatten())
    output = schema.MultiBinning.parse_obj({
            "inputs":["eta","phi"],
            "nodetype": "multibinning",
            "edges": [
                list(X.flatten()),
                list(Y.flatten()),
            ],
            "content": values,
            "flow": 'error',
        })
    return output

def getVetoMap(vetomaps):
    output = schema.Category.parse_obj({
                "nodetype": "category",
                "input": "year",
                "content":[
                    schema.CategoryItem.parse_obj({
                        "key": year, 
                        "value": schema.Category.parse_obj({
                            "nodetype": "category",
                            "input": "hname",
                            "content":[
                                schema.CategoryItem.parse_obj({
                                        "key": hname.split(";")[0], 
                                        "value": getContent(vetomaps, year, hname)})
                                for hname in uproot.open(vetomaps[year]).keys()
                                ],
                            })
                    })
                    for year in vetomaps.keys()
                ],
    })
    return output

def main():
    for p in vetomaps:
        name        = p + "_JetVetoMaps"
        print("\n Writing jet veto maps for {} into JSON...".format(p))
        description = "These are the jet veto maps showing regions with an excess of jets (hot zones) and lack of jets (cold zones). Using the phi-symmetry of the CMS detector, these areas with\
                       detector and or calibration issues can be pinpointed."
        version     = 1
        inputs      = [{"name": "year","type" : "string", "description": "year/scenario: example Winter22_RunCD etc"},
                       {"name": "hname","type": "string", "description": "name of the type of veto map: example 'jetvetomap' etc"},
                       {"name": "eta", "type" : "real", "description"  : "jet eta"},
                       {"name": "phi", "type" : "real", "description"  : "jet phi"},
                      ]
        output      = {"name"      : "vetomaps",
                       "type"       : "real",
                       "description": "Non-zero value for (eta, phi) indicates that the region is vetoed."}
        corr = Correction.parse_obj({
            "version"     : version,
            "name"        : name,
            "description" : description,
            "inputs"      : inputs,
            "output"      : output,
            "data"        : getVetoMap(rootFiles[p]),
            })
        print("These are the jet veto maps for {}".format(list(rootFiles[p].keys())))

        cset = CorrectionSet(schema_version=2,
                             corrections=[corr],
                             description="These are the jet veto maps for {}".format(list(rootFiles[p].keys())))
        outName = p + "_jetvetomaps.json"
        os.system("rm " + outName)
        with open( outName, "w") as fout:
            fout.write(cset.json(exclude_unset=True, indent=2))
            print("JSON for {} written at {}.".format(p, outName))
        os.system("rm {}.gz".format(outName))
        print("rm {}.gz".format(outName))
        print("gzip {}".format(outName))
        os.system("gzip " + outName)

if __name__ == "__main__":
    main()
