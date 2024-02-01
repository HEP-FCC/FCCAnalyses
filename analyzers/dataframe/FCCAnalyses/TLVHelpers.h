#ifndef TLVHelpers_ANALYZERS_H
#define TLVHelpers_ANALYZERS_H

#include "Math/Vector4D.h"
#include "ROOT/RVec.hxx"

namespace FCCAnalyses {
  namespace TLVHelpers {
    ROOT::VecOps::RVec<float> get_e(const ROOT::VecOps::RVec<TLorentzVector> &in_tlv) {
      ROOT::VecOps::RVec<float> result;
      for (auto &p : in_tlv) {
        result.push_back(p.E());
      }
      return result; 
    }

    ROOT::VecOps::RVec<float>
    get_px(const ROOT::VecOps::RVec<TLorentzVector> &in_tlv) {
      ROOT::VecOps::RVec<float> result;
      for (auto &p : in_tlv) {
        result.push_back(p.Px());
      }
      return result;
    }
    ROOT::VecOps::RVec<float>
    get_py(const ROOT::VecOps::RVec<TLorentzVector> &in_tlv) {
      ROOT::VecOps::RVec<float> result;
      for (auto &p : in_tlv) {
        result.push_back(p.Py());
      }
      return result;
    }

    ROOT::VecOps::RVec<float>
    get_pz(const ROOT::VecOps::RVec<TLorentzVector> &in_tlv) {
      ROOT::VecOps::RVec<float> result;
      for (auto &p : in_tlv) {
        result.push_back(p.Pz());
      }
      return result;
    }
  }
}
#endif

