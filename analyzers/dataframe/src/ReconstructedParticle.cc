#include "FCCAnalyses/ReconstructedParticle.h"

// Standard library
#include <cstdlib>
#include <iostream>
#include <stdexcept>

namespace FCCAnalyses ::ReconstructedParticle {

/*
 *  sel_type
 */
sel_type::sel_type(const int type) : m_type(type) {}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> sel_type::operator()(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    if (in[i].type == m_type) {
      result.emplace_back(in[i]);
    }
  }
  return result;
}

/*
 *  sel_absType
 */
sel_absType::sel_absType(const int type) : m_type(type) {
  if (m_type < 0) {
    throw std::invalid_argument(
        "ReconstructedParticle::sel_absType: Received negative value!");
  }
}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> sel_absType::operator()(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    if (std::abs(in[i].type) == m_type) {
      result.emplace_back(in[i]);
    }
  }
  return result;
}

/*
 *  sel_pt
 */
sel_pt::sel_pt(float arg_min_pt) : m_min_pt(arg_min_pt) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  sel_pt::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if (std::sqrt(std::pow(p.momentum.x,2) + std::pow(p.momentum.y,2)) > m_min_pt) {
      result.emplace_back(p);
    }
  }
  return result;
}

/*
 *  sel_eta
 */
sel_eta::sel_eta(float arg_min_eta) : m_min_eta(arg_min_eta) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  sel_eta::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    TLorentzVector tv1;
    tv1.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    if (abs(tv1.Eta()) < abs(m_min_eta)){
      result.emplace_back(p);
    }
  }
  return result;
}


sel_p::sel_p(float arg_min_p, float arg_max_p) : m_min_p(arg_min_p), m_max_p(arg_max_p)  {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  sel_p::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    float momentum = std::sqrt(   std::pow(p.momentum.x,2)
                                + std::pow(p.momentum.y,2)
                                + std::pow(p.momentum.z,2) );
    if ( momentum > m_min_p && momentum < m_max_p ) {
      result.emplace_back(p);
    }
  }
  return result;
}

sel_charge::sel_charge(int arg_charge, bool arg_abs){m_charge = arg_charge; m_abs = arg_abs;};

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  sel_charge::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if ((m_abs && abs(in[i].charge)==m_charge) || (m_charge==in[i].charge) ) {
      result.emplace_back(p);
    }
  }
  return result;
}



resonanceBuilder::resonanceBuilder(float arg_resonance_mass) {m_resonance_mass = arg_resonance_mass;}
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> resonanceBuilder::operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  int n = legs.size();
  if (n >1) {
    ROOT::VecOps::RVec<bool> v(n);
    std::fill(v.end() - 2, v.end(), true);
    do {
      edm4hep::ReconstructedParticleData reso;
      TLorentzVector reso_lv;
      for (int i = 0; i < n; ++i) {
          if (v[i]) {
            reso.charge += legs[i].charge;
            TLorentzVector leg_lv;
            leg_lv.SetXYZM(legs[i].momentum.x, legs[i].momentum.y, legs[i].momentum.z, legs[i].mass);
            reso_lv += leg_lv;
          }
      }
      reso.momentum.x = reso_lv.Px();
      reso.momentum.y = reso_lv.Py();
      reso.momentum.z = reso_lv.Pz();
      reso.mass = reso_lv.M();
      result.emplace_back(reso);
    } while (std::next_permutation(v.begin(), v.end()));
  }
  if (result.size() > 1) {
    auto resonancesort = [&] (edm4hep::ReconstructedParticleData i ,edm4hep::ReconstructedParticleData j) { return (abs( m_resonance_mass -i.mass)<abs(m_resonance_mass-j.mass)); };
    std::sort(result.begin(), result.end(), resonancesort);
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>::const_iterator first = result.begin();
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>::const_iterator last = result.begin() + 1;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> onlyBestReso(first, last);
    return onlyBestReso;
  } else {
    return result;
  }
}

/*
 * recoilBuilder
 */
