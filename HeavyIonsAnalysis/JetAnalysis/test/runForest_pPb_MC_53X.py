import FWCore.ParameterSet.Config as cms
process = cms.Process('HiForest')
process.options = cms.untracked.PSet(
    # wantSummary = cms.untracked.bool(True)
    #SkipEvent = cms.untracked.vstring('ProductNotFound')
)

#####################################################################################
# HiForest labelling info
#####################################################################################

process.load("CmsHi.JetAnalysis.HiForest_cff")
process.HiForest.inputLines = cms.vstring("HiForest V3",)
import subprocess
version = subprocess.Popen(["(cd $CMSSW_BASE/src && git describe --tags)"], stdout=subprocess.PIPE, shell=True).stdout.read()
if version == '':
    version = 'no git info'
process.HiForest.HiForestVersion = cms.untracked.string(version)

#####################################################################################
# Input source
#####################################################################################

process.source = cms.Source("PoolSource",
                            duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
                            fileNames = cms.untracked.vstring("file:input.root"))

# Number of events we want to process, -1 = all events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1))


#####################################################################################
# Load Global Tag, Geometry, etc.
#####################################################################################

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.ReconstructionHeavyIons_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')

# PbPb 53X MC
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'STARTHI53_V28::All', '')

from HeavyIonsAnalysis.Configuration.CommonFunctions_cff import *
overrideGT_pPb5020(process)
overrideJEC_pp2760(process)

process.HeavyIonGlobalParameters = cms.PSet(
    centralityVariable = cms.string("HFtowersTrunc"),
    nonDefaultGlauberModel = cms.string("Hijing"),
    centralitySrc = cms.InputTag("hiCentrality")
    )

#####################################################################################
# Define tree output
#####################################################################################

process.TFileService = cms.Service("TFileService",
                                   fileName=cms.string("HiForest.root"))

#####################################################################################
# Additional Reconstruction and Analysis: Main Body
#####################################################################################

process.load('Configuration.StandardSequences.Generator_cff')
process.load('RecoJets.Configuration.GenJetParticles_cff')
process.load('RecoHI.HiJetAlgos.HiGenJets_cff')
process.load('RecoHI.HiJetAlgos.HiRecoJets_cff')
process.load('RecoHI.HiJetAlgos.HiRecoPFJets_cff')

#process.hiGenParticles.srcVector = cms.vstring('generator')

process.load('CmsHi.JetAnalysis.jets.HiGenJetsCleaned_cff')
process.load('CmsHi.JetAnalysis.jets.ak5PFJetSequence_pPb_mc_cff')
process.load('CmsHi.JetAnalysis.jets.akPu5PFJetSequence_pPb_mc_cff')

process.load('CmsHi.JetAnalysis.jets.ak5CaloJetSequence_pPb_mc_cff')
process.load('CmsHi.JetAnalysis.jets.akPu5CaloJetSequence_pPb_mc_cff')

process.load('CmsHi.HiHLTAlgos.hievtanalyzer_mc_cfi')
process.load('CmsHi.JetAnalysis.HiGenAnalyzer_cfi')

process.temp_step = cms.Path(process.hiGenParticlesForJets
                             *
                             process.ak6HiGenJets +
                             process.ak7HiGenJets)

process.ana_step = cms.Path(process.heavyIon*
                            process.hiEvtAnalyzer*
                            process.HiGenParticleAna*
                            process.hiGenJetsCleaned
                            +
                            process.ak5CaloJetSequence
                            +
                            process.akPu5CaloJetSequence
                            +
                            process.ak5PFJetSequence
                            +
                            process.akPu5PFJetSequence
                            )

process.load('CmsHi.HiHLTAlgos.hltanalysis_cff')
process.hltanalysis.hltresults = cms.InputTag("TriggerResults","","HLT")
#process.hltanalysis.hltresults = cms.InputTag("TriggerResults","","HISIGNAL")
process.skimanalysis.hltresults = cms.InputTag("TriggerResults","","HiForest")

process.hltAna = cms.Path(process.hltanalysis)
process.pAna = cms.EndPath(process.skimanalysis)
