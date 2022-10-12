#include "FCCAnalyses/CaloNtupleizer.h"
#include "TVector3.h"
#include "TLorentzVector.h"
#include "edm4hep/MCParticleData.h"

#include <math.h>

#include "DD4hep/Detector.h"

namespace FCCAnalyses{

namespace CaloNtupleizer{

dd4hep::DDSegmentation::BitFieldCoder* m_decoder;

void loadGeometry(std::string xmlGeometryPath, std::string readoutName){
  dd4hep::Detector* dd4hepgeo = &(dd4hep::Detector::getInstance());
  dd4hepgeo->fromCompact(xmlGeometryPath);
  dd4hepgeo->volumeManager();
  dd4hepgeo->apply("DD4hepVolumeManager", 0, 0);
  m_decoder = dd4hepgeo->readout(readoutName).idSpec().decoder();
}


// calo hit
ROOT::VecOps::RVec<float> getCaloHit_x (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.x);
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloHit_y (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloHit_z (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.z);
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloHit_r (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(sqrt(p.position.x * p.position.x + p.position.y * p.position.y));
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloHit_phi (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Phi());
  }
  return result;
}

ROOT::VecOps::RVec<int> getCaloHit_phiBin (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in){
  ROOT::VecOps::RVec<int> result;
  for (auto & p: in){
    dd4hep::DDSegmentation::CellID cellId = p.cellID;
    result.push_back(m_decoder->get(cellId, "phi"));
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloHit_theta (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Theta());
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloHit_eta (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Eta());
  }
  return result;
}

ROOT::VecOps::RVec<int> getCaloHit_etaBin (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in){
  ROOT::VecOps::RVec<int> result;
  for (auto & p: in){
    dd4hep::DDSegmentation::CellID cellId = p.cellID;
    result.push_back(m_decoder->get(cellId, "eta"));
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloHit_energy (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.energy);
  }
  return result;
}

ROOT::VecOps::RVec<int> getCaloHit_layer (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in){
  ROOT::VecOps::RVec<int> result;
  for (auto & p: in){
    dd4hep::DDSegmentation::CellID cellId = p.cellID;
    result.push_back(m_decoder->get(cellId, "layer"));
  }
  return result;
}

ROOT::VecOps::RVec<TVector3> getCaloHit_positionVector3 (const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& in){
  ROOT::VecOps::RVec<TVector3> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3);
  }
  return result;
}

// calo cluster
ROOT::VecOps::RVec<float> getCaloCluster_x (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.x);
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloCluster_y (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.y);
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloCluster_z (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.position.z);
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloCluster_phi (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Phi());
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloCluster_theta (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Theta());
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloCluster_eta (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3.Eta());
  }
  return result;
}

ROOT::VecOps::RVec<float> getCaloCluster_energy (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.energy);
  }
  return result;
}

ROOT::VecOps::RVec<TVector3> getCaloCluster_positionVector3 (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in){
  ROOT::VecOps::RVec<TVector3> result;
  for (auto & p: in){
    TVector3 t3;
    t3.SetXYZ(p.position.x, p.position.y, p.position.z);
    result.push_back(t3);
  }
  return result;
}

ROOT::VecOps::RVec<int> getCaloCluster_firstCell (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in){
  ROOT::VecOps::RVec<int> result;
  for (auto & p: in){
    result.push_back(p.hits_begin);
  }
  return result;
}

ROOT::VecOps::RVec<int> getCaloCluster_lastCell (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in){
  ROOT::VecOps::RVec<int> result;
  for (auto & p: in){
    result.push_back(p.hits_end);
  }
  return result;
}

ROOT::VecOps::RVec<std::vector<float>>
getCaloCluster_energyInLayers (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in,
                               const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& cells,
                               const int nLayers) {
  static const int layer_idx = m_decoder->index("layer");
  static const int cryo_idx = m_decoder->index("cryo");
  ROOT::VecOps::RVec<std::vector<float>> result;
  result.reserve(in.size());

  for (const auto & c: in) {
    std::vector<float> energies(nLayers, 0);
    for (auto i = c.hits_begin; i < c.hits_end; i++) {
      int layer = m_decoder->get(cells[i].cellID, layer_idx);
      int cryoID = m_decoder->get(cells[i].cellID, cryo_idx);
      if(cryoID == 0) {
        energies[layer] += cells[i].energy;
      }
    }
    result.push_back(energies);
  }
  return result;
}

