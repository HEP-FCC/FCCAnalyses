#ifdef __CINT__

#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;
#pragma link C++ nestedclasses;

#pragma link C++ class vector<TLorentzVector>+;
#pragma link C++ class ROOT::VecOps::RVec<TLorentzVector>+;
#pragma link C++ class std::vector<std::string>+;

//Algo
#pragma link C++ class thrustFit;
#pragma link C++ class minimize_thrust;
#pragma link C++ class getRP_combination;


//Reconstructed Particles
#pragma link C++ class selRP_pT;
#pragma link C++ class selRP_p;
#pragma link C++ function getRP_p;
#pragma link C++ function getRP_pt;
#pragma link C++ function getRP_px;
#pragma link C++ function getRP_py;
#pragma link C++ function getRP_pz;
#pragma link C++ function getRP_eta;
#pragma link C++ function getRP_y;
#pragma link C++ function getRP_theta;
#pragma link C++ function getRP_phi;
#pragma link C++ function getRP_e;
#pragma link C++ function getRP_mass;
#pragma link C++ function getRP_charge;
#pragma link C++ function getRP_tlv;
#pragma link C++ function mergeParticles;
#pragma link C++ function get_n_particles;


//MC Particles
#pragma link C++ function getMC_p;
#pragma link C++ function getMC_px;
#pragma link C++ function getMC_py;
#pragma link C++ function getMC_pz;
#pragma link C++ function getMC_e;

//Reconstructed Particles to tracks
#pragma link C++ function getRPTRK_D0;
#pragma link C++ function getRP2TRK_Z0;

#pragma link C++ function getRP2MC_p;
#pragma link C++ class getRP2MC_p_func;



#endif
