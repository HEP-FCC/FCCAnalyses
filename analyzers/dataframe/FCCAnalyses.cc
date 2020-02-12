#include "FCCAnalyses.h"

#include "TLorentzVector.h"
#include "datamodel/MCParticleData.h"
#include "datamodel/ParticleData.h"
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

double deltaR(fcc::LorentzVector v1, fcc::LorentzVector v2) {
  TLorentzVector tv1;
  tv1.SetXYZM(v1.px, v1.py, v1.pz, v1.mass);

  TLorentzVector tv2;
  tv2.SetXYZM(v2.px, v2.py, v2.pz, v2.mass);

  double deltaPhi = M_PI - std::abs(std::abs(tv1.Phi() - tv2.Phi()) - M_PI);
  double deltaEta = std::abs(tv1.Eta() - tv2.Eta());
  double result = std::sqrt(deltaPhi * deltaPhi + deltaEta * deltaEta);
  return result;
}

  recoil::recoil(float arg_sqrts) : m_sqrts(arg_sqrts) {};
  std::vector<fcc::ParticleData>  recoil::operator() (std::vector<fcc::ParticleData> in) {
      std::vector<fcc::ParticleData> result;
      auto recoil_p4 = TLorentzVector(0, 0, 0, m_sqrts);
      for (auto & v1: in) {
        TLorentzVector tv1;
        tv1.SetXYZM(v1.core.p4.px, v1.core.p4.py, v1.core.p4.pz, v1.core.p4.mass);
        recoil_p4 -= tv1;
      }
      auto recoil_fcc = fcc::ParticleData();
      recoil_fcc.core.p4.px = recoil_p4.Px();
      recoil_fcc.core.p4.py = recoil_p4.Py();
      recoil_fcc.core.p4.pz = recoil_p4.Pz();
      recoil_fcc.core.p4.mass = recoil_p4.M();
      result.push_back(recoil_fcc);
      return result;
  };
