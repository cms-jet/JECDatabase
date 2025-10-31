
#---------------------------------------------------
# conddb --db Summer24Prompt24_V1_MC.db search Jet
# conddb --db Summer24Prompt24_V1_MC.db dump PAYLOADNAME
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
        tag    = cms.string('JetCorrectorParametersCollection_Summer22_22Sep2023_RunCD_V4_DATA_AK4PFPuppiPNetRegression'),
        label  = cms.untracked.string('AK4PFPuppiPNetRegression')
      ),
  ),
  connect = cms.string('sqlite:Summer22_22Sep2023_RunCD_V4_DATA.db')
)
process.es_prefer_jec = cms.ESPrefer("PoolDBESSource","jec")

process.demo1 = cms.EDAnalyzer('JetCorrectorDBReader',
  payloadName    = cms.untracked.string('AK4PFPuppiPNetRegression'),
  printScreen    = cms.untracked.bool(True),
  createTextFile = cms.untracked.bool(False),
  globalTag      = cms.untracked.string('')# What is this for?
)
process.p = cms.Path(process.demo1)

