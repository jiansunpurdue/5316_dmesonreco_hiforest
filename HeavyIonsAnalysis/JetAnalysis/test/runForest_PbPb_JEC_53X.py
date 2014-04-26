#!/usr/bin/env python2
# Run the foresting configuration on PbPb in CMSSW_5_3_X, using the new HF/Voronoi jets
# Author: Alex Barbieri
# Date: 2013-10-15

hiTrackQuality = "highPurity"              # iterative tracks
#hiTrackQuality = "highPuritySetWithPV"    # calo-matched tracks

import FWCore.ParameterSet.Config as cms
process = cms.Process('HiForest')
process.options = cms.untracked.PSet(
    # wantSummary = cms.untracked.bool(True)
    #SkipEvent = cms.untracked.vstring('ProductNotFound')
)

#####################################################################################
# HiForest labelling info
#####################################################################################

process.load("HeavyIonsAnalysis.JetAnalysis.HiForest_cff")
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
                            fileNames = cms.untracked.vstring("/store/user/belt/QCD_Pt_80_TuneZ2_2p76TeV_pythia6/QCDpT80_2011RECO_STARTHI53_LV1_5_3_16_Track8_Jet22_1GeVcut/573d209b5e104c1770c264763824b971/QCDpT80_step3_RAW2DIGI_L1Reco_RECO_10_1_j5g.root"))

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
process.GlobalTag = GlobalTag(process.GlobalTag, 'STARTHI53_LV1::All', '')

from HeavyIonsAnalysis.Configuration.CommonFunctions_cff import *
overrideGT_PbPb2760(process)
overrideJEC_pp2760(process)

process.HeavyIonGlobalParameters = cms.PSet(
    centralityVariable = cms.string("HFtowers"),
    nonDefaultGlauberModel = cms.string("Hydjet_Drum"),
    centralitySrc = cms.InputTag("hiCentrality")
    )

#####################################################################################
# Define tree output
#####################################################################################

process.TFileService = cms.Service("TFileService",
                                   fileName=cms.string("hiForest_QCDpT80_STARTHI53_LV1_Track8_Jet22.root"))

#####################################################################################
# Additional Reconstruction and Analysis: Main Body
#####################################################################################

process.load('Configuration.StandardSequences.Generator_cff')
process.load('RecoJets.Configuration.GenJetParticles_cff')
#process.load('RecoHI.HiJetAlgos.HiGenJets_cff')
#process.load('RecoHI.HiJetAlgos.HiRecoJets_cff')
#process.load('RecoHI.HiJetAlgos.HiRecoPFJets_cff')

#process.hiGenParticles.srcVector = cms.vstring('generator')

process.load('HeavyIonsAnalysis.JetAnalysis.jets.HiGenJetsCleaned_JEC_cff')

process.load('HeavyIonsAnalysis.JetAnalysis.jets.akPu3CaloJetSequence_PbPb_jec_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.akVs3CaloJetSequence_PbPb_jec_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.akVs3PFJetSequence_PbPb_jec_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.akPu3PFJetSequence_PbPb_jec_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.ak3PFJetSequence_PbPb_jec_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.ak3CaloJetSequence_PbPb_jec_cff')

process.load('HeavyIonsAnalysis.JetAnalysis.jets.akPu4CaloJetSequence_PbPb_jec_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.akVs4CaloJetSequence_PbPb_jec_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.akVs4PFJetSequence_PbPb_jec_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.akPu4PFJetSequence_PbPb_jec_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.ak4PFJetSequence_PbPb_jec_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.ak4CaloJetSequence_PbPb_jec_cff')

process.load('HeavyIonsAnalysis.JetAnalysis.jets.akPu5CaloJetSequence_PbPb_jec_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.akVs5CaloJetSequence_PbPb_jec_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.akVs5PFJetSequence_PbPb_jec_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.akPu5PFJetSequence_PbPb_jec_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.ak5PFJetSequence_PbPb_jec_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.ak5CaloJetSequence_PbPb_jec_cff')