recoilBuilder::recoilBuilder(float arg_sqrts) : m_sqrts(arg_sqrts) {};

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
recoilBuilder::operator()(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> inParticles) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  auto recoil_p4 = TLorentzVector(0, 0, 0, m_sqrts);

  for (const auto &v1 : inParticles) {
    TLorentzVector tv1;
    tv1.SetXYZM(v1.momentum.x, v1.momentum.y, v1.momentum.z, v1.mass);
    recoil_p4 -= tv1;
  }

  auto recoil_fcc = edm4hep::ReconstructedParticleData();
  recoil_fcc.momentum.x = recoil_p4.Px();
  recoil_fcc.momentum.y = recoil_p4.Py();
  recoil_fcc.momentum.z = recoil_p4.Pz();
  recoil_fcc.mass = recoil_p4.M();
  result.push_back(recoil_fcc);

  return result;
};

sel_axis::sel_axis(bool arg_pos): m_pos(arg_pos) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> sel_axis::operator()(ROOT::VecOps::RVec<float> angle, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  for (size_t i = 0; i < angle.size(); ++i) {
    if (m_pos==1 && angle.at(i)>0.) result.push_back(in.at(i));
    if (m_pos==0 && angle.at(i)<0.) result.push_back(in.at(i));;
  }
  return result;
}


sel_tag::sel_tag(bool arg_pass): m_pass(arg_pass) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> sel_tag::operator()(ROOT::VecOps::RVec<bool> tags, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  for (size_t i = 0; i < in.size(); ++i) {
    if (m_pass) {
      if (tags.at(i)) result.push_back(in.at(i));
    }
    else {
      if (!tags.at(i)) result.push_back(in.at(i));
    }
  }
  return result;
}



// Angular separation between the particles of a collection:
//   arg_delta = 0 / 1 / 2 :   return delta_max, delta_min, delta_average

angular_separationBuilder::angular_separationBuilder( int  arg_delta) : m_delta(arg_delta) {};
float angular_separationBuilder::operator() ( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {

 float result = -9999;

 float dmax = -999;
 float dmin = 999;
 float sum = 0;
 float npairs = 0;
 for (int i=0; i < in.size(); i++) {
  if ( in.at(i).energy < 0) continue;    // "dummy" particle - cf selRP_matched_to_list
  TVector3 p1( in.at(i).momentum.x, in.at(i).momentum.y, in.at(i).momentum.z );
  for (int j=i+1; j < in.size(); j++) {
    if ( in.at(j).energy < 0) continue;   // "dummy" particle
    TVector3 p2( in.at(j).momentum.x, in.at(j).momentum.y, in.at(j).momentum.z );
    float delta_ij = fabs( p1.Angle( p2 ) );
    if ( delta_ij > dmax) dmax = delta_ij;
    if ( delta_ij < dmin) dmin = delta_ij;
    sum = sum + delta_ij;
    npairs ++;
  }
 }
 float delta_max = dmax;
 float delta_min = dmin;
 float delta_ave = sum / npairs;

 if (m_delta == 0 ) result = delta_max;
 if (m_delta == 1 ) result = delta_min;
 if (m_delta == 2 ) result = delta_ave;

 return result;
}


ROOT::VecOps::RVec<float> get_pt(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
 ROOT::VecOps::RVec<float> result;
 for (size_t i = 0; i < in.size(); ++i) {
   result.push_back(sqrt(in[i].momentum.x * in[i].momentum.x + in[i].momentum.y * in[i].momentum.y));
 }
 return result;
}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> merge(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> x, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> y) {
  //to be keept as ROOT::VecOps::RVec
  std::vector<edm4hep::ReconstructedParticleData> result;
  result.reserve(x.size() + y.size());
  result.insert( result.end(), x.begin(), x.end() );
  result.insert( result.end(), y.begin(), y.end() );
  return ROOT::VecOps::RVec(result);
}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
remove(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> x,
       ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> y) {
  //to be kept as ROOT::VecOps::RVec
  std::vector<edm4hep::ReconstructedParticleData> result;
  result.reserve( x.size() );
  result.insert( result.end(), x.begin(), x.end() );
  float epsilon = 1e-8;
  for (size_t i = 0; i < y.size(); ++i) {
    float mass1 = y.at(i).mass;
    float px1 = y.at(i).momentum.x;
    float py1 = y.at(i).momentum.y;
    float pz1 = y.at(i).momentum.z;
    for(std::vector<edm4hep::ReconstructedParticleData>::iterator
          it = std::begin(result); it != std::end(result); ++it) {
      float mass2 = it->mass;
      float px2 = it->momentum.x;
      float py2 = it->momentum.y;
      float pz2 = it->momentum.z;
      if (abs(mass1 - mass2) < epsilon && abs(px1 - px2) < epsilon &&
          abs(py1 - py2) < epsilon && abs(pz1 - pz2) < epsilon) {
        result.erase(it);
        break;
      }
    }
  }
  return ROOT::VecOps::RVec(result);
}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
get(ROOT::VecOps::RVec<int> indexes,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> inParticles) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;

  for (const auto &index : indexes) {
    if (index > -1)
      result.push_back(inParticles.at(index));
  }

  return result;
}

