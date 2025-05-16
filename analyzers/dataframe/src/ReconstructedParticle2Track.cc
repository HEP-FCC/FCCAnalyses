#include "FCCAnalyses/ReconstructedParticle2Track.h"
#include "FCCAnalyses/VertexingUtils.h"

namespace FCCAnalyses{

namespace ReconstructedParticle2Track{

  ROOT::VecOps::RVec<float> 
  getRP2TRK_mom(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
                ROOT::VecOps::RVec<edm4hep::TrackState> tracks) {
    ROOT::VecOps::RVec<float> result;
    for (auto & p: in) {
      if (p.tracks_begin<tracks.size())
        result.push_back(VertexingUtils::get_trackMom(tracks.at(p.tracks_begin)));
      else result.push_back(std::nan(""));
    }
    return result;
  }

  ROOT::VecOps::RVec<float> 
  getRP2TRK_charge(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
                   ROOT::VecOps::RVec<edm4hep::TrackState> tracks) {
    ROOT::VecOps::RVec<float> result;
    for (auto & p: in) {
      if (p.tracks_begin<tracks.size())
        result.push_back(p.charge);
      else result.push_back(std::nan(""));
    }
    return result;
  }

  ROOT::VecOps::RVec<float> getRP2TRK_Bz(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& rps, const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
    const double c_light = 2.99792458e8;
    const double a = c_light * 1e3 * 1e-15; //[omega] = 1/mm
    ROOT::VecOps::RVec<float> out;

    for(auto & p: rps) {
      if(p.tracks_begin < tracks.size()) {
	double pt= sqrt(p.momentum.x * p.momentum.x + p.momentum.y * p.momentum.y);
	double Bz= tracks.at(p.tracks_begin).omega / a * pt * std::copysign(1.0, p.charge);
	out.push_back(Bz);
      } else {
	out.push_back(-9.);
      }
    }
    return out;
  }

  float Bz(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& rps, const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks) {
    const double c_light =  2.99792458e8;// speed of light m/sec;
    const double a = c_light * 1e3 * 1e-15; //[omega] = 1/mm

    double Bz = -9;

    for(auto & p: rps) {
      if(p.tracks_begin < tracks.size()) {
        double pt= sqrt(p.momentum.x * p.momentum.x + p.momentum.y * p.momentum.y);
        Bz= tracks.at(p.tracks_begin).omega / a * pt * std::copysign(1.0, p.charge);
      }
    }
    return Bz;
  }


  ROOT::VecOps::RVec<float> XPtoPar_dxy(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in,
					const ROOT::VecOps::RVec<edm4hep::TrackState>& trackstates,
          const ROOT::VecOps::RVec<edm4hep::TrackData>& tracks,
					const TLorentzVector& V, // primary vertex
					const float& Bz) {

    const double cSpeed = 2.99792458e8 * 1.0e-9;

    ROOT::VecOps::RVec<float> out;

    for (const auto & rp: in) {

      auto track = tracks.at(rp.tracks_begin);

      if(track.tracks_begin - track.tracks_end >0) { // if any tracks

        float D0_wrt0 = trackstates.at(track.trackStates_begin).D0;
        float Z0_wrt0 = trackstates.at(track.trackStates_begin).Z0;
        float phi0_wrt0 = trackstates.at(track.trackStates_begin).phi;

        TVector3 X( - D0_wrt0 * TMath::Sin(phi0_wrt0) , D0_wrt0 * TMath::Cos(phi0_wrt0) , Z0_wrt0);
        TVector3 x = X - V.Vect();
        //std::cout<<"vertex: "<<V.Vect().X()<<", "<<V.Vect().Y()<<", "<<V.Vect().Z()<<", "<<std::endl;
        TVector3 p(rp.momentum.x, rp.momentum.y, rp.momentum.z);

        double a = - rp.charge * Bz * cSpeed;
        double pt = p.Pt();
        double r2 = x(0) * x(0) + x(1) * x(1);
        double cross = x(0) * p(1) - x(1) * p(0);
        double D=-9;
        if (pt * pt - 2 * a * cross + a * a * r2 > 0) {
          double T = TMath::Sqrt(pt * pt - 2 * a * cross + a * a * r2);
      	  if (pt < 10.0) D = (T - pt) / a;
                else D = (-2 * cross + a * r2) / (T + pt);
        }
        //std::cout<<"displ: "<<D<<std::endl;
	      out.push_back(D);

      } else {
	out.push_back(-9.);
      }
    }
    return out;
  }


