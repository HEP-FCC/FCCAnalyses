namespace FCCAnalyses {
Vec_tlv energyReconstructFourJet(Vec_f px, Vec_f py, Vec_f pz, Vec_f e) {
    
    
    //cout << "***************" << std::endl;
    
    //cout << px.size() << std::endl;
    
    float p0 = std::sqrt(px[0]*px[0] + py[0]*py[0] + pz[0]*pz[0]);
    float p1 = std::sqrt(px[1]*px[1] + py[1]*py[1] + pz[1]*pz[1]);
    float p2 = std::sqrt(px[2]*px[2] + py[2]*py[2] + pz[2]*pz[2]);
    float p3 = std::sqrt(px[3]*px[3] + py[3]*py[3] + pz[3]*pz[3]);

    TMatrixD mtrx(4, 4);
    mtrx(0, 0) = 1;
    mtrx(0, 1) = 1;
    mtrx(0, 2) = 1;
    mtrx(0, 3) = 1;

    mtrx(1, 0) = px[0]/e[0];
    mtrx(1, 1) = px[1]/e[1];
    mtrx(1, 2) = px[2]/e[2];
    mtrx(1, 3) = px[3]/e[3];
    
    mtrx(2, 0) = py[0]/e[0];
    mtrx(2, 1) = py[1]/e[1];
    mtrx(2, 2) = py[2]/e[2];
    mtrx(2, 3) = py[3]/e[3];
    
    mtrx(3, 0) = pz[0]/e[0];
    mtrx(3, 1) = pz[1]/e[1];
    mtrx(3, 2) = pz[2]/e[2];
    mtrx(3, 3) = pz[3]/e[3];
    
    TMatrixD inv = mtrx.Invert();
    
    
    TVectorD vec(4);
    vec(0) = 240;
    vec(1) = 0;
    vec(2) = 0;
    vec(3) = 0;
    
    TVectorD res = inv*vec;
    
    bool isValid = true;
    
    if(res[0]<0 or res[1]<0 or res[2]<0 or res[3]<0 or res[0]>240 or res[1]>240 or res[2]>240 or res[3]>240) {
        isValid = false;
    }
    
    Vec_tlv ret;
    float chi2 = 0;
    for(int i=0; i<4; i++) {
        TLorentzVector tlv;
        if(isValid)
            tlv.SetPxPyPzE(px[i]*res[i]/e[i], py[i]*res[i]/e[i], pz[i]*res[i]/e[i], res[i]);
        else
            tlv.SetPxPyPzE(px[i], py[i], pz[i], e[i]);
        ret.push_back(tlv);
        
        if(res[i] > 0) {
            float uncert = 0.5*std::sqrt(e[i]) + 0.05*e[i];
            float delta = (e[i]-res[i])/uncert;
            chi2 += delta*delta;
        }
        else {
            chi2 += 1000.;
        }
    }
    
    // add chi2 as dummy to the list of Lorentz vectors
    TLorentzVector chi2_;
    chi2_.SetPxPyPzE(0, 0, 0, chi2);
    ret.push_back(chi2_);
    
    
    return ret;
}
}
