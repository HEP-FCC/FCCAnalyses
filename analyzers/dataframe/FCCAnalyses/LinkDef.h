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
#pragma link C++ class std::vector<std::vector<float>>+;
#pragma link C++ class std::vector<std::vector<double>>+;
#pragma link C++ class ROOT::VecOps::RVec<edm4hep::TrackState>+;
#pragma link C++ class ROOT::VecOps::RVec<edm4hep::VertexData>+;
#pragma link C++ class ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>+;
#pragma link C++ class ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>+;
#pragma link C++ class ROOT::VecOps::RVec<edm4hep::ClusterData>+;
#pragma link C++ class ROOT::VecOps::RVec<podio::ObjectID>+;
#pragma link C++ class ROOT::VecOps::RVec<edm4hep::Vector3d>+;
#pragma link C++ class ROOT::VecOps::RVec<edm4hep::MCParticleData>+;
#pragma link C++ class ROOT::VecOps::RVec<TVector3>+;
#pragma link C++ class ROOT::VecOps::RVec<ROOT::VecOps::RVec<int>>+;
#pragma link C++ class ROOT::VecOps::RVec<ROOT::VecOps::RVec<float>>+;
#pragma link C++ class ROOT::VecOps::RVec<ROOT::VecOps::RVec<double>>+;
#pragma link C++ class ROOT::VecOps::RVec<ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>>+;
#pragma link C++ class ROOT::VecOps::RVec<std::vector<float>>+;

#pragma link C++ class ROOT::VecOps::RVec<FCCAnalyses::VertexingUtils::FCCAnalysesVertex>+;
#pragma link C++ class ROOT::VecOps::RVec<ROOT::VecOps::RVec<FCCAnalyses::VertexingUtils::FCCAnalysesVertex>>+;
#pragma link C++ class ROOT::VecOps::RVec<ROOT::VecOps::RVec<TVector3>>+;
#pragma link C++ class ROOT::VecOps::RVec<ROOT::VecOps::RVec<TLorentzVector>>+;

//to load all other functions
#pragma link C++ function dummyLoader;

#endif
