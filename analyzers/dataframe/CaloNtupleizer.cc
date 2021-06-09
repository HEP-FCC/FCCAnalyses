#include "CaloNtupleizer.h"
#include "TVector3.h"
#include "TLorentzVector.h"

#include <math.h>

using namespace CaloNtupleizer;

// calo hit
ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloHit_x (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.x);
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloHit_y (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloHit_z (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.z);
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloHit_phi (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Phi());
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloHit_theta (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Theta());
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloHit_eta (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Eta());
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloHit_energy (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.energy);
  }
  return result;
}

ROOT::VecOps::RVec<TVector3> CaloNtupleizer::getCaloHit_positionVector3 (ROOT::VecOps::RVec<edm4hep::CalorimeterHitData> in){
  ROOT::VecOps::RVec<TVector3> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3);
  }
  return result;
}

// calo cluster
ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloCluster_x (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.x);
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloCluster_y (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloCluster_z (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.z);
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloCluster_phi (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Phi());
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloCluster_theta (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Theta());
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloCluster_eta (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Eta());
  }
  return result;
}

ROOT::VecOps::RVec<float> CaloNtupleizer::getCaloCluster_energy (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.energy);
  }
  return result;
}

ROOT::VecOps::RVec<TVector3> CaloNtupleizer::getCaloCluster_positionVector3 (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<TVector3> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3);
  }
  return result;
}

ROOT::VecOps::RVec<int> CaloNtupleizer::getCaloCluster_firstCell (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<int> result;
  for (auto & p: in){
    result.push_back(p.hits_begin);
  }
  return result;
}

ROOT::VecOps::RVec<int> CaloNtupleizer::getCaloCluster_lastCell (ROOT::VecOps::RVec<edm4hep::ClusterData> in){
  ROOT::VecOps::RVec<int> result;
  for (auto & p: in){
    result.push_back(p.hits_end);
  }
  return result;
}

//// MC particles
//ROOT::VecOps::RVec<float> getMC_phi (ROOT::VecOps::RVec<fcc::MCParticleData> in){
//    ROOT::VecOps::RVec<float> result;
//    for (auto & p: in){
//        TLorentzVector fourvec;
//        fourvec.SetPxPyPzE(p.core.p4.px, p.core.p4.py, p.core.p4.pz, sqrt(p.core.p4.px * p.core.p4.px + p.core.p4.py * p.core.p4.py + p.core.p4.pz * p.core.p4.pz + p.core.p4.mass * p.core.p4.mass));
//        result.push_back(fourvec.Phi());
//    }
//    return result;
//}
//
//ROOT::VecOps::RVec<float> getMC_theta (ROOT::VecOps::RVec<fcc::MCParticleData> in){
//    ROOT::VecOps::RVec<float> result;
//    for (auto & p: in){
//        TLorentzVector fourvec;
//        fourvec.SetPxPyPzE(p.core.p4.px, p.core.p4.py, p.core.p4.pz, sqrt(p.core.p4.px * p.core.p4.px + p.core.p4.py * p.core.p4.py + p.core.p4.pz * p.core.p4.pz + p.core.p4.mass * p.core.p4.mass));
//        result.push_back(fourvec.Theta());
//    }
//    return result;
//}
//
//ROOT::VecOps::RVec<float> getMC_eta (ROOT::VecOps::RVec<fcc::MCParticleData> in){
//    ROOT::VecOps::RVec<float> result;
//    for (auto & p: in){
//        TLorentzVector fourvec;
//        fourvec.SetPxPyPzE(p.core.p4.px, p.core.p4.py, p.core.p4.pz, sqrt(p.core.p4.px * p.core.p4.px + p.core.p4.py * p.core.p4.py + p.core.p4.pz * p.core.p4.pz + p.core.p4.mass * p.core.p4.mass));
//        result.push_back(fourvec.Eta());
//    }
//    return result;
//}
//
//ROOT::VecOps::RVec<float> getMC_energy (ROOT::VecOps::RVec<fcc::MCParticleData> in){
//    ROOT::VecOps::RVec<float> result;
//    for (auto & p: in){
//        TLorentzVector fourvec;
//        fourvec.SetPxPyPzE(p.core.p4.px, p.core.p4.py, p.core.p4.pz, sqrt(p.core.p4.px * p.core.p4.px + p.core.p4.py * p.core.p4.py + p.core.p4.pz * p.core.p4.pz + p.core.p4.mass * p.core.p4.mass));
//        result.push_back(fourvec.E());
//    }
//    return result;
//}
//
//ROOT::VecOps::RVec<TLorentzVector> getMC_lorentzVector (ROOT::VecOps::RVec<fcc::MCParticleData> in){
//    ROOT::VecOps::RVec<TLorentzVector> result;
//    for (auto & p: in){
//        TLorentzVector fourvec;
//        fourvec.SetPxPyPzE(p.core.p4.px, p.core.p4.py, p.core.p4.pz, sqrt(p.core.p4.px * p.core.p4.px + p.core.p4.py * p.core.p4.py + p.core.p4.pz * p.core.p4.pz + p.core.p4.mass * p.core.p4.mass));
//        result.push_back(fourvec);
//    }
//    return result;
//}
//
//ROOT::VecOps::RVec<int> getMC_pid (ROOT::VecOps::RVec<fcc::MCParticleData> in){
//    ROOT::VecOps::RVec<int> result;
//    for (auto & p: in){
//        result.push_back(p.core.pdgId);
//    }
//    return result;
//}
//
//ROOT::VecOps::RVec<int> getMC_status (ROOT::VecOps::RVec<fcc::MCParticleData> in){
//    ROOT::VecOps::RVec<int> result;
//    for (auto & p: in){
//        result.push_back(p.core.status);
//    }
//    return result;
//}
