
#---------------------------------------------------
# conddb --db Winter25Prompt25_V1_MC.db search Jet
# conddb --db Winter25Prompt25_V1_MC.db dump PAYLOADNAME
#---------------------------------------------------

import FWCore.ParameterSet.Config as cms

process = cms.Process("myprocess")
process.load("CondCore.CondDB.CondDB_cfi")

process.maxEvents = cms.untracked.PSet(
  input = cms.untracked.int32(1)
)

process.source = cms.Source("EmptySource")

process.jec = cms.ESSource("PoolDBESSource",
  DBParameters = cms.PSet(
    messageLevel = cms.untracked.int32(0)
  ),
  toGet = cms.VPSet(
    cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag    = cms.string('JetCorrectorParametersCollection_Winter25Prompt25_V1_MC_AK8PFPuppi'),
        label  = cms.untracked.string('AK8PFPuppi')
      ),
  ),
  connect = cms.string('sqlite:Winter25Prompt25_V1_MC.db')
)
process.es_prefer_jec = cms.ESPrefer("PoolDBESSource","jec")

process.demo1 = cms.EDAnalyzer('JetCorrectorDBReader',
  payloadName    = cms.untracked.string('AK8PFPuppi'),
  printScreen    = cms.untracked.bool(True),
  createTextFile = cms.untracked.bool(False),
  globalTag      = cms.untracked.string('')# What is this for?
)
process.p = cms.Path(process.demo1)

