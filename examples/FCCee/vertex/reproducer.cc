// Make sure these can all be found on LD_LIBRARY_PATH
#ifdef __CLING__
R__LOAD_LIBRARY(libpodio)
R__LOAD_LIBRARY(libpodioDict)
R__LOAD_LIBRARY(libpodioRootIO)
R__LOAD_LIBRARY(libedm4hep)
R__LOAD_LIBRARY(libedm4hepDict)
R__LOAD_LIBRARY(libFCCAnalyses)
#endif

// also make sure that the podio include directory is in ROOT_INCLUDE_PATH
#include "podio/EventStore.h"
#include "podio/ROOTReader.h"
#include "edm4hep/TrackState.h"
#include "edm4hep/TrackCollection.h"

#include "VertexFinderActs.h"
#include "ROOT/RVec.hxx"

void reproducer()
{

  gInterpreter->ProcessLine("#include \"VertexFinderActs.h\"");
  gSystem->Load("libpodio");
  gSystem->Load("libpodioDict");
  gSystem->Load("libpodioRootIO");
  gSystem->Load("libedm4hep");
  gSystem->Load("libedm4hepDict");
  gSystem->Load("libFCCAnalyses");

  auto reader = podio::ROOTReader();
  reader.openFile("https://fcc-physics-events.web.cern.ch/fcc-physics-events/sharedFiles/FCCee/test_zbb_Bs2DsK.root");
  auto store = podio::EventStore();
  store.setReader(&reader);

  const auto nEntries = reader.getEntries();
  for (int entry = 0; entry < nEntries; ++entry) {

    auto& tracks = store.get<edm4hep::TrackCollection>("EFlowTrack");
    ROOT::VecOps::RVec<edm4hep::TrackState>  track_states;// = tracks.getTrackStates();
    for (auto track : tracks) { track_states.push_back(track.getTrackStates(0)); } 
    auto result = VertexFinderActs::VertexFinderAMVF(track_states);
    
  }
}