TLorentzVector get_P4vis(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
    TLorentzVector P4sum;
    for (auto & p: in) {
      TLorentzVector tlv;
      tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
      P4sum += tlv;
    }
    return P4sum;
  }


ROOT::VecOps::RVec<float> get_mass(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.mass);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_eta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Eta());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_phi(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Phi());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_e(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.energy);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_p(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.P());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_px(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.x);
  }
  return result;
}


ROOT::VecOps::RVec<float> get_py(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_pz(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.momentum.z);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_charge(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    result.push_back(p.charge);
  }
  return result;
}

ROOT::VecOps::RVec<float> get_y(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Rapidity());
  }
  return result;
}

ROOT::VecOps::RVec<float> get_theta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Theta());
  }
  return result;
}

ROOT::VecOps::RVec<TLorentzVector> get_tlv(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
  ROOT::VecOps::RVec<TLorentzVector> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv);
  }
  return result;
}

TLorentzVector get_tlv(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, int index) {
  TLorentzVector result;
  auto & p = in[index];
  result.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
  return result;
}

TLorentzVector get_tlv(edm4hep::ReconstructedParticleData in) {
  TLorentzVector result;
  result.SetXYZM(in.momentum.x, in.momentum.y, in.momentum.z, in.mass);
  return result;
}

ROOT::VecOps::RVec<int>
get_type(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
  ROOT::VecOps::RVec<int> result;
  for (auto & p: in) {
    result.push_back(p.type);
  }
  return result;
}


int get_n(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> x) {
  int result =  x.size();
  return result;
}

ROOT::VecOps::RVec<bool>
getJet_btag(ROOT::VecOps::RVec<int> index,
            ROOT::VecOps::RVec<edm4hep::ParticleIDData> pid,
            ROOT::VecOps::RVec<float> values) {
  ROOT::VecOps::RVec<bool> result;
  result.resize(index.size());

  for (const auto &idx : index) {
    result.push_back(values.at(pid.at(idx).parameters_begin));
  }

  return result;
}

int getJet_ntags(ROOT::VecOps::RVec<bool> inBJetMask) {
  return std::count_if(inBJetMask.begin(), inBJetMask.end(),
                       [](bool bJet) { return bJet; });
}

