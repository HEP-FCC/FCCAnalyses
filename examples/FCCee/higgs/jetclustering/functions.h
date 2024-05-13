#ifndef ZHfunctions_H
#define ZHfunctions_H

#include <cmath>
#include <vector>
#include <math.h>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"
#include "ReconstructedParticle2MC.h"


namespace FCCAnalyses { 

// make Lorentzvectors from pseudojets
Vec_tlv makeLorentzVectors(Vec_f jets_px, Vec_f jets_py, Vec_f jets_pz, Vec_f jets_e) {
    Vec_tlv result;
    for(int i=0; i<jets_px.size(); i++) {
        TLorentzVector tlv;
        tlv.SetPxPyPzE(jets_px[i], jets_py[i], jets_pz[i], jets_e[i]);
        result.push_back(tlv);
    }
    return result;
}

Vec_i jetTruthFinder(std::vector<std::vector<int>> constituents, Vec_rp reco, Vec_mc mc, Vec_i mcind, bool findGluons = false) {
    // jet truth=finder: match the gen-level partons (eventually with gluons) with the jet constituents
    // matching by mimimizing the sum of dr of the parton and all the jet constituents 

    Vec_tlv genQuarks; // Lorentz-vector of potential partons (gen-level)
    Vec_i genQuarks_pdgId; // corresponding PDG ID
    for(size_t i = 0; i < mc.size(); ++i) {
        int pdgid = abs(mc.at(i).PDG);
        if(pdgid > 6 and not findGluons) continue; // only quarks 
        if(pdgid > 6 and pdgid != 21 and findGluons) continue; // only quarks and gluons
        TLorentzVector tlv;
        tlv.SetXYZM(mc.at(i).momentum.x,mc.at(i).momentum.y,mc.at(i).momentum.z,mc.at(i).mass);
        genQuarks.push_back(tlv);
        genQuarks_pdgId.push_back(mc.at(i).PDG);
    }

    Vec_tlv recoParticles; // Lorentz-vector of all reconstructed particles
    for(size_t i = 0; i < reco.size(); ++i) {
        auto & p = reco[i];
        TLorentzVector tlv;
        tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
        recoParticles.push_back(tlv);
    }

    Vec_i usedIdx;
    Vec_i result;
    for(size_t iJet = 0; iJet < constituents.size(); ++iJet) {
        Vec_d dr;
        for(size_t iGen = 0; iGen < genQuarks.size(); ++iGen) {
            if(std::find(usedIdx.begin(), usedIdx.end(), iGen) != usedIdx.end()) {
                dr.push_back(1e99); // set infinite dr, skip
                continue;
            }
            dr.push_back(0);
            for(size_t i = 0; i < constituents[iJet].size(); ++i) {
                dr[iGen] += recoParticles[constituents[iJet][i]].DeltaR(genQuarks[iGen]);
            }
        }
        int maxDrIdx = std::min_element(dr.begin(),dr.end()) - dr.begin();
        usedIdx.push_back(maxDrIdx);
        result.push_back(genQuarks_pdgId[maxDrIdx]);

    }
    return result;
}





}

#endif