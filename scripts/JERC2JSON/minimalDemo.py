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
cset = core.CorrectionSet.from_file("2016postVFP_UL/UL16postVFP_jerc.json.gz")#2016_JERC_All.json.gz")
print("JSON access to: {}_{}_{}".format(jec, lvl, algo))
sf=cset["{}_{}_{}".format(jec, lvl, algo)]
print([input.name for input in sf.inputs])
print("JSON result: {}".format(sf.evaluate(eta,pt)))


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
print("JSON result: {}".format(sf.evaluate(area,eta,pt,rho)))


print("\n\n JECSource:\n===========")
#CMSSW (JECSource)
TotalUncertainty=ROOT.JetCorrectionUncertainty(ROOT.JetCorrectorParameters("{}/{}_UncertaintySources_{}.txt".format(jec,jec,algo),unc))
TotalUncertainty.setJetEta(eta)
TotalUncertainty.setJetPt(pt)
print("CMSSW result: {}".format(TotalUncertainty.getUncertainty(True)))

#JSON (JECSource)
sf=cset["{}_{}_{}".format(jec, unc, algo)]
print([input.name for input in sf.inputs])
print("JSON result: {}".format(sf.evaluate(eta,pt)))



jer,algo,syst=("Summer20UL16_JRV3_MC","AK4PFchs","nom")
pt,pt_gen,eta,rho=(100.,98.,0.,15.)
print("\n\n JER parameters: ", jer, algo, lvl, syst,  pt, pt_gen, eta, rho)

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
print("JSON result: {}".format(sf.evaluate(eta,syst)))


print("\n\n PtResolution:\n==============")
ResolutionChoice="PtResolution"
#CMSSW (JER Resolution)
jerobj = ROOT.PyJetResolutionWrapper("{}/{}_{}_{}.txt".format(jer,jer,ResolutionChoice,algo))
params_resolution = ROOT.PyJetParametersWrapper()
params_resolution.setJetEta(eta)
params_resolution.setJetPt(pt)
params_resolution.setRho(rho)
print("CMSSW result: {}".format(jerobj.getResolution(params_resolution)))


#JSON (JER resolution)
sf=cset["{}_{}_{}".format(jer, ResolutionChoice, algo)]
print([input.name for input in sf.inputs])
print("JSON result: {}".format(sf.evaluate(eta,pt,rho)))



print("\n\n JER Smearing (JSON only):\n==============")
event_id = 999
jecFactor = cset.compound["{}_{}_{}".format(jec, "L1L2L3Res", algo)].evaluate(area,eta,pt,rho)
pt_jec = pt * jecFactor
jerpt=cset["{}_{}_{}".format(jer, ResolutionChoice, algo)].evaluate(eta,pt,rho)
ptgen = pt_gen if abs(pt_jec - pt_gen) < 3*pt_jec*jerpt else -1.0
jersf = cset["{}_ScaleFactor_{}".format(jer, algo)].evaluate(eta,syst)
jersmear = cset["JERSmear"].evaluate(pt_jec, eta, ptgen, rho, event_id, jerpt, jersf)
pt_final = pt_jec * jersmear
print("ptraw: {:.2f}; pt_jec: {:.2f}; pt_final: {:.2f}; pt_gen: {:.2f}".format(pt,pt_jec,pt_final,pt_gen))
