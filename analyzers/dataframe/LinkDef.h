#ifdef __CINT__

//Globals
#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;
#pragma link C++ nestedclasses;

//Dictionaries for output objects
#pragma link C++ class std::vector<TLorentzVector>+;
#pragma link C++ class std::vector<std::string>+;

#pragma link C++ class ROOT::VecOps::RVec<TLorentzVector>+;
#pragma link C++ class std::vector<std::vector<int>>+;
#pragma link C++ class ROOT::VecOps::RVec<edm4hep::TrackState>+;
#pragma link C++ class ROOT::VecOps::RVec<edm4hep::VertexData>+;
#pragma link C++ class ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>+;
#pragma link C++ class ROOT::VecOps::RVec<edm4hep::Vector3d>+;
#pragma link C++ class ROOT::VecOps::RVec<edm4hep::MCParticleData>+;
#pragma link C++ class ROOT::VecOps::RVec<TVector3>+;

//to load all other functions
#pragma link C++ function dummyLoader;

#endif
