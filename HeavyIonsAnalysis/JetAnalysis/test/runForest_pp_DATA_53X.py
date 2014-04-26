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
                            fileNames = cms.untracked.vstring("file:DATA_RECO.root")
                            )

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

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'GR_P_V43D::All', '')

from HeavyIonsAnalysis.Configuration.CommonFunctions_cff import *
overrideGT_pp2760(process)
overrideJEC_pp2760(process)

process.HeavyIonGlobalParameters = cms.PSet(
    centralityVariable = cms.string("HFtowers"),
    nonDefaultGlauberModel = cms.string(""),
    centralitySrc = cms.InputTag("hiCentrality")
    )

#####################################################################################
# Define tree output
#####################################################################################

process.TFileService = cms.Service("TFileService",
                                   fileName=cms.string("HiForest_pp_data.root"))

#####################################################################################
# Additional Reconstruction and Analysis: Main Body
#####################################################################################

#process.load('RecoHI.HiJetAlgos.HiRecoJets_cff')
#process.load('RecoHI.HiJetAlgos.HiRecoPFJets_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.jets.allJets_pp_data_cff')

process.jetSequences = cms.Sequence(process.allJets)
# process.jetSequences.remove(process.ak2CaloJetSequence)
# process.jetSequences.remove(process.akPu2CaloJetSequence)
# process.jetSequences.remove(process.akVs2CaloJetSequence)
# process.jetSequences.remove(process.ak2PFJetSequence)
# process.jetSequences.remove(process.akPu2PFJetSequence)
# process.jetSequences.remove(process.akVs2PFJetSequence)
process.jetSequences.remove(process.ak7CaloJetSequence)
process.jetSequences.remove(process.akPu7CaloJetSequence)
process.jetSequences.remove(process.akVs7CaloJetSequence)
process.jetSequences.remove(process.ak7PFJetSequence)
process.jetSequences.remove(process.akPu7PFJetSequence)
process.jetSequences.remove(process.akVs7PFJetSequence)


#####################################################################################
# To be cleaned

process.load('HeavyIonsAnalysis.JetAnalysis.ExtraTrackReco_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.ExtraPfReco_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.TrkAnalyzers_cff')
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
process.photonMatch.matched = cms.InputTag("hiGenParticles")
process.patPhotons.addPhotonID = cms.bool(False)
process.multiPhotonAnalyzer.GammaEtaMax = cms.untracked.double(100)
process.multiPhotonAnalyzer.GammaPtMin = cms.untracked.double(10)
process.RandomNumberGeneratorService.multiPhotonAnalyzer = process.RandomNumberGeneratorService.generator.clone()

#####################

######################
# muons
######################
process.load("HeavyIonsAnalysis.MuonAnalysis.hltMuTree_cfi")
process.hltMuTree.doGen = cms.untracked.bool(True)
process.load("RecoHI.HiMuonAlgos.HiRecoMuon_cff")
process.muons.JetExtractorPSet.JetCollectionLabel = cms.InputTag("akVs3PFJets")
process.globalMuons.TrackerCollectionLabel = "hiGeneralTracks"
process.muons.TrackExtractorPSet.inputTrackCollection = "hiGeneralTracks"
process.muons.inputCollectionLabels = ["hiGeneralTracks", "globalMuons", "standAloneMuons:UpdatedAtVtx", "tevMuons:firstHit","tevMuons:picky", "tevMuons:dyt"]

process.hltMuTree.doGen = False

######################

process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_data_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cff')
process.load('HeavyIonsAnalysis.JetAnalysis.EventSelection_cff')

#Filtering
# Minimum bias trigger selection (later runs)
# process.load("HLTrigger.HLTfilters.hltHighLevel_cfi")
# process.hltMinBiasHFOrBSC = process.hltHighLevel.clone()
# process.hltMinBiasHFOrBSC.HLTPaths = ["HLT_HIMinBiasHfOrBSC_v1"]
# process.load("HeavyIonsAnalysis.Configuration.collisionEventSelection_cff")
# process.filterSequence = cms.Sequence(process.hltMinBiasHFOrBSC*process.collisionEventSelection)
# process.skimanalysis.superFilters = cms.vstring("ana_step")

process.photonStep = cms.Sequence(process.hiGoodTracks * process.photon_extra_reco * process.makeHeavyIonPhotons * process.selectedPatPhotons)
process.photonStep.remove(process.interestingTrackEcalDetIds)
process.photonStep.remove(process.photonMatch)
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

process.pcollisionEventSelection = cms.Path(process.collisionEventSelection)
process.pHBHENoiseFilter = cms.Path( process.HBHENoiseFilter )
process.phfCoincFilter = cms.Path(process.hfCoincFilter )
process.phfCoincFilter3 = cms.Path(process.hfCoincFilter3 )
process.pprimaryVertexFilter = cms.Path(process.primaryVertexFilter )
process.phltPixelClusterShapeFilter = cms.Path(process.siPixelRecHits*process.hltPixelClusterShapeFilter )
process.phiEcalRecHitSpikeFilter = cms.Path(process.hiEcalRecHitSpikeFilter )


process.ana_step = cms.Path(#process.filterSequence *
                            process.photonStep *
                            process.hltanalysis *
                            process.hiEvtAnalyzer *
                            process.jetSequences +
                            process.multiPhotonAnalyzer +
                            process.pfcandAnalyzer +
                            process.rechitAna +
#temp                            process.hltMuTree +
                            process.HiForest +                            
                            process.anaTrack
                            )

process.pAna = cms.EndPath(process.skimanalysis)