// High level cluster variables
// max cell energy in a given layer
ROOT::VecOps::RVec<float> getCaloCluster_maxEnergyInLayer (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in, const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& cells, const int layer) {
  ROOT::VecOps::RVec<float> result;
  static const int layer_idx = m_decoder->index("layer");
  for (auto & c: in) {
    float max_energy = -1;
    for (auto i = c.hits_begin; i < c.hits_end; i++) {
      int cell_layer = m_decoder->get(cells[i].cellID, layer_idx);
      float cell_energy = cells[i].energy;
      if(cell_layer == layer && cell_energy > max_energy){
          max_energy = cell_energy;
      }
    }
    result.push_back(max_energy);
  }
  return result;
}

// next to max cell energy in a given layer, separated from the cell with max energy by at least one cell
ROOT::VecOps::RVec<float> getCaloCluster_secondMaxEnergyInLayer (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in, const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& cells, const int layer) {
  ROOT::VecOps::RVec<float> result;
  static const int layer_idx = m_decoder->index("layer");
  for (auto & c: in) {
    float max_energy = -1;
    int max_energy_cell_phi_bin = -1;
    int max_energy_cell_eta_bin = -1;
    int max_phi_index_for_modulo = 2; // should be improved but without hardcoding the max number of bins
    int max_eta_index_for_modulo = 2; // should be improved but without hardcoding the max number of bins
    for (auto i = c.hits_begin; i < c.hits_end; i++) {
      int cell_layer = m_decoder->get(cells[i].cellID, layer_idx);
      float cell_energy = cells[i].energy;
      if(cell_layer == layer){
        int cell_phi_bin = m_decoder->get(cells[i].cellID, "phi");
        int cell_eta_bin = m_decoder->get(cells[i].cellID, "eta");
        if(cell_phi_bin > max_phi_index_for_modulo){
            max_phi_index_for_modulo = cell_phi_bin;
        }
        if(cell_eta_bin > max_eta_index_for_modulo){
            max_eta_index_for_modulo = cell_eta_bin;
        }
        if (cell_energy > max_energy){
          max_energy = cell_energy;
          max_energy_cell_phi_bin = m_decoder->get(cells[i].cellID, "phi");
          max_energy_cell_eta_bin = m_decoder->get(cells[i].cellID, "eta");
        }
      }
    }
    float next_to_max_energy = -1;
    int next_to_max_energy_cell_phi_bin = -1;
    int next_to_max_energy_cell_eta_bin = -1;
    for (auto i = c.hits_begin; i < c.hits_end; i++) {
      float cell_energy = cells[i].energy;
      next_to_max_energy_cell_phi_bin = m_decoder->get(cells[i].cellID, "phi");
      next_to_max_energy_cell_eta_bin = m_decoder->get(cells[i].cellID, "eta");
      float dist_with_max_energy = sqrt(((max_energy_cell_phi_bin - next_to_max_energy_cell_phi_bin) % (max_phi_index_for_modulo - 1)) * ((max_energy_cell_phi_bin - next_to_max_energy_cell_phi_bin) % (max_phi_index_for_modulo - 1)) + ((max_energy_cell_eta_bin - next_to_max_energy_cell_eta_bin) % (max_eta_index_for_modulo - 1)) * ((max_energy_cell_eta_bin - next_to_max_energy_cell_eta_bin) % (max_eta_index_for_modulo - 1)));
      if(cell_energy < max_energy && cell_energy > next_to_max_energy && dist_with_max_energy > 1.0){
          next_to_max_energy = cells[i].energy;
      }
    }
    result.push_back(max_energy);
  }
  return result;
}

// total energy in a layer divided by cluster energy (sensitive to the longitudinal shower development useful for e.g. high energy pi0/gamma separation where transverse shape become similar)
ROOT::VecOps::RVec<float> getCaloCluster_energyInLayerOverClusterEnergy (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in, const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& cells, const int layer) {
  static const int layer_idx = m_decoder->index("layer");
  ROOT::VecOps::RVec<float> result;
  for (const auto & c: in) {
    float cluster_energy = c.energy;
    float energy_in_layer = 0;
    for (auto i = c.hits_begin; i < c.hits_end; i++) {
      int cell_layer = m_decoder->get(cells[i].cellID, layer_idx);
      if(cell_layer == layer){
          energy_in_layer += cells[i].energy;
      }
    }
    result.push_back(energy_in_layer/cluster_energy);
  }
  return result;
}

