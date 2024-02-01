"""
31 January 2024
Abraham Tishelman-Charny

The purpose of this python module is to store text definitions of ROOT functions to be used in FCCAnalyses stage 1 steering scripts.
"""


CustomDefinitions = """
ROOT::VecOps::RVec<double> SumFlavorScores(ROOT::VecOps::RVec<double> recojet_isFlavor) {

    double score_1, score_2, pair_score; 
    ROOT::VecOps::RVec<double> recojetpair_isFlavor;

    // cannot compute any mass pair flavour score values, return a single non-physical value
    if(recojet_isFlavor.size() < 2){
        recojetpair_isFlavor.push_back(-99);
        return recojetpair_isFlavor; 
    }


    // For each jet, take its flavor score sum with the remaining jets. Stop at last jet.
    for(int i = 0; i < recojet_isFlavor.size()-1; ++i) {

    score_1 = recojet_isFlavor.at(i); 

        for(int j=i+1; j < recojet_isFlavor.size(); ++j){ // go until end
            score_2 = recojet_isFlavor.at(j);
            pair_score = score_1 + score_2; 
            recojetpair_isFlavor.push_back(pair_score);

        }
    }

    return recojetpair_isFlavor;
}



ROOT::VecOps::RVec<double> all_recoil_masses(ROOT::VecOps::RVec<TLorentzVector> all_jet_4vectors){
  double m_sqrts = 240;
  auto recoil_p4 = TLorentzVector(0, 0, 0, m_sqrts);
  TLorentzVector tv1, tv2, tvpair; 
  double E, px, py, pz, recoil_mass;
  ROOT::VecOps::RVec<double> recoil_masses;

  // cannot compute any mass pair values, return a single non-physical value
  if(all_jet_4vectors.size() < 2){
    recoil_masses.push_back(-99);
    return recoil_masses;  
  }

    // For each jet, take its recoil mass using the remaining jets. Stop at last jet.
    for(int i = 0; i < all_jet_4vectors.size()-1; ++i) {

        tv1 = all_jet_4vectors.at(i);

        for(int j=i+1; j < all_jet_4vectors.size(); ++j){ // go until end

            tv2 = all_jet_4vectors.at(j); 
            E = tv1.E() + tv2.E();
            px = tv1.Px() + tv2.Px();
            py = tv1.Py() + tv2.Py();
            pz = tv1.Pz() + tv2.Pz();

            tvpair.SetPxPyPzE(px, py, pz, E);

            recoil_p4 = TLorentzVector(0, 0, 0, m_sqrts);
            recoil_p4 -= tvpair; 

            recoil_mass = recoil_p4.M();
            recoil_masses.push_back(recoil_mass);

        }
    }

  return recoil_masses;

}

"""
