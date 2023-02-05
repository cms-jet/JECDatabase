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

vetomaps = ["Winter22Run3",
            "Summer19UL18_V1",
            "Summer19UL17_V2",
            "Summer19UL16_V0"
           ]
arrFiles = []
for p in vetomaps:
    rootFile ={}
    subprocess.Popen("svn export --force https://github.com/cms-jet/JECDatabase/trunk/jet_veto_maps/{}".format(p), stdout=subprocess.PIPE, shell=True)
    filelist = glob.glob(p + "/" + p + "*.root")
    keys = [filename.split(p+"/")[1].rsplit("_", 1)[0] for filename in filelist]
    for k, f in zip(keys, filelist):
        rootFile[k+"_V1"] = f
    arrFiles.append(rootFile)
print("Converting veto maps for the following into JSON: \n")
print(json.dumps(arrFiles, indent = 2))

def getContent(vetomaps, hname):
    file = uproot.open(vetomaps)
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

def main():
    for rootFiles in arrFiles:
        corrs=[]
        for p in rootFiles.keys():
            print(p)
            name        = p
            description = "These are the jet veto maps showing regions with an excess of jets (hot zones) and lack of jets (cold zones). Using the phi-symmetry of the CMS detector, these areas with detector and or calibration issues can be pinpointed."
            version     = 1
            inputs      = [
                           {"name": "type","type": "string", "description": "name of the type of veto map. The recommended map for analyses is 'jetvetomap'."},
                           {"name": "eta", "type" : "real", "description"  : "jet eta"},
                           {"name": "phi", "type" : "real", "description"  : "jet phi"},
                          ]
            output      = {"name"      : "vetomaps",
                           "type"       : "real",
                           "description": "Non-zero value for (eta, phi) indicates that the region is vetoed."}
            data        = schema.Category.parse_obj({"nodetype": "category",
                                                     "input": "type",
                                                     "content":[
                                                         schema.CategoryItem.parse_obj({
                                                             "key": hname.split(";")[0],
                                                             "value": getContent(rootFiles[p], hname)})
                                                         for hname in uproot.open(rootFiles[p]).keys()
                                                     ],
                                                    })
            corr = Correction.parse_obj({
                "version"     : version,
                "name"        : name,
                "description" : description,
                "inputs"      : inputs,
                "output"      : output,
                "data"        : data,
                })
            print("These are the jet veto maps for {}".format(p))
            corrs.append(corr)
        cset = CorrectionSet(schema_version=2,
                             corrections=corrs,
                             description="These are the jet veto maps for {}. The recommended veto maps to be applied to both data and MC for analysis is 'jetvetomap'.".format(list(rootFiles.keys())))

        p = "vetomapsJSON/" + p
        os.system("mkdir -p " + p)
        outName = p + "/jetvetomaps.json"
        os.system("rm " + outName)
        with open( outName, "w") as fout:
            fout.write(cset.json(exclude_unset=True, indent=2))
            print("JSON for {} written at {}.".format(p, outName))
        os.system("rm {}.gz".format(outName))
        print("rm {}.gz".format(outName))
        print("gzip {}".format(outName))
        os.system("gzip " + outName)
        print("#### Compressed and done writing {}.json.gz \n".format(outName))

if __name__ == "__main__":
    main()