  ROOT::VecOps::RVec<float> XPtoPar_dz(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in,
                                        const ROOT::VecOps::RVec<edm4hep::TrackState>& trackstates,
                                        const ROOT::VecOps::RVec<edm4hep::TrackData>& tracks,
                                        const TLorentzVector& V, // primary vertex
                                        const float& Bz) {

    const double cSpeed = 2.99792458e8 * 1.0e-9; //Reduced speed of light ???

    ROOT::VecOps::RVec<float> out;

    for (const auto & rp: in) {

      auto track = tracks.at(rp.tracks_begin);

      if(track.tracks_begin - track.tracks_end >0) { // if any tracks

        float D0_wrt0 = trackstates.at(track.trackStates_begin).D0;
        float Z0_wrt0 = trackstates.at(track.trackStates_begin).Z0;
        float phi0_wrt0 = trackstates.at(track.trackStates_begin).phi;

        TVector3 X( - D0_wrt0 * TMath::Sin(phi0_wrt0) , D0_wrt0 * TMath::Cos(phi0_wrt0) , Z0_wrt0);
        TVector3 x = X - V.Vect();

        TVector3 p(rp.momentum.x, rp.momentum.y, rp.momentum.z);

        double a = - rp.charge * Bz * cSpeed;
        double pt = p.Pt();
        double C = a/(2 * pt);
        double r2 = x(0) * x(0) + x(1) * x(1);
        double cross = x(0) * p(1) - x(1) * p(0);
        double T = TMath::Sqrt(pt * pt - 2 * a * cross + a * a * r2);
        double D;
        if (pt < 10.0) D = (T - pt) / a;
        else D = (-2 * cross + a * r2) / (T + pt);
        double B = C * TMath::Sqrt(TMath::Max(r2 - D * D, 0.0) / (1 + 2 * C * D));
        if ( TMath::Abs(B) > 1.) B = TMath::Sign(1, B);
        double st = TMath::ASin(B) / C;
        double ct = p(2) / pt;
        double z0;
        double dot = x(0) * p(0) + x(1) * p(1);
        if (dot > 0.0) z0 = x(2) - ct * st;
        else z0 = x(2) + ct * st;

        out.push_back(z0);
      } else {
        out.push_back(-9.);
      }
    }
    return out;
  }

  ROOT::VecOps::RVec<float> XPtoPar_phi(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in,
					const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks,
					const TLorentzVector& V, // primary vertex
					const float& Bz) {

    const double cSpeed = 2.99792458e8 * 1.0e-9; //Reduced speed of light ???

    ROOT::VecOps::RVec<float> out;

    for (const auto & rp: in) {

      if( rp.tracks_begin < tracks.size()) {

        float D0_wrt0 = tracks.at(rp.tracks_begin).D0;
        float Z0_wrt0 = tracks.at(rp.tracks_begin).Z0;
        float phi0_wrt0 = tracks.at(rp.tracks_begin).phi;

        TVector3 X( - D0_wrt0 * TMath::Sin(phi0_wrt0) , D0_wrt0 * TMath::Cos(phi0_wrt0) , Z0_wrt0);
        TVector3 x = X - V.Vect();

        TVector3 p(rp.momentum.x, rp.momentum.y, rp.momentum.z);

        double a = - rp.charge * Bz * cSpeed;
        double pt = p.Pt();
        double r2 = x(0) * x(0) + x(1) * x(1);
        double cross = x(0) * p(1) - x(1) * p(0);
        double T = TMath::Sqrt(pt * pt - 2 * a * cross + a * a * r2);
        double phi0 = TMath::ATan2((p(1) - a * x(0)) / T, (p(0) + a * x(1)) / T);

	out.push_back(phi0);

      } else {
        out.push_back(-9.);
      }
    }
    return out;
  }

  ROOT::VecOps::RVec<float> XPtoPar_C(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in,
				       const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks,
				       const float& Bz) {

    const double cSpeed = 2.99792458e8 * 1.0e3 * 1.0e-15;
    ROOT::VecOps::RVec<float> out;

    for (const auto & rp: in) {

      if( rp.tracks_begin < tracks.size()) {

        TVector3 p(rp.momentum.x, rp.momentum.y, rp.momentum.z);

        double a = std::copysign(1.0, rp.charge) * Bz * cSpeed;
	double pt = p.Pt();
        double C = a/(2 * pt);

	out.push_back(C);
      } else {
        out.push_back(-9.);
      }
    }
    return out;
  }

  ROOT::VecOps::RVec<float> XPtoPar_ct(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>& in,
				       const ROOT::VecOps::RVec<edm4hep::TrackState>& tracks,
				       const float& Bz) {

    const double cSpeed = 2.99792458e8 * 1.0e-9;
    ROOT::VecOps::RVec<float> out;

    for (const auto & rp: in) {

      if( rp.tracks_begin < tracks.size()) {

        TVector3 p(rp.momentum.x, rp.momentum.y, rp.momentum.z);
	double pt = p.Pt();

        double ct = p(2) / pt;

	out.push_back(ct);

      } else {
        out.push_back(-9.);
      }
    }
    return out;
  }


ROOT::VecOps::RVec<float>
getRP2TRK_D0(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
             ROOT::VecOps::RVec<edm4hep::TrackState> tracks) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    if (p.tracks_begin<tracks.size())
      result.push_back(tracks.at(p.tracks_begin).D0);
    else result.push_back(-9.);
  }
  return result;
}


