import os
import FWCore.ParameterSet.Config as cms

process = cms.Process("HFA")

# ----------------------------------------------------------------------
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
#process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )


# ----------------------------------------------------------------------
# -- Database configuration
process.load("CondCore.DBCommon.CondDBCommon_cfi")
process.load("CondCore.DBCommon.CondDBSetup_cfi")

# -- Conditions
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = "GR_R_53_LV6::All"

# ----------------------------------------------------------------------
# -- Input files

process.source = cms.Source("PoolSource",
        skipEvents = cms.untracked.uint32(0),
        fileNames  = cms.untracked.vstring(
		'file:/uscms_data/d3/jiansun/data/1CC46C43-99B9-E311-B9CF-FA163E4A10E1_highpt_rereco_run181913.root'
            )
        )

process.maxEvents = cms.untracked.PSet(
        input = cms.untracked.int32(200)
        )

rootFileName = "d0.root"

process.tree = cms.EDAnalyzer(
    "HFTree",
    verbose      = cms.untracked.int32(1),
    printFrequency = cms.untracked.int32(1000),
    fileName     = cms.untracked.string(rootFileName),
    requireCand  =  cms.untracked.bool(False)
    )

# ----------------------------------------------------------------------
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("UserCode.OpenHF.HFRecoStuff_cff")
process.load("UserCode.OpenHF.HFCharm_cff")

process.d0Dump.trackPt = cms.untracked.double(1.0)
# ----------------------------------------------------------------------
process.TFileService = cms.Service("TFileService",
           fileName = cms.string('d0.root')
        )

# ----------------------------------------------------------------------
process.p = cms.Path(
    process.recoStuffSequence*
    process.d0Sequence*
    process.tree
)