process.load('HeavyIonsAnalysis.JetAnalysis.jets.HiReRecoJets_cff')

process.jetSequences = cms.Sequence(process.hiReRecoCaloJets +
                                    process.hiReRecoPFJets +

                                    process.akPu3CaloJetSequence +
                                    process.akVs3CaloJetSequence +
                                    process.akVs3PFJetSequence +
                                    process.akPu3PFJetSequence +
                                    process.ak3PFJetSequence +                                    
                                    process.ak3CaloJetSequence +

                                    process.akPu4CaloJetSequence +
                                    process.akVs4CaloJetSequence +
                                    process.akVs4PFJetSequence +
                                    process.akPu4PFJetSequence +
                                    process.ak4PFJetSequence +
                                    process.ak4CaloJetSequence +
                                    
                                    process.akPu5CaloJetSequence +
                                    process.akVs5CaloJetSequence +
                                    process.akVs5PFJetSequence +
                                    process.akPu5PFJetSequence +
                                    process.ak5PFJetSequence +
                                    process.ak5CaloJetSequence
                                    
                                    )

process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_mc_cfi')
process.load('HeavyIonsAnalysis.JetAnalysis.HiGenAnalyzer_cfi')

#####################################################################################
# To be cleaned

process.load('HeavyIonsAnalysis.JetAnalysis.ExtraTrackReco_cff')
#process.load('HeavyIonsAnalysis.JetAnalysis.ExtraPfReco_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.TrkAnalyzers_MC_cff')
process.load("HeavyIonsAnalysis.TrackAnalysis.METAnalyzer_cff")
process.load("HeavyIonsAnalysis.JetAnalysis.pfcandAnalyzer_cfi")
process.load('HeavyIonsAnalysis.JetAnalysis.rechitanalyzer_cfi')
process.rechitAna = cms.Sequence(process.rechitanalyzer+process.pfTowers)
process.pfcandAnalyzer.skipCharged = False
process.pfcandAnalyzer.pfPtMin = 0

#####################################################################################

#########################
# Track Analyzer
#########################
process.anaTrack.qualityStrings = cms.untracked.vstring('highPurity','highPuritySetWithPV')
process.pixelTrack.qualityStrings = cms.untracked.vstring('highPurity','highPuritySetWithPV')
process.hiTracks.cut = cms.string('quality("highPurity")')

# set track collection to iterative tracking
process.anaTrack.trackSrc = cms.InputTag("hiGeneralTracks")

# clusters missing in recodebug - to be resolved
process.anaTrack.doPFMatching = False

#####################
# photons
process.interestingTrackEcalDetIds.TrackCollection = cms.InputTag("hiGeneralTracks")
process.load("RecoEcal.EgammaCoreTools.EcalNextToDeadChannelESProducer_cff")
process.load('HeavyIonsAnalysis.JetAnalysis.ExtraEGammaReco_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.EGammaAnalyzers_cff')
process.multiPhotonAnalyzer.GenEventScale = cms.InputTag("generator")
process.multiPhotonAnalyzer.HepMCProducer = cms.InputTag("generator")
process.multiPhotonAnalyzer.gsfElectronCollection = cms.untracked.InputTag("ecalDrivenGsfElectrons")
process.load("edwenger.HiTrkEffAnalyzer.TrackSelections_cff")
process.hiGoodTracks.src = cms.InputTag("hiGeneralTracks")
process.photonStep = cms.Path(process.hiGoodTracks * process.photon_extra_reco * process.makeHeavyIonPhotons)
process.photonStep.remove(process.interestingTrackEcalDetIds)
process.photonMatch.matched = cms.InputTag("genParticles")
process.photonStep.remove(process.seldigis)
process.reducedEcalRecHitsEB = cms.EDProducer("ReducedRecHitCollectionProducer",
    interestingDetIdCollections = cms.VInputTag(cms.InputTag("interestingEcalDetIdEB"), cms.InputTag("interestingEcalDetIdEBU")),
    recHitsLabel = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
    reducedHitsCollection = cms.string('')
)
process.reducedEcalRecHitsEE = cms.EDProducer("ReducedRecHitCollectionProducer",
    interestingDetIdCollections = cms.VInputTag(cms.InputTag("interestingEcalDetIdEE")),
    recHitsLabel = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
    reducedHitsCollection = cms.string('')
)
process.patPhotons.addPhotonID = cms.bool(False)
process.extrapatstep = cms.Path(process.selectedPatPhotons)
process.multiPhotonAnalyzer.GammaEtaMax = cms.untracked.double(100)
process.multiPhotonAnalyzer.GammaPtMin = cms.untracked.double(10)
process.RandomNumberGeneratorService.multiPhotonAnalyzer = process.RandomNumberGeneratorService.generator.clone()