// cov_index accesses the different elements of the covariance matrix. 
// diagonal elements are: 0: d0d0, 2: phiphi, 5: omegaomega, 9: z0z0, 14: tanLambdatanLambda
// off-diagonal elements are: 1: phid0, 3: d0omega, 4: phiomega, 6: d0z0, 7: phiz0, 8: omegaz0, 10: d0tanLambda, 11: phitanLambda, 12: omegatanLambda, 13: tanLambdaz0
ROOT::VecOps::RVec<float>
get_cov(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
					      ROOT::VecOps::RVec<edm4hep::TrackData> tracks,
                ROOT::VecOps::RVec<edm4hep::TrackState> trackstates,
                int cov_index) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    if (p.tracks_begin - p.tracks_end > 0) { // if any tracks
      auto track = tracks.at(p.tracks_begin);
      result.push_back(trackstates.at(track.trackStates_begin).covMatrix[cov_index]);
    } else {
      result.push_back(-9.);
    }
  }
  return result;
}

ROOT::VecOps::RVec<float>
getRP2TRK_D0_sig(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
					      ROOT::VecOps::RVec<edm4hep::TrackState> tracks) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    if (p.tracks_begin<tracks.size())
      result.push_back(tracks.at(p.tracks_begin).D0/sqrt(tracks.at(p.tracks_begin).covMatrix[0]));
    else result.push_back(-9.);
  }
  return result;
}

ROOT::VecOps::RVec<float>
getRP2TRK_Z0(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
					  ROOT::VecOps::RVec<edm4hep::TrackState> tracks) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    if (p.tracks_begin<tracks.size())
      result.push_back(tracks.at(p.tracks_begin).Z0);
    else result.push_back(-9.);
  }
  return result;
}

ROOT::VecOps::RVec<float>
getRP2TRK_Z0_sig(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
					      ROOT::VecOps::RVec<edm4hep::TrackState> tracks) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    if (p.tracks_begin<tracks.size())
      result.push_back(tracks.at(p.tracks_begin).Z0/sqrt(tracks.at(p.tracks_begin).covMatrix[9]));
    else result.push_back(std::nan(""));
  }
  return result;
}

ROOT::VecOps::RVec<float>
getRP2TRK_phi(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
					   ROOT::VecOps::RVec<edm4hep::TrackState> tracks) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    if (p.tracks_begin<tracks.size())
      result.push_back(tracks.at(p.tracks_begin).phi);
    else result.push_back(-9);
  }
  return result;
}


ROOT::VecOps::RVec<float>
getRP2TRK_omega(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
					     ROOT::VecOps::RVec<edm4hep::TrackState> tracks) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    if (p.tracks_begin<tracks.size())
      result.push_back(tracks.at(p.tracks_begin).omega);
    else result.push_back(-9);
  }
  return result;
}


ROOT::VecOps::RVec<float>
getRP2TRK_tanLambda(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
						 ROOT::VecOps::RVec<edm4hep::TrackState> tracks) {
  ROOT::VecOps::RVec<float> result;
  for (auto & p: in) {
    if (p.tracks_begin<tracks.size())
      result.push_back(tracks.at(p.tracks_begin).tanLambda);
    else result.push_back(-9);
  }
  return result;
}


ROOT::VecOps::RVec<edm4hep::TrackState>
getRP2TRK( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in,
					ROOT::VecOps::RVec<edm4hep::TrackState> tracks )
{

  ROOT::VecOps::RVec<edm4hep::TrackState> result ;
  result.reserve( in.size() );

  for (auto & p: in) {
    if (p.tracks_begin >= 0 && p.tracks_begin<tracks.size()) {
	result.push_back(tracks.at(p.tracks_begin) ) ;
    }
  }
 return result ;
}

// returns reco indices of tracks
ROOT::VecOps::RVec<int> 
get_recoindTRK( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, 
		ROOT::VecOps::RVec<edm4hep::TrackState> tracks )
{

  ROOT::VecOps::RVec<int> result ;
  
  for (unsigned int ctr=0; ctr<in.size(); ctr++) {
    edm4hep::ReconstructedParticleData p = in.at(ctr);
    if (p.tracks_begin >= 0 && p.tracks_begin<tracks.size()) result.push_back(ctr) ;
  }
 return result ;
}

int getTK_n(ROOT::VecOps::RVec<edm4hep::TrackState> x) {
  int result =  x.size();
  return result;
}

///
ROOT::VecOps::RVec<bool> 
hasTRK( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in ) {

  ROOT::VecOps::RVec<bool> result ;
  result.reserve( in.size() );
  
  for (auto & p: in) {
    if (p.tracks_begin >= 0 && p.tracks_begin != p.tracks_end) result.push_back(true) ;
    else result.push_back(false);
  }
 return result ;
}

}//end NS ReconstructedParticle2Track

}//end NS FCCAnalyses
