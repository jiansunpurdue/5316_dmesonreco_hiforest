import FWCore.ParameterSet.Config as cms
from RecoHI.HiJetAlgos.HiRecoJets_cff import *
from RecoHI.HiJetAlgos.HiRecoPFJets_cff import *
akVs2PFJets.jetPtMin = 1
akVs2CaloJets.jetPtMin = 1
akVs3PFJets.jetPtMin = 1
akVs3CaloJets.jetPtMin = 1
akVs4PFJets.jetPtMin = 1
akVs4CaloJets.jetPtMin = 1
akVs5PFJets.jetPtMin = 1
akVs5CaloJets.jetPtMin = 1
akVs6PFJets.jetPtMin = 1
akVs6CaloJets.jetPtMin = 1
akVs7PFJets.jetPtMin = 1
akVs7CaloJets.jetPtMin = 1
akPu2PFJets.jetPtMin = 1
akPu2CaloJets.jetPtMin = 1
akPu3PFJets.jetPtMin = 1
akPu3CaloJets.jetPtMin = 1
akPu4PFJets.jetPtMin = 1
akPu4CaloJets.jetPtMin = 1
akPu5PFJets.jetPtMin = 1
akPu5CaloJets.jetPtMin = 1
akPu6PFJets.jetPtMin = 1
akPu6CaloJets.jetPtMin = 1
akPu7PFJets.jetPtMin = 1
akPu7CaloJets.jetPtMin = 1
ak2PFJets.jetPtMin = 1
ak2CaloJets.jetPtMin = 1
ak3PFJets.jetPtMin = 1
ak3CaloJets.jetPtMin = 1
ak4PFJets.jetPtMin = 1
ak4CaloJets.jetPtMin = 1
ak5PFJets.jetPtMin = 1
ak5CaloJets.jetPtMin = 1
ak6PFJets.jetPtMin = 1
ak6CaloJets.jetPtMin = 1
ak7PFJets.jetPtMin = 1
ak7CaloJets.jetPtMin = 1
akVs2PFJets.jetPtMin = 1
akVs2CaloJets.jetPtMin = 1
akVs3PFJets.jetPtMin = 1
akVs3CaloJets.jetPtMin = 1
akVs4PFJets.jetPtMin = 1
akVs4CaloJets.jetPtMin = 1
akVs5PFJets.jetPtMin = 1
akVs5CaloJets.jetPtMin = 1
akVs6PFJets.jetPtMin = 1
akVs6CaloJets.jetPtMin = 1
akVs7PFJets.jetPtMin = 1
akVs7CaloJets.jetPtMin = 1
akPu2PFJets.jetPtMin = 1
akPu2CaloJets.jetPtMin = 1
akPu3PFJets.jetPtMin = 1
akPu3CaloJets.jetPtMin = 1
akPu4PFJets.jetPtMin = 1
akPu4CaloJets.jetPtMin = 1
akPu5PFJets.jetPtMin = 1
akPu5CaloJets.jetPtMin = 1
akPu6PFJets.jetPtMin = 1
akPu6CaloJets.jetPtMin = 1
akPu7PFJets.jetPtMin = 1
akPu7CaloJets.jetPtMin = 1
ak2PFJets.jetPtMin = 1
ak2CaloJets.jetPtMin = 1
ak3PFJets.jetPtMin = 1
ak3CaloJets.jetPtMin = 1
ak4PFJets.jetPtMin = 1
ak4CaloJets.jetPtMin = 1
ak5PFJets.jetPtMin = 1
ak5CaloJets.jetPtMin = 1
ak6PFJets.jetPtMin = 1
ak6CaloJets.jetPtMin = 1
ak7PFJets.jetPtMin = 1
ak7CaloJets.jetPtMin = 1
akVs2PFJets.jetPtMin = 1
akVs2CaloJets.jetPtMin = 1
akVs3PFJets.jetPtMin = 1
akVs3CaloJets.jetPtMin = 1
akVs4PFJets.jetPtMin = 1
akVs4CaloJets.jetPtMin = 1
akVs5PFJets.jetPtMin = 1
akVs5CaloJets.jetPtMin = 1
akVs6PFJets.jetPtMin = 1
akVs6CaloJets.jetPtMin = 1
akVs7PFJets.jetPtMin = 1
akVs7CaloJets.jetPtMin = 1
akPu2PFJets.jetPtMin = 1
akPu2CaloJets.jetPtMin = 1
akPu3PFJets.jetPtMin = 1
akPu3CaloJets.jetPtMin = 1
akPu4PFJets.jetPtMin = 1
akPu4CaloJets.jetPtMin = 1
akPu5PFJets.jetPtMin = 1
akPu5CaloJets.jetPtMin = 1
akPu6PFJets.jetPtMin = 1
akPu6CaloJets.jetPtMin = 1
akPu7PFJets.jetPtMin = 1
akPu7CaloJets.jetPtMin = 1
ak2PFJets.jetPtMin = 1
ak2CaloJets.jetPtMin = 1
ak3PFJets.jetPtMin = 1
ak3CaloJets.jetPtMin = 1
ak4PFJets.jetPtMin = 1
ak4CaloJets.jetPtMin = 1
ak5PFJets.jetPtMin = 1
ak5CaloJets.jetPtMin = 1
ak6PFJets.jetPtMin = 1
ak6CaloJets.jetPtMin = 1
ak7PFJets.jetPtMin = 1
ak7CaloJets.jetPtMin = 1

hiReRecoPFJets = cms.Sequence(
ak2PFJets
+
ak3PFJets
+
ak4PFJets
+
ak5PFJets
+
ak6PFJets
+
ak7PFJets
+
akPu2PFJets
+
akPu3PFJets
+
akPu4PFJets
+
akPu5PFJets
+
akPu6PFJets
+
akPu7PFJets
+
akVs2PFJets
+
akVs3PFJets
+
akVs4PFJets
+
akVs5PFJets
+
akVs6PFJets
+
akVs7PFJets
)

hiReRecoCaloJets = cms.Sequence(
ak2CaloJets
+
ak3CaloJets
+
ak4CaloJets
+
ak5CaloJets
+
ak6CaloJets
+
ak7CaloJets
+
akPu2CaloJets
+
akPu3CaloJets
+
akPu4CaloJets
+
akPu5CaloJets
+
akPu6CaloJets
+
akPu7CaloJets
+
akVs2CaloJets
+
akVs3CaloJets
+
akVs4CaloJets
+
akVs5CaloJets
+
akVs6CaloJets
+
akVs7CaloJets
)