#####################
# muons
######################
process.load("HeavyIonsAnalysis.MuonAnalysis.hltMuTree_cfi")
process.hltMuTree.doGen = cms.untracked.bool(True)
process.load("RecoHI.HiMuonAlgos.HiRecoMuon_cff")
process.muons.JetExtractorPSet.JetCollectionLabel = cms.InputTag("akVs3PFJets")
process.globalMuons.TrackerCollectionLabel = "hiGeneralTracks"
process.muons.TrackExtractorPSet.inputTrackCollection = "hiGeneralTracks"
process.muons.inputCollectionLabels = ["hiGeneralTracks", "globalMuons", "standAloneMuons:UpdatedAtVtx", "tevMuons:firstHit", "tevMuons:picky", "tevMuons:dyt"]

process.temp_step = cms.Path(process.hiGenParticles * process.hiGenParticlesForJets
                             *
                             process.ak2HiGenJets +
                             process.ak3HiGenJets +
                             process.ak4HiGenJets +
                             process.ak5HiGenJets + 
                             process.ak6HiGenJets +
                             process.ak7HiGenJets)

process.ana_step = cms.Path(process.heavyIon*
                            process.hiEvtAnalyzer*
                            process.HiGenParticleAna*
                            process.hiGenJetsCleaned*
                            process.jetSequences +                            
                            process.multiPhotonAnalyzer +
                            process.pfcandAnalyzer +
                            process.rechitAna +
#temp                            process.hltMuTree +
                            process.HiForest +
                            process.cutsTPForFak +
                            process.cutsTPForEff +
                            process.anaTrack)

process.load('HeavyIonsAnalysis.JetAnalysis.EventSelection_cff')
process.phltJetHI = cms.Path( process.hltJetHI )
process.pcollisionEventSelection = cms.Path(process.collisionEventSelection)
process.pHBHENoiseFilter = cms.Path( process.HBHENoiseFilter )
process.phfCoincFilter = cms.Path(process.hfCoincFilter )
process.phfCoincFilter3 = cms.Path(process.hfCoincFilter3 )
process.pprimaryVertexFilter = cms.Path(process.primaryVertexFilter )
process.phltPixelClusterShapeFilter = cms.Path(process.siPixelRecHits*process.hltPixelClusterShapeFilter )
process.phiEcalRecHitSpikeFilter = cms.Path(process.hiEcalRecHitSpikeFilter )

# Customization
from HeavyIonsAnalysis.JetAnalysis.customise_cfi import *
setPhotonObject(process,"cleanPhotons")

process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cff')

process.hltAna = cms.Path(process.hltanalysis)
process.pAna = cms.EndPath(process.skimanalysis)

# Load Beamspot for case of pp MC reco with PbPb settings
from CondCore.DBCommon.CondDBSetup_cfi import CondDBSetup
process.beamspot = cms.ESSource("PoolDBESSource",CondDBSetup,
                                toGet = cms.VPSet(cms.PSet( record = cms.string('BeamSpotObjectsRcd'),
                                                            tag= cms.string('Realistic2p76TeVCollisions2013_START53_V9_v1_mc')
                                                            )),
                                connect =cms.string('frontier://FrontierProd/CMS_COND_31X_BEAMSPOT')
                                )
process.es_prefer_beamspot = cms.ESPrefer("PoolDBESSource","beamspot")
