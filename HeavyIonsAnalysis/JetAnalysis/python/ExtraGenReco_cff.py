import FWCore.ParameterSet.Config as cms

#
# Gen
from PhysicsTools.HepMCCandAlgos.HiGenParticles_cfi import *
from RecoJets.Configuration.GenJetParticles_cff import *
from RecoHI.HiJetAlgos.HiGenCleaner_cff import *
from PhysicsTools.PatAlgos.producersHeavyIons.heavyIonProducer_cfi import heavyIon

hiGenParticlesForJets.ignoreParticleIDs += cms.vuint32( 12,14,16)

hiGenParticles.srcVector = cms.vstring('hiSignal')

hiGen = cms.Sequence(
  heavyIon * # GenHIEventProducer
  hiGenParticles *
  hiGenParticlesForJets *
  genPartons *
  hiPartons
  )
