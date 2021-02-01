#include "CalorimeterReco.h"
#include "TVector3.h"
#include "TLorentzVector.h"

#include <math.h>

// calo hit
ROOT::VecOps::RVec<float> getCaloHit_x (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.x);
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloHit_y (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloHit_z (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.z);
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloHit_phi (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Phi());
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloHit_theta (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Theta());
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloHit_eta (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Eta());
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloHit_energy (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.core.energy);
  }
  return result;
}

ROOT::VecOps::RVec<TVector3> getCaloHit_positionVector3 (ROOT::VecOps::RVec<fcc::PositionedCaloHitData> in){
  ROOT::VecOps::RVec<TVector3> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3);
  }
  return result;
}

// calo cluster
ROOT::VecOps::RVec<float> getCaloCluster_x (ROOT::VecOps::RVec<fcc::CaloClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.core.position.x);
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloCluster_y (ROOT::VecOps::RVec<fcc::CaloClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.core.position.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloCluster_z (ROOT::VecOps::RVec<fcc::CaloClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.core.position.z);
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloCluster_phi (ROOT::VecOps::RVec<fcc::CaloClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.core.position.x, p.core.position.y, p.core.position.z);
    result.push_back(t3.Phi());
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloCluster_theta (ROOT::VecOps::RVec<fcc::CaloClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.core.position.x, p.core.position.y, p.core.position.z);
    result.push_back(t3.Theta());
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloCluster_eta (ROOT::VecOps::RVec<fcc::CaloClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.core.position.x, p.core.position.y, p.core.position.z);
    result.push_back(t3.Eta());
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloCluster_energy (ROOT::VecOps::RVec<fcc::CaloClusterData> in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.core.energy);
  }
  return result;
}

ROOT::VecOps::RVec<TVector3> getCaloCluster_positionVector3 (ROOT::VecOps::RVec<fcc::CaloClusterData> in){
  ROOT::VecOps::RVec<TVector3> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.core.position.x, p.core.position.y, p.core.position.z);
    result.push_back(t3);
  }
  return result;
}

ROOT::VecOps::RVec<int> getCaloCluster_firstCell (ROOT::VecOps::RVec<fcc::CaloClusterData> in){
  ROOT::VecOps::RVec<int> result;
  for (auto & p: in){
    result.push_back(p.hits_begin);
  }
  return result;
}

ROOT::VecOps::RVec<int> getCaloCluster_lastCell (ROOT::VecOps::RVec<fcc::CaloClusterData> in){
  ROOT::VecOps::RVec<int> result;
  for (auto & p: in){
    result.push_back(p.hits_end);
  }
  return result;
}

// MC particles
ROOT::VecOps::RVec<float> getMC_phi (ROOT::VecOps::RVec<fcc::MCParticleData> in){
    ROOT::VecOps::RVec<float> result;
    for (auto & p: in){
        TLorentzVector fourvec;
        fourvec.SetPxPyPzE(p.core.p4.px, p.core.p4.py, p.core.p4.pz, sqrt(p.core.p4.px * p.core.p4.px + p.core.p4.py * p.core.p4.py + p.core.p4.pz * p.core.p4.pz + p.core.p4.mass * p.core.p4.mass));
        result.push_back(fourvec.Phi());
    }
    return result;
}

ROOT::VecOps::RVec<float> getMC_theta (ROOT::VecOps::RVec<fcc::MCParticleData> in){
    ROOT::VecOps::RVec<float> result;
    for (auto & p: in){
        TLorentzVector fourvec;
        fourvec.SetPxPyPzE(p.core.p4.px, p.core.p4.py, p.core.p4.pz, sqrt(p.core.p4.px * p.core.p4.px + p.core.p4.py * p.core.p4.py + p.core.p4.pz * p.core.p4.pz + p.core.p4.mass * p.core.p4.mass));
        result.push_back(fourvec.Theta());
    }
    return result;
}

ROOT::VecOps::RVec<float> getMC_eta (ROOT::VecOps::RVec<fcc::MCParticleData> in){
    ROOT::VecOps::RVec<float> result;
    for (auto & p: in){
        TLorentzVector fourvec;
        fourvec.SetPxPyPzE(p.core.p4.px, p.core.p4.py, p.core.p4.pz, sqrt(p.core.p4.px * p.core.p4.px + p.core.p4.py * p.core.p4.py + p.core.p4.pz * p.core.p4.pz + p.core.p4.mass * p.core.p4.mass));
        result.push_back(fourvec.Eta());
    }
    return result;
}

ROOT::VecOps::RVec<float> getMC_energy (ROOT::VecOps::RVec<fcc::MCParticleData> in){
    ROOT::VecOps::RVec<float> result;
    for (auto & p: in){
        TLorentzVector fourvec;
        fourvec.SetPxPyPzE(p.core.p4.px, p.core.p4.py, p.core.p4.pz, sqrt(p.core.p4.px * p.core.p4.px + p.core.p4.py * p.core.p4.py + p.core.p4.pz * p.core.p4.pz + p.core.p4.mass * p.core.p4.mass));
        result.push_back(fourvec.E());
    }
    return result;
}

ROOT::VecOps::RVec<TLorentzVector> getMC_lorentzVector (ROOT::VecOps::RVec<fcc::MCParticleData> in){
    ROOT::VecOps::RVec<TLorentzVector> result;
    for (auto & p: in){
        TLorentzVector fourvec;
        fourvec.SetPxPyPzE(p.core.p4.px, p.core.p4.py, p.core.p4.pz, sqrt(p.core.p4.px * p.core.p4.px + p.core.p4.py * p.core.p4.py + p.core.p4.pz * p.core.p4.pz + p.core.p4.mass * p.core.p4.mass));
        result.push_back(fourvec);
    }
    return result;
}

ROOT::VecOps::RVec<int> getMC_pid (ROOT::VecOps::RVec<fcc::MCParticleData> in){
    ROOT::VecOps::RVec<int> result;
    for (auto & p: in){
        result.push_back(p.core.pdgId);
    }
    return result;
}

ROOT::VecOps::RVec<int> getMC_status (ROOT::VecOps::RVec<fcc::MCParticleData> in){
    ROOT::VecOps::RVec<int> result;
    for (auto & p: in){
        result.push_back(p.core.status);
    }
    return result;
}
