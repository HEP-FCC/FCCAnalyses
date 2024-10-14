// library with extra functions needed by custom FCC-hh analysis, such as
// HHbbZZ(llvv) analysis

#ifndef ANALYSIS_FCCHH_ANALYZERS_H
#define ANALYSIS_FCCHH_ANALYZERS_H

#include "ROOT/RVec.hxx"
#include "TLorentzVector.h"
#include "TString.h"

#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"
#include "edm4hep/ReconstructedParticleData.h"
#include "podio/ObjectID.h"

#include <iostream>

namespace AnalysisFCChh {

/// TESTER: return the transverse momenta of the input ReconstructedParticles
// ROOT::VecOps::RVec<float>
// get_pt_test(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);

// helpers for reco particles:
TLorentzVector getTLV_reco(edm4hep::ReconstructedParticleData reco_part);
TLorentzVector getTLV_MC(edm4hep::MCParticleData MC_part);

// struct to use for a pair of two reco particles, to make sure the correct ones
// stay together
struct RecoParticlePair {
  edm4hep::ReconstructedParticleData particle_1;
  edm4hep::ReconstructedParticleData particle_2;
  TLorentzVector merged_TLV() {
    TLorentzVector tlv_1 = getTLV_reco(particle_1);
    TLorentzVector tlv_2 = getTLV_reco(particle_2);
    return tlv_1 + tlv_2;
  }
  void sort_by_pT() {
    double pT_1 = sqrt(particle_1.momentum.x * particle_1.momentum.x +
                       particle_1.momentum.y * particle_1.momentum.y);
    double pT_2 = sqrt(particle_2.momentum.x * particle_2.momentum.x +
                       particle_2.momentum.y * particle_2.momentum.y);

    if (pT_1 >= pT_2) {
      return;
    } // nothing to do if already sorted corrected
    else {
      edm4hep::ReconstructedParticleData sublead = particle_1;

      particle_1 = particle_2;
      particle_2 = sublead;
      return;
    }
  }
};

// same for MC particle
struct MCParticlePair {
  edm4hep::MCParticleData particle_1;
  edm4hep::MCParticleData particle_2;
  TLorentzVector merged_TLV() {
    TLorentzVector tlv_1 = getTLV_MC(particle_1);
    TLorentzVector tlv_2 = getTLV_MC(particle_2);
    return tlv_1 + tlv_2;
  }
  void sort_by_pT() {
    double pT_1 = sqrt(particle_1.momentum.x * particle_1.momentum.x +
                       particle_1.momentum.y * particle_1.momentum.y);
    double pT_2 = sqrt(particle_2.momentum.x * particle_2.momentum.x +
                       particle_2.momentum.y * particle_2.momentum.y);

    if (pT_1 >= pT_2) {
      return;
    } // nothing to do if already sorted corrected
    else {
      edm4hep::MCParticleData sublead = particle_1;

      particle_1 = particle_2;
      particle_2 = sublead;
      return;
    }
  }
};

// merge the particles in such a pair into one edm4hep:RecoParticle to use with
// other functions (in a vector)
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
merge_pairs(ROOT::VecOps::RVec<RecoParticlePair> pairs);
int get_n_pairs(ROOT::VecOps::RVec<RecoParticlePair> pairs);
ROOT::VecOps::RVec<RecoParticlePair>
get_first_pair(ROOT::VecOps::RVec<RecoParticlePair>
                   pairs); // can use to get leading pair if the inputs to pair
                           // finding fct were pT sorted

// functions to separate the pair again - ONLY DOES THIS FOR THE FIRST PAIR IN
// THE VECTOR
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
get_first_from_pair(ROOT::VecOps::RVec<RecoParticlePair> pairs);
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
get_second_from_pair(ROOT::VecOps::RVec<RecoParticlePair> pairs);

// truth filter used to get ZZ(llvv) events from the ZZ(llvv+4l+4v) inclusive
// signal samples
bool ZZllvvFilter(ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles,
                  ROOT::VecOps::RVec<podio::ObjectID> daughter_ids);
bool WWlvlvFilter(ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles,
                  ROOT::VecOps::RVec<podio::ObjectID> daughter_ids,
                  ROOT::VecOps::RVec<podio::ObjectID> parent_ids);

// helper functions for the ZZllv truth filter:
bool isStablePhoton(edm4hep::MCParticleData truth_part);
bool isPhoton(edm4hep::MCParticleData truth_part);
bool isLep(edm4hep::MCParticleData truth_part);
bool isLightLep(edm4hep::MCParticleData truth_part);
bool isNeutrino(edm4hep::MCParticleData truth_part);
bool isQuark(edm4hep::MCParticleData truth_part);
bool isZ(edm4hep::MCParticleData truth_part);
bool isW(edm4hep::MCParticleData truth_part);
bool isTau(edm4hep::MCParticleData truth_part);
bool isH(edm4hep::MCParticleData truth_part);
bool isb(edm4hep::MCParticleData truth_part);
bool isHadron(edm4hep::MCParticleData truth_part);
bool isTop(edm4hep::MCParticleData truth_part);
bool isGluon(edm4hep::MCParticleData truth_part);
bool isc(edm4hep::MCParticleData truth_part);
bool iss(edm4hep::MCParticleData truth_part);
bool isMuon(edm4hep::MCParticleData truth_part);
int checkZDecay(edm4hep::MCParticleData truth_Z,
                ROOT::VecOps::RVec<podio::ObjectID> daughter_ids,
                ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles);
int checkWDecay(edm4hep::MCParticleData truth_W,
                ROOT::VecOps::RVec<podio::ObjectID> daughter_ids,
                ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles);
int findTopDecayChannel(
    ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles,
    ROOT::VecOps::RVec<podio::ObjectID> daughter_ids);
int findHiggsDecayChannel(
    ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles,
    ROOT::VecOps::RVec<podio::ObjectID> daughter_ids);

// truth level fct to get a Z->ll truth decay
ROOT::VecOps::RVec<edm4hep::MCParticleData>
getTruthZll(ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles,
            ROOT::VecOps::RVec<podio::ObjectID> daughter_ids);

// find the SFOS pair of reconstructed leptons (electrons or muons)
ROOT::VecOps::RVec<RecoParticlePair>
getOSPairs(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> leptons_in);
ROOT::VecOps::RVec<RecoParticlePair> getDFOSPairs(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> electrons_in,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> muons_in);
// ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
// getOSPair(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> leptons_in);
ROOT::VecOps::RVec<RecoParticlePair> getBestOSPair(
    ROOT::VecOps::RVec<RecoParticlePair> electron_pairs,
    ROOT::VecOps::RVec<RecoParticlePair> muon_pairs); // closest to Z mass
ROOT::VecOps::RVec<RecoParticlePair>
getLeadingPair(ROOT::VecOps::RVec<RecoParticlePair> electron_pairs,
               ROOT::VecOps::RVec<RecoParticlePair>
                   muon_pairs); // pair with leading pT(pair)

// make a general pair, not caring about charges, e.g. the two b-jets
ROOT::VecOps::RVec<RecoParticlePair>
getPairs(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> particles_in);
ROOT::VecOps::RVec<RecoParticlePair> getPair_sublead(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> particles_in);
ROOT::VecOps::RVec<MCParticlePair>
getPairs(ROOT::VecOps::RVec<edm4hep::MCParticleData> particles_in);

// SORT OBJ COLLECTION
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> SortParticleCollection(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> particles_in);

// btags
ROOT::VecOps::RVec<bool>
getJet_tag(ROOT::VecOps::RVec<int> index,
           ROOT::VecOps::RVec<edm4hep::ParticleIDData> pid,
           ROOT::VecOps::RVec<float> values, int algoIndex);
ROOT::VecOps::RVec<edm4hep::MCParticleData>
getBhadron(ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles,
           ROOT::VecOps::RVec<podio::ObjectID> parent_ids);
ROOT::VecOps::RVec<edm4hep::MCParticleData>
getChadron(ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles,
           ROOT::VecOps::RVec<podio::ObjectID> parent_ids);
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
get_tagged_jets(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> jets,
                ROOT::VecOps::RVec<edm4hep::ParticleIDData> jet_tags,
                ROOT::VecOps::RVec<podio::ObjectID> jet_tags_indices,
                ROOT::VecOps::RVec<float> jet_tags_values, int algoIndex);
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
get_untagged_jets(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> jets,
                  ROOT::VecOps::RVec<int> index,
                  ROOT::VecOps::RVec<edm4hep::ParticleIDData> pid,
                  ROOT::VecOps::RVec<float> values, int algoIndex);

// tau jets
ROOT::VecOps::RVec<edm4hep::MCParticleData> find_truth_matches(
    ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_parts,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco_particles,
    float dR_thres);
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
get_tau_jets(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> jets,
             ROOT::VecOps::RVec<int> index,
             ROOT::VecOps::RVec<edm4hep::ParticleIDData> pid,
             ROOT::VecOps::RVec<float> tag_values, int algoIndex);
ROOT::VecOps::RVec<edm4hep::MCParticleData>
getTruthTauHads(ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles,
                ROOT::VecOps::RVec<podio::ObjectID> daughter_ids,
                ROOT::VecOps::RVec<podio::ObjectID> parent_ids, TString type);
ROOT::VecOps::RVec<edm4hep::MCParticleData>
getTruthTau(ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles,
            ROOT::VecOps::RVec<podio::ObjectID> daughter_ids,
            ROOT::VecOps::RVec<podio::ObjectID> parent_ids, TString type);
ROOT::VecOps::RVec<edm4hep::MCParticleData>
getTruthTauLeps(ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles,
                ROOT::VecOps::RVec<podio::ObjectID> daughter_ids,
                ROOT::VecOps::RVec<podio::ObjectID> parent_ids, TString type);
// isolation: select only those particles of sel_parts that are isolated by the
// given dR from the check_parts
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
sel_isolated(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> sel_parts,
             ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> check_parts,
             float dR_thres = 0.4);

// merge two four vectors into one to create a new particle (follow vector
// structure to be able to use with other RecoParticle fcts easily like get_pt
// etc.)
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> merge_parts_TLVs(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> particle_1,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> particle_2);
ROOT::VecOps::RVec<edm4hep::MCParticleData>
merge_parts_TLVs(ROOT::VecOps::RVec<edm4hep::MCParticleData> particle_1,
                 ROOT::VecOps::RVec<edm4hep::MCParticleData> particle_2);

// reco level quantities
// transverse masses:
ROOT::VecOps::RVec<float>
get_mT(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> particle_1,
       ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> particle_2);
ROOT::VecOps::RVec<float>
get_mT_new(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> particle_1,
           ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> particle_2);
ROOT::VecOps::RVec<float>
get_m_pseudo(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> Z_ll_pair,
             ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> MET_obj);
ROOT::VecOps::RVec<float>
get_mT_pseudo(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> Z_ll_pair,
              ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> MET_obj);
TLorentzVector getTLV_MET(edm4hep::ReconstructedParticleData met_object);

// stransverse mass mT2 :
// https://www.hep.phy.cam.ac.uk/~lester/mt2/#Alternatives
// ROOT::VecOps::RVec<float>
// get_mT2(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> particle_1,
// ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> particle_2,
// ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> MET_obj);
// ROOT::VecOps::RVec<float>
// get_mT2_125(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
// particle_1, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
// particle_2, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> MET_obj);

// angular distances:function can return dR, dEta, dPhi for any two fully
// reconstructed particles that have a full 4 vector
ROOT::VecOps::RVec<float> get_angularDist(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> particle_1,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> particle_2,
    TString type = "dR");
ROOT::VecOps::RVec<float> get_angularDist_MET(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> particle_1,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> MET_obj,
    TString type = "dR");

ROOT::VecOps::RVec<float>
get_angularDist_pair(ROOT::VecOps::RVec<RecoParticlePair> pairs,
                     TString type = "dR");
ROOT::VecOps::RVec<float>
get_angularDist_pair(ROOT::VecOps::RVec<MCParticlePair> pairs,
                     TString type = "dR");

// HT variables
ROOT::VecOps::RVec<float>
get_HT2(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> particle_1,
        ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> particle_2);
ROOT::VecOps::RVec<float>
get_HT_wInv(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> MET,
            ROOT::VecOps::RVec<RecoParticlePair> ll_pair,
            ROOT::VecOps::RVec<RecoParticlePair> bb_pair);
ROOT::VecOps::RVec<float>
get_HT_true(ROOT::VecOps::RVec<RecoParticlePair> ll_pair,
            ROOT::VecOps::RVec<RecoParticlePair> bb_pair);
ROOT::VecOps::RVec<float> get_HT2_ratio(ROOT::VecOps::RVec<float> HT2,
                                        ROOT::VecOps::RVec<float> HT_wInv);
ROOT::VecOps::RVec<float>
get_MET_significance(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> MET,
                     ROOT::VecOps::RVec<float> HT_true, bool doSqrt = true);

// reco mass of lepton+b-jet, to try suppress ttbar processes
ROOT::VecOps::RVec<RecoParticlePair>
make_lb_pairing(ROOT::VecOps::RVec<RecoParticlePair> lepton_pair,
                ROOT::VecOps::RVec<RecoParticlePair> bb_pair);
ROOT::VecOps::RVec<float>
get_mlb_reco(ROOT::VecOps::RVec<RecoParticlePair> lb_pairs);
ROOT::VecOps::RVec<float>
get_mlb_MET_reco(ROOT::VecOps::RVec<RecoParticlePair> lb_pairs,
                 ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> MET);

// for separating bbWW and bbtautau?
ROOT::VecOps::RVec<float>
get_pzeta_vis(ROOT::VecOps::RVec<RecoParticlePair> lepton_pair);
ROOT::VecOps::RVec<float>
get_pzeta_miss(ROOT::VecOps::RVec<RecoParticlePair> lepton_pair,
               ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> MET);
ROOT::VecOps::RVec<float> get_dzeta(ROOT::VecOps::RVec<float> pzeta_miss,
                                    ROOT::VecOps::RVec<float> pzeta_vis,
                                    float factor = 0.85);

// combine particles:
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
build_HZZ(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> Z_ll_pair,
          ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> MET_obj);

// retrieve children from a given truth particle
ROOT::VecOps::RVec<edm4hep::MCParticleData> get_immediate_children(
    edm4hep::MCParticleData truth_part,
    ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles,
    ROOT::VecOps::RVec<podio::ObjectID> daughter_ids);

// select the truth Higgs, depending on which particles it decays to:
ROOT::VecOps::RVec<edm4hep::MCParticleData>
get_truth_Higgs(ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles,
                ROOT::VecOps::RVec<podio::ObjectID> daughter_ids,
                TString decay = "ZZ");
ROOT::VecOps::RVec<edm4hep::MCParticleData>
get_truth_Z_decay(ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles,
                  ROOT::VecOps::RVec<podio::ObjectID> daughter_ids,
                  TString decay = "ZZ");

// Filters and specifics for the bbtautau analysis:
bool isFromHadron(edm4hep::MCParticleData truth_part,
                  ROOT::VecOps::RVec<podio::ObjectID> parent_ids,
                  ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles);
bool hasHiggsParent(
    edm4hep::MCParticleData truth_part,
    ROOT::VecOps::RVec<podio::ObjectID> parent_ids,
    ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles);
bool isFromHiggsDirect(
    edm4hep::MCParticleData truth_part,
    ROOT::VecOps::RVec<podio::ObjectID> parent_ids,
    ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles);
bool isChildOfTauFromHiggs(
    edm4hep::MCParticleData truth_part,
    ROOT::VecOps::RVec<podio::ObjectID> parent_ids,
    ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles);
bool isChildOfWFromHiggs(
    edm4hep::MCParticleData truth_part,
    ROOT::VecOps::RVec<podio::ObjectID> parent_ids,
    ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles);
bool isChildOfZFromHiggs(
    edm4hep::MCParticleData truth_part,
    ROOT::VecOps::RVec<podio::ObjectID> parent_ids,
    ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles);
ROOT::VecOps::RVec<edm4hep::MCParticleData>
getLepsFromTau(ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles,
               ROOT::VecOps::RVec<podio::ObjectID> parent_ids);
ROOT::VecOps::RVec<edm4hep::MCParticleData>
getLepsFromW(ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles,
             ROOT::VecOps::RVec<podio::ObjectID> parent_ids);
ROOT::VecOps::RVec<edm4hep::MCParticleData>
getLepsFromZ(ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles,
             ROOT::VecOps::RVec<podio::ObjectID> parent_ids);
ROOT::VecOps::RVec<edm4hep::MCParticleData>
getPhotonsFromH(ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles,
                ROOT::VecOps::RVec<podio::ObjectID> parent_ids);
ROOT::VecOps::RVec<int> getTruthLepLepFlavour(
    ROOT::VecOps::RVec<edm4hep::MCParticleData> leps_from_tau);
ROOT::VecOps::RVec<edm4hep::MCParticleData>
getTruthEle(ROOT::VecOps::RVec<edm4hep::MCParticleData> leps_from_tau);
ROOT::VecOps::RVec<edm4hep::MCParticleData>
getTruthMu(ROOT::VecOps::RVec<edm4hep::MCParticleData> leps_from_tau);

// tautau specific masses/variables
ROOT::VecOps::RVec<float> get_x_fraction(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> visible_particle,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> MET);
ROOT::VecOps::RVec<float> get_x_fraction_truth(
    ROOT::VecOps::RVec<edm4hep::MCParticleData> visible_particle,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> MET);
ROOT::VecOps::RVec<float> get_mtautau_col(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> ll_pair_merged,
    ROOT::VecOps::RVec<float> x1, ROOT::VecOps::RVec<float> x2);
ROOT::VecOps::RVec<float> get_mbbtautau_col(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> bb_pair_merged,
    ROOT::VecOps::RVec<float> mtautau_col);

// truth matching:
//  old function that can match only 1 particle -> TO REMOVE?
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> find_reco_matched(
    ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_parts_to_match,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco_parts_all,
    float dR_thres = 0.1);

// isolation criterion, delphes style. flag exclude_light_leps does not check
// for isolation of test_parts vs electrons or muons (using the mass) as seems
// to be done in FCC-hh delphes sim
ROOT::VecOps::RVec<float> get_IP_delphes(
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> test_parts,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco_parts_all,
    float dR_min = 0.3, float pT_min = 0.5, bool exclude_light_leps = true);

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
filter_lightLeps(ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind,
                 ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
                 ROOT::VecOps::RVec<edm4hep::MCParticleData> mc);

// truth MET
ROOT::VecOps::RVec<edm4hep::MCParticleData>
getNusFromW(ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles,
            ROOT::VecOps::RVec<podio::ObjectID> parent_ids);
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
getTruthMETObj(ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles,
               ROOT::VecOps::RVec<podio::ObjectID> parent_ids,
               TString type = "hww_only");

// for checking signal efficiencies in delphes card validation
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> find_reco_matches(
    ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_parts,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco_particles,
    float dR_thres = 0.1);
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
find_reco_matches_no_remove(
    ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_parts,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco_particles,
    float dR_thres = 0.1);
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
find_reco_matches_exclusive(
    ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_parts,
    ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_parts_exc,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco_particles,
    float dR_thres = 0.1);
ROOT::VecOps::RVec<int> find_reco_match_indices(
    ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_parts,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco_particles,
    float dR_thres = 0.1);
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
find_reco_matched_particle(
    edm4hep::MCParticleData truth_part_to_match,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> check_reco_parts,
    float dR_thres = 0.1);
ROOT::VecOps::RVec<edm4hep::MCParticleData> find_mc_matched_particle(
    edm4hep::ReconstructedParticleData reco_part_to_match,
    ROOT::VecOps::RVec<edm4hep::MCParticleData> check_mc_parts,
    float dR_thres = 0.1);
ROOT::VecOps::RVec<int> find_reco_matched_index(
    edm4hep::MCParticleData truth_part_to_match,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> check_reco_parts,
    float dR_thres = 0.1);
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
find_true_signal_leps_reco_matches(
    ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_leps_to_match,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco_electrons,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco_muons,
    float dR_thres = 0.1);
ROOT::VecOps::RVec<int> find_truth_to_reco_matches_indices(
    ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_leps_to_match,
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco_parts,
    int pdg_ID, float dR_thres = 0.1);

// retrieving isoVar from delphes:
//  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
//  get_isoVar(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
//  reco_parts_to_check, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>
//  all_reco_parts);

// template function for getting vector via indices - needed to read e.g.
// UserDataCollections
template <typename T>
ROOT::VecOps::RVec<T> get(const ROOT::VecOps::RVec<int> &index,
                          const ROOT::VecOps::RVec<T> &in) {
  ROOT::VecOps::RVec<T> result;
  result.reserve(index.size());
  for (size_t i = 0; i < index.size(); ++i) {
    if (index[i] > -1)
      result.push_back(in[index[i]]);
  }
  return result;
}

} // namespace AnalysisFCChh

#endif
