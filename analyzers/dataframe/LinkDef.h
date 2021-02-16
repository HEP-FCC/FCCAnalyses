#ifdef __CINT__

#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;
#pragma link C++ nestedclasses;

#pragma link C++ class vector<TLorentzVector>+;
#pragma link C++ class ROOT::VecOps::RVec<TLorentzVector>+;
#pragma link C++ class std::vector<std::string>+;
#pragma link C++ class ROOT::VecOps::RVec<edm4hep::TrackState>+;
#pragma link C++ class ROOT::VecOps::RVec<edm4hep::VertexData>+;
#pragma link C++ class ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>+;
#pragma link C++ class ROOT::VecOps::RVec<edm4hep::Vector3d>+;
#pragma link C++ class ROOT::VecOps::RVec<edm4hep::MCParticleData>+;


#pragma link C++ function dummyloader;

//Algo
#pragma link C++ class thrustFit;
#pragma link C++ class minimize_thrust;
#pragma link C++ class getRP_combination;


//MC Particles
#pragma link C++ function getMC_p;
#pragma link C++ function MCParticles::get_px;
//#pragma link C++ class MCParticle::get_px;
#pragma link C++ function getMC_py;
#pragma link C++ function getMC_pz;
#pragma link C++ function getMC_e;

//Reconstructed Particles to tracks
#pragma link C++ function getRPTRK_D0;
#pragma link C++ function getRP2TRK_Z0;

#pragma link C++ function getRP2MC_p;
#pragma link C++ class getRP2MC_p_func;

//Vertex
#pragma link C++ function get_nTracks;

#endif