// Identify hadronic tau decays from a jet collection and, optionally, extract specific
// sub-components of the decay (e.g. the charged/neutral pions of a 1- or 3-prong decay).
// Efficiency of the code and validation can be found in https://arxiv.org/abs/2601.11383.
//
// Usage: first cluster the event into jets (e.g. clustering_ee_kt(2, 4, 1, 0)), then call this
// function on the jet constituents. For each jet, the algorithm:
//   1) picks the highest-pT charged constituent as the seed ("leading pion"),
//   2) rejects the jet if that seed is below `kLeadPtMin` GeV, or if the jet contains a
//      constituent identified as an electron or muon,
//   3) adds further charged/neutral constituents within `kConeHalfAngle` rad of the running
//      tau direction and above `kCompanionPtMin` GeV,
//   4) classifies the candidate by prong multiplicity (1 or 3 charged tracks, net charge +-1)
//      and photon/neutral-hadron count into a `tauID` (see table below), and discards the
//      candidate (tauID = -2) if its visible mass exceeds `kTauMassMax` GeV.
//
// `request` selects which four-vector is written out for a candidate:
//    0 : full visible tau
//    1 : charged pion with the same charge as the tau
//        (for a 3-prong decay, the one paired with the opposite-charge pion closest to
//        the rho(770) mass; for a 1-prong decay, simply the leading pion)
//    2 : the tau's other component - the opposite-charge pion of the rho pair (3-prong)
//        or the summed neutral system (1-prong)
//    3 : sum of all charged pions
//    4 (or any other value) : summed neutral system only
//   Requests 1-4 only differ from each other in the 3-prong case; for 1-prong decays,
//   1 == the single charged pion and 2/4 == the neutral system.
//
// Output: one edm4hep::ReconstructedParticleData entry per input jet (never skipped), so the
// output vector can be zipped index-by-index with the input jets and filtered by `type`:
//   type == tauID (0-6 for 1-prong, 10-16 for 3-prong, higher tauID = more photons/pi0s found)
//   type == -1  : no charged constituent above kLeadPtMin found in the jet
//   type == -11 : jet contains an electron
//   type == -13 : jet contains a muon
//   type == -2  : visible mass >= kTauMassMax
//   type == -3  : constituents don't form a valid 1- or 3-prong
//   type == -4  : leading charged constituent has |charge| != 1 (not expected in practice)
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> findTauInJet (const ROOT::VecOps::RVec< FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents   >& jets, int request){

  // Constituent mass windows used to veto electrons/muons
  constexpr double kMuonMass = 0.105658;        // GeV
  constexpr double kElectronMass = 0.000510999; // GeV
  constexpr double kMuonMassTol = 1.e-03;
  constexpr double kElectronMassTol = 1.e-05;
  // pT thresholds (GeV)
  constexpr double kLeadPtMin = 2.0;
  constexpr double kCompanionPtMin = 1.0;
  // Half-opening angle (rad) of the cone
  constexpr double kConeHalfAngle = 0.20;
  // Nominal rho(770) mass (GeV)
  constexpr double kRhoMass = 0.775;
  // Reject candidates with a visible mass at or above this (GeV)
  constexpr double kTauMassMax = 3.0;

  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> out;

  for (size_t i = 0; i < jets.size(); ++i) {

    // Full visible tau (0 in request)
    TLorentzVector sum_tau;
    edm4hep::ReconstructedParticleData Tau;
    // Neutral constituents (2 or 4 in request)
    TLorentzVector neutral;
    // Charged constituents (1 or 3 in request)
    TLorentzVector charged;
    // Individual ones
    ROOT::VecOps::RVec<TLorentzVector> charged_vec;
    // Their charge
    ROOT::VecOps::RVec<int> charges_vec;
    // Their track index to access later for track related variables
    ROOT::VecOps::RVec<int> track_vec;

    int tauID = -1;
    int count_piP = 0, count_piM = 0, count_pho = 0;

    // Leading particle
    TLorentzVector lead;
    lead.SetPxPyPzE(0, 0, 0, 0);
    int chargeLead = 0;
    int track = 0;

    FCCAnalyses::JetConstituentsUtils::FCCAnalysesJetConstituents jcs = jets.at(i);

    // First loop through the constituents to find the leading pion.
    for (const auto& jc : jcs) {

      // No electrons or muons in hadronic tau decays
      if (fabs(jc.mass - kMuonMass) < kMuonMassTol) {
        tauID = -13;
        continue;
      }
      if (fabs(jc.mass - kElectronMass) < kElectronMassTol) {
        tauID = -11;
        continue;
      }

      // Now find the leading charged particle
      if (sqrt(jc.momentum.x*jc.momentum.x + jc.momentum.y*jc.momentum.y) > lead.Pt() && jc.charge != 0) {
        lead.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);
        chargeLead = jc.charge;
        track = jc.tracks_begin; // This saves the index in the track collection related to the leading pion
      }
    }

    charges_vec.push_back(chargeLead);
    charged_vec.push_back(lead);
    track_vec.push_back(track);

    if (lead.Pt() < kLeadPtMin) {
      tauID = -1;
      Tau.type = tauID;
      out.push_back(Tau);
      continue;
    } // Too low pt, the particle will be empty but still will show up as an entry

    if (tauID==-13 || tauID==-11) {
      Tau.type = tauID;
      out.push_back(Tau);
      continue;
    } // Leptons in jet, the particle will be empty but still will show up as an entry

    if (chargeLead==1) {
      count_piP++;
    } else if (chargeLead==-1) {
      count_piM++;
    } else {
      // Not expected: the seed passed the charge!=0 check above, so |charge| should be 1.
      Tau.type = -4;
      out.push_back(Tau);
      continue;
    }

    sum_tau += lead;
    charged += lead;

    // Now loop to build the tau adding candidates to the lead only if they satisfy some conditions: distance, charge, etc
    for (const auto& jc : jcs) {

      TLorentzVector tlv;
      tlv.SetPxPyPzE(jc.momentum.x, jc.momentum.y, jc.momentum.z, jc.energy);

      if (tlv==lead) continue;

      // Distance (in terms of Theta) to the running tau direction
      double dTheta = fabs(sum_tau.Theta() - tlv.Theta());

      if (tlv.Pt()<kCompanionPtMin || dTheta>kConeHalfAngle) continue;

      if (jc.charge>0) {
        count_piP++;
        charged += tlv;
        charges_vec.push_back(jc.charge);
        charged_vec.push_back(tlv);
        track_vec.push_back(jc.tracks_begin);
      } else if (jc.charge<0) {
        count_piM++;
        charged += tlv;
        charges_vec.push_back(jc.charge);
        charged_vec.push_back(tlv);
        track_vec.push_back(jc.tracks_begin);
      } else {
        count_pho++;
        neutral += tlv;
      }

      sum_tau += tlv;
    }

    // Lets build the ID : count the charged pions and the neutrals.
    // Considering the decays of the tau, we want candidates with one or three charged candidates (one or three prongs).
    // The ID is then increased depending on the number of photons/neutral hadrons found.

    if (tauID!=-13 && tauID!=-11 && abs(count_piP-count_piM)==1 && ((count_piP+count_piM)==1 || (count_piP+count_piM)==3)) {

      if ((count_piP+count_piM)==1 && count_pho==0) tauID=0;
      if ((count_piP+count_piM)==1 && count_pho==1) tauID=1;
      if ((count_piP+count_piM)==1 && count_pho==2) tauID=2;
      if ((count_piP+count_piM)==1 && count_pho==3) tauID=3;
      if ((count_piP+count_piM)==1 && count_pho==4) tauID=4;
      if ((count_piP+count_piM)==1 && count_pho==5) tauID=5;
      if ((count_piP+count_piM)==1 && count_pho>=6) tauID=6;

      if ((count_piP+count_piM)==3 && count_pho==0) tauID=10;
      if ((count_piP+count_piM)==3 && count_pho==1) tauID=11;
      if ((count_piP+count_piM)==3 && count_pho==2) tauID=12;
      if ((count_piP+count_piM)==3 && count_pho==3) tauID=13;
      if ((count_piP+count_piM)==3 && count_pho==4) tauID=14;
      if ((count_piP+count_piM)==3 && count_pho==5) tauID=15;
      if ((count_piP+count_piM)==3 && count_pho>=6) tauID=16;

      if (request==0) {
        Tau.momentum.x = sum_tau.Px();
        Tau.momentum.y = sum_tau.Py();
        Tau.momentum.z = sum_tau.Pz();
        Tau.mass = sum_tau.M();
        Tau.energy = sum_tau.E();
        Tau.charge = (count_piP-count_piM);
        Tau.type = tauID;
        Tau.tracks_begin = track;
      } else if (request==1 || request==2) {
        // Get the pion from the rho resonance for the request==2
        if ((count_piP+count_piM)==3) {
          // Charge the tau candidate is required to have (+-1); the pion sharing this
          // charge in the opposite-charge pair closest to the rho mass is "second".
          int tauCharge = count_piP - count_piM;
          TLorentzVector second;
          int second_track = -1;
          TLorentzVector third;
          double minMassDifference = -1e6;
          for (size_t iCh = 0; iCh < charges_vec.size(); ++iCh) {
            for (size_t jCh = iCh + 1; jCh < charges_vec.size(); ++jCh) {
              if (charges_vec[iCh] + charges_vec[jCh] == 0) { // opposite charges
                double invMass = (charged_vec[iCh] + charged_vec[jCh]).M();
                double massDifference = std::abs(invMass - kRhoMass);

                if (minMassDifference == -1e6 || massDifference < minMassDifference) {
                  // First candidate pair found, or a smaller mass difference than before
                  minMassDifference = massDifference;
                  // Save the pion with same charge as the tau as the charged one and the other as the neutral
                  if (charges_vec[iCh]==tauCharge) {
                    second = charged_vec[iCh];
                    third = charged_vec[jCh];
                    second_track = track_vec[iCh];
                  } else {
                    second = charged_vec[jCh];
                    third = charged_vec[iCh];
                    second_track = track_vec[jCh];
                  }
                }
              }
            }
          }

          if (request==1) {
            Tau.momentum.x = second.Px();
            Tau.momentum.y = second.Py();
            Tau.momentum.z = second.Pz();
            Tau.mass = second.M();
            Tau.energy = second.E();
            Tau.charge = (count_piP-count_piM);
            Tau.type = tauID;
            Tau.tracks_begin = second_track;
          } else {
            Tau.momentum.x = third.Px();
            Tau.momentum.y = third.Py();
            Tau.momentum.z = third.Pz();
            Tau.mass = third.M();
            Tau.energy = third.E();
            Tau.charge = (count_piP-count_piM); // neutral particle has the same charge as the tau to allow for easy matching
            Tau.type = tauID;
            Tau.tracks_begin = second_track; // and same track index as the charged
          }
        } else {
          // 1-prong: only one charged pion exists, so it is trivially "the pion with the
          // same charge as the tau" (request==1); the neutral system is everything else.
          if (request==1) {
            Tau.momentum.x = lead.Px();
            Tau.momentum.y = lead.Py();
            Tau.momentum.z = lead.Pz();
            Tau.mass = lead.M();
            Tau.energy = lead.E();
            Tau.charge = (count_piP-count_piM);
            Tau.type = tauID;
            Tau.tracks_begin = track;
          } else {
            // The only charged constituent is the lead, so the neutral system is exactly
            // `neutral` (using it directly avoids the floating point cancellation of
            // computing sum_tau - lead).
            Tau.momentum.x = neutral.Px();
            Tau.momentum.y = neutral.Py();
            Tau.momentum.z = neutral.Pz();
            Tau.mass = neutral.M();
            Tau.energy = neutral.E();
            Tau.charge = (count_piP-count_piM); // neutral particle has the same charge as the tau to allow for easy matching
            Tau.type = tauID;
            Tau.tracks_begin = track; // and same track index as the charged
          }
        }
      } else if (request==3) {
        Tau.momentum.x = charged.Px();
        Tau.momentum.y = charged.Py();
        Tau.momentum.z = charged.Pz();
        Tau.mass = charged.M();
        Tau.energy = charged.E();
        Tau.charge = (count_piP-count_piM);
        Tau.type = tauID;
        Tau.tracks_begin = track;
      } else {
        Tau.momentum.x = neutral.Px();
        Tau.momentum.y = neutral.Py();
        Tau.momentum.z = neutral.Pz();
        Tau.mass = neutral.M();
        Tau.energy = neutral.E();
        Tau.charge = (count_piP-count_piM); // neutral particle has the same charge as the tau to allow for easy matching
        Tau.type = tauID;
        Tau.tracks_begin = track; // and same track index as the charged
      }

      // Save taus (or its components) with mass below kTauMassMax
      if (sum_tau.M() < kTauMassMax) {
        out.push_back(Tau);
      } else {
        // Reset the particle if it's not a tau but keep a different ID to identify the cause
        Tau.momentum.x = 0;
        Tau.momentum.y = 0;
        Tau.momentum.z = 0;
        Tau.mass = 0;
        Tau.energy = 0;
        Tau.charge = 0;
        Tau.type = -2;
        out.push_back(Tau);
      }
    } else {
      // Prong number not matched
      Tau.type = -3;
      out.push_back(Tau);
    }
  }
  return out;
}

} // namespace FCCAnalyses::ReconstructedParticle
