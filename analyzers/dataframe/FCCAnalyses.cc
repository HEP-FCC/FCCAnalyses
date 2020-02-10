#include "FCCAnalyses.h"

#include "TLorentzVector.h"
#include "datamodel/MCParticleData.h"
#include "datamodel/Point.h"
#include "datamodel/LorentzVector.h"

std::vector<float> pt (std::vector<fcc::MCParticleData> in){
 std::vector<float> result;
	 for (size_t i = 0; i < in.size(); ++i) {
		 result.push_back(std::sqrt(in[i].core.p4.px * in[i].core.p4.px + in[i].core.p4.py * in[i].core.p4.py));
	 }
	 return result;
}

std::vector<float> eta(std::vector<fcc::MCParticleData> in){
 std::vector<float> result;
   TLorentzVector lv;
	 for (size_t i = 0; i < in.size(); ++i) {
     lv.SetXYZM(in[i].core.p4.px, in[i].core.p4.py, in[i].core.p4.pz, in[i].core.p4.mass);
		 result.push_back(lv.Eta());
	 }
	 return result;
}

std::vector<TLorentzVector> tlv(std::vector<fcc::LorentzVector> in){
 std::vector<TLorentzVector> result;
   TLorentzVector lv;
	 for (size_t i = 0; i < in.size(); ++i) {
     lv.SetXYZM(in[i].px, in[i].py, in[i].pz, in[i].mass);
		 result.push_back(lv);
	 }
	 return result;
}

std::vector<float> r (std::vector<fcc::Point> in) {
 std::vector<float> result;
	 for (size_t i = 0; i < in.size(); ++i) {
     result.push_back(std::sqrt(in[i].x*in[i].x + in[i].y*in[i].y));
   }
 return result; 
}


std::vector<float> norm (std::vector<fcc::Point> in) {
 std::vector<float> result;
	 for (size_t i = 0; i < in.size(); ++i) {
     result.push_back(std::sqrt(in[i].x*in[i].x + in[i].y*in[i].y + in[i].z*in[i].z));
   }
 return result; 
}