// distance between the max and second max energy cells whithin a layer, given in units of cell size
ROOT::VecOps::RVec<float> getCaloCluster_distBetweenMaximaInLayer (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in, const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& cells, const int layer) {
  static const int layer_idx = m_decoder->index("layer");
  ROOT::VecOps::RVec<float> result;
  for (const auto & c: in) {
    float max_energy = 0;
    float next_to_max_energy = 0;
    int max_energy_cell_phi_bin = -1;
    int max_energy_cell_eta_bin = -1;
    int next_to_max_energy_cell_phi_bin = -1;
    int next_to_max_energy_cell_eta_bin = -1;
    int max_phi_index_for_modulo = 2; // should be improved but without hardcoding the max number of bins
    int max_eta_index_for_modulo = 2; // should be improved but without hardcoding the max number of bins
    for (auto i = c.hits_begin; i < c.hits_end; i++) {
      int cell_layer = m_decoder->get(cells[i].cellID, layer_idx);
      if(cell_layer == layer){
          float cell_energy = cells[i].energy;
          int cell_phi_bin = m_decoder->get(cells[i].cellID, "phi");
          int cell_eta_bin = m_decoder->get(cells[i].cellID, "eta");
          if(cell_energy > max_energy){
              max_energy = cell_energy;
              max_energy_cell_phi_bin = cell_phi_bin;
              max_energy_cell_eta_bin = cell_eta_bin;
          }
          else if(cell_energy > next_to_max_energy){
              next_to_max_energy = cell_energy;
              next_to_max_energy_cell_phi_bin = cell_phi_bin;
              next_to_max_energy_cell_eta_bin = cell_eta_bin;
          }
          if(cell_phi_bin > max_phi_index_for_modulo){
              max_phi_index_for_modulo = cell_phi_bin;
          }
          if(cell_eta_bin > max_eta_index_for_modulo){
              max_eta_index_for_modulo = cell_eta_bin;
          }
      }
    }
    float distance = 0;
    if (next_to_max_energy_cell_phi_bin != -1){ // protect from clusters with one cell
        distance = sqrt(((max_energy_cell_phi_bin - next_to_max_energy_cell_phi_bin) % (max_phi_index_for_modulo - 1))  * ((max_energy_cell_phi_bin - next_to_max_energy_cell_phi_bin) % (max_phi_index_for_modulo - 1)) + ((max_energy_cell_eta_bin - next_to_max_energy_cell_eta_bin) % (max_energy_cell_eta_bin -1)) * ((max_energy_cell_eta_bin - next_to_max_energy_cell_eta_bin) % (max_energy_cell_eta_bin -1)));
    }
    result.push_back(distance);
  }
  return result;
}

// Core energy
//ROOT::VecOps::RVec<float> getCaloCluster_coreEnergyInLayer (const ROOT::VecOps::RVec<edm4hep::ClusterData>& in, const ROOT::VecOps::RVec<edm4hep::CalorimeterHitData>& cells, const int layer) {
//  static const int layer_idx = m_decoder->index("layer");
//  ROOT::VecOps::RVec<float> result;
//  for (const auto & c: in) {
//    float max_energy = 0;
//    size_t max_energy_cell_idx = -1;
//    for (auto i = c.hits_begin; i < c.hits_end; i++) {
//      int cell_layer = m_decoder->get(cells[i].cellID, layer_idx);
//      if(cell_layer == layer){
//          float cell_energy = cells[i].energy;
//          if(cell_energy > max_energy){
//              max_energy = cell_energy;
//              max_energy_cell_idx = i;
//          }
//
//}



// SimSecondaries particles
ROOT::VecOps::RVec<float> getSimParticleSecondaries_x (const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in){
    result.push_back(p.vertex.x);
  }
  return result;
}


ROOT::VecOps::RVec<float> getSimParticleSecondaries_y (const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in){
  ROOT::VecOps::RVec<float> result;
for (auto & p: in) {
  result.push_back(p.vertex.y);
}
return result;
}


ROOT::VecOps::RVec<float> getSimParticleSecondaries_z (const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in){
  ROOT::VecOps::RVec<float> result;
for (auto & p: in) {
  result.push_back(p.vertex.z);
}
return result;
}


  ROOT::VecOps::RVec<float> getSimParticleSecondaries_PDG (const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in){
    ROOT::VecOps::RVec<float> result;
    for (auto & p: in) {
      result.push_back(p.PDG);
    }
    return result;
  }

ROOT::VecOps::RVec<float> getSimParticleSecondaries_phi (const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Phi());
  }
  return result;
}


ROOT::VecOps::RVec<float> getSimParticleSecondaries_theta (const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Theta());
  }
  return result;
}

ROOT::VecOps::RVec<float> getSimParticleSecondaries_eta (const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.Eta());
  }
  return result;
}

ROOT::VecOps::RVec<float> getSimParticleSecondaries_energy (const ROOT::VecOps::RVec<edm4hep::MCParticleData>& in){
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    result.push_back(tlv.E());
  }
  return result;
}

getFloatAt::getFloatAt(size_t pos) {m_pos = pos;}
ROOT::RVecF getFloatAt::operator()(const ROOT::VecOps::RVec<std::vector<float>>& in) {
  ROOT::RVecF result;
  for (auto & v : in) {
    result.push_back(v[m_pos]);
  }
  return result;
}

}//end NS CaloNtupleizer

}//end NS FCCAnalyses
