#include "FWCore/Framework/interface/MakerMacros.h"
#include "UserCode/OpenHF/interface/HFTree.hh"

#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <iostream>

#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"


#include <TROOT.h>
#include <TTree.h>
#include <TH1.h>

#include "UserCode/OpenHF/data_format/TAna01Event.hh"
#include "UserCode/OpenHF/data_format/TAnaTrack.hh"
#include "UserCode/OpenHF/data_format/TAnaCand.hh"
#include "UserCode/OpenHF/data_format/TAnaVertex.hh"
#include "UserCode/OpenHF/data_format/candAna.cc"
#include "UserCode/OpenHF/data_format/hfcand_v0.hh"
// -- Yikes!
TAna01Event  *gHFEvent;


using namespace::std;
using namespace::edm;

// ----------------------------------------------------------------------
HFTree::HFTree(const edm::ParameterSet& iConfig) :
  fRequireCand(iConfig.getUntrackedParameter<bool>("requireCand", true)), 
  fFullGenBlock(iConfig.getUntrackedParameter<bool>("fullGenBlock", false)), 
  fTreeName(iConfig.getUntrackedParameter<string>("treeName", string("T1"))), 
  fVerbose(iConfig.getUntrackedParameter<int>("verbose", 1)),
  fPrintFrequency(iConfig.getUntrackedParameter<int>("printFrequency", 1000)) {
  using namespace std;
  cout << "----------------------------------------------------------------------" << endl;
  cout << "--- HFTree constructor" << endl;
  cout << "---  verbose:                         " << fVerbose << endl;
  cout << "---  printFrequency:                  " << fPrintFrequency << endl;
  cout << "---  treeName:                        " << fTreeName << endl; 
  cout << "---  requireCand:                     " << (fRequireCand?"true":"false") << endl; 
  cout << "---  fullGenBlock:                    " << (fFullGenBlock?"true":"false") << endl; 
  cout << "----------------------------------------------------------------------" << endl;

  a = new candAna;
  a->set_cut(2, 0.5);
  
  fEvent = new TAna01Event(0);
  gHFEvent = fEvent;

  fEventCounter = -1; 
}


// ----------------------------------------------------------------------
HFTree::~HFTree() {
  
}


// ----------------------------------------------------------------------
void HFTree::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

  ++fEventCounter; 
  if (fVerbose > 0) {
    if (fEventCounter%fPrintFrequency == 0) {
      pid_t pid = getpid();
      char line[100]; 
      sprintf(line, "ps -F %i", pid); 
      cout << "==>HFTree: analyze() in event #" << fEventCounter 
	   << "  run: " << gHFEvent->fRunNumber 
	   << " event: "  << gHFEvent->fEventNumber
	   << endl;
      system(line); 
    }
  }


//  if (fRequireCand){
//    if (gHFEvent->nCands() > 0) {
//      if (fVerbose > 1) {
//	cout << "HFTree> filling tree for run: " << gHFEvent->fRunNumber
//	     << " event: "  << gHFEvent->fEventNumber ;
//
//	if (fVerbose > 2) {
//	  cout << " Cand: ";
//	
//	  for (int i = 0; i < gHFEvent->nCands(); ++i) {
//	    cout << gHFEvent->getCand(i)->fType << " ";
//	  }
//	}
//	cout << endl;
//      }
//      fTree->Fill();
//    } 
//  } else {
//    fTree->Fill();
//  }


//  if (gHFEvent->nCands() > 0)
//  {
	a->hfcandidate->Reset();
    a->evtAnalysis(gHFEvent);
    hftree->Fill();
//  }

  gHFEvent->Clear();
}

// ------------ method called once each job just before starting event loop  ------------
void  HFTree::beginJob() {
  edm::Service<TFileService> fs;
  fTree = fs->make<TTree>("fTree" , "heavy flavor original tree");
  hftree = fs->make<TTree>("hftree" , "heavy flavor reduced tree");
  fTree->Branch("TAna01Event", "TAna01Event", &fEvent, 256000/8, 1);
// hfTree->Branch("hfcand_v0", "hfcand_v0", &a->hfcandidate, 256000/8, 1);
  hftree->Branch("hfcandidate", &a->hfcandidate);
}

// ------------ method called once each job just after ending the event loop  ------------
void  HFTree::endJob() {

  pid_t pid = getpid();
  char line[100]; 
  sprintf(line, "ps -F %i", pid); 
  cout << "==>HFTree: endJob():" << endl;
  system(line); 

}

//define this as a plug-in
DEFINE_FWK_MODULE(HFTree);
