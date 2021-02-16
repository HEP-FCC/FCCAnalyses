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

#include "VertexingACTS.h"
void reproducer()
{

  gInterpreter->ProcessLine("#include \"VertexingACTS.h\"");
  gSystem->Load("libpodio.so");
  gSystem->Load("libpodioDict.so");
  gSystem->Load("libpodioRootIO.so");
  gSystem->Load("libedm4hep.so");
  gSystem->Load("libedm4hepDict.so");
  gSystem->Load("libFCCAnalyses.so");

  auto reader = podio::ROOTReader();
  reader.openFile("/eos/experiment/fcc/ee/generation/DelphesEvents/fcc_tmp/p8_ee_Zuds_ecm91/events_199980034.root");
  auto store = podio::EventStore();
  store.setReader(&reader);


  const auto nEntries = reader.getEntries();
  for (int entry = 0; entry < nEntries; ++entry) {

    auto& tracks = store.get<edm4hep::TrackCollection>("EFlowTrack");
    std::vector<edm4hep::TrackState>  track_states;// = tracks.getTrackStates();
    for (auto track : tracks) { track_states.push_back(track.getTrackStates(0)); } 
    bool status = VertexingACTS::initialize(track_states);
    
  }
}
