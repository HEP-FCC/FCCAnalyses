#include "FCCAnalyses/SmearObjects.h"

#include "FCCAnalyses/VertexFitterSimple.h"
#include "FCCAnalyses/VertexingUtils.h"

#include "TDecompChol.h"

#include <iostream>

namespace FCCAnalyses
{

  namespace SmearObjects
  {

    // -------------------------------------------------------------------------------------------

    TVectorD TrackParamFromMC_DelphesConv(edm4hep::MCParticleData aMCParticle)
    {

      TVector3 p(aMCParticle.momentum.x, aMCParticle.momentum.y, aMCParticle.momentum.z);
      TVector3 x(1e-3 * aMCParticle.vertex.x, 1e-3 * aMCParticle.vertex.y, 1e-3 * aMCParticle.vertex.z); // mm to m
      float Q = aMCParticle.charge;
      TVectorD param = VertexFitterSimple::XPtoPar(x, p, Q); // convention Franco

      return param;
    }

    // -------------------------------------------------------------------------------------------

    SmearedTracks::SmearedTracks(float smear_d0, float smear_phi, float smear_omega, float smear_z0, float smear_tlambda, bool debug = false)
    {

      m_smear_parameters[0] = smear_d0;
      m_smear_parameters[1] = smear_phi;
      m_smear_parameters[2] = smear_omega;
      m_smear_parameters[3] = smear_z0;
      m_smear_parameters[4] = smear_tlambda;

      m_debug = debug;
    }

    ROOT::VecOps::RVec<edm4hep::TrackState> SmearedTracks::operator()(
        const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> &allRecoParticles,
        const ROOT::VecOps::RVec<edm4hep::TrackState> &alltracks,
        const ROOT::VecOps::RVec<int> &RP2MC_indices,
        const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mcParticles)
    {

      // returns a vector of TrackStates that is parallel to the collection of full tracks (alltracks),
      // i.e. same number of entries, same order.
      // The method retrieve the MC particle that is associated to a track, and builds a "track state"
      // out of the MC particle (i.e. it determines the corresponding (d0, phi, omega, z0, tanlambda).
      // From this vector, and from the covariance matrix of the track, which is scaled by the user,
      // new track states are generated.

      int ntracks = alltracks.size();

      ROOT::VecOps::RVec<edm4hep::TrackState> result;
      result.resize(ntracks);

      edm4hep::TrackState dummy;

      TVectorD zero(5);
      for (int k=0; k<5; k++) { zero(k) = 0. ; }

      for (int itrack = 0; itrack < ntracks; itrack++)
      {
        edm4hep::TrackState track = alltracks[itrack];
        edm4hep::TrackState smeared_track = track;

        // find the corresponding MC particle
        int MCindex = -1;
        for (int ireco = 0; ireco < allRecoParticles.size(); ireco++)
        {
          edm4hep::ReconstructedParticleData rp = allRecoParticles[ireco];
          int track_index = rp.tracks_begin;
          if (track_index == itrack)
          {
            MCindex = RP2MC_indices[ireco];
            break;
          }
        } // end loop on RPs

        if (MCindex < 0 || MCindex >= mcParticles.size())
        { // in principle, this should not happen in delphes,
          // each track should be matched to a MC particle.
          result[itrack] = dummy;
          continue;
        }

        edm4hep::MCParticleData MCpart = mcParticles[MCindex];

        // the MC-truth track parameters, in Delphes's comvention
        TVectorD mcTrackParam = TrackParamFromMC_DelphesConv(MCpart);

        // the covariance matrix of the track, in Delphes's convention
        TMatrixDSym Cov = VertexingUtils::get_trackCov(track);

        // if the covMat of the track is pathological (numerical precision issue, fraction of tracks = 5e-6): return original track
        if ( Cov.Determinant() <= 0 ) {
	     result[itrack] = smeared_track;
             continue;
        }

        // scale the covariance matrix
        for (int j = 0; j < 5; j++)
        {
          for (int k = 0; k < 5; k++)
          {
            Cov[j][k] = Cov[j][k] * (m_smear_parameters[j] * m_smear_parameters[k]);
          }
        }
        // if (m_debug) {
        // Cov.Print();
        //}

        // generate a new track state (in Delphes's convention)
        TVectorD smeared_param = CovSmear(mcTrackParam, Cov, &m_random, m_debug);

        if ( smeared_param == zero )  {   // Cholesky decomposition failed
            result[itrack] = smeared_track;
            continue;
        }

        // back to the edm4hep conventions..

        double scale0 = 1e-3; // convert mm to m
        double scale1 = 1;
        double scale2 = 0.5 * 1e3; // C = rho/2, convert from mm-1 to m-1
        double scale3 = 1e-3;      // convert mm to m
        double scale4 = 1.;
        scale2 = -scale2; // sign of omega

        smeared_track.D0 = smeared_param[0] / scale0;
        smeared_track.phi = smeared_param[1] / scale1;
        smeared_track.omega = smeared_param[2] / scale2;
        smeared_track.Z0 = smeared_param[3] / scale3;
        smeared_track.tanLambda = smeared_param[4] / scale4;

        // transform rescaled cov matrix from Delphes convention to EDM4hep convention
        smeared_track.covMatrix = track.covMatrix;

        smeared_track.covMatrix[0] = Cov[0][0] / (scale0 * scale0);
        smeared_track.covMatrix[1] = Cov[1][0] / (scale1 * scale0);
        smeared_track.covMatrix[2] = Cov[1][1] / (scale1 * scale1);
        smeared_track.covMatrix[3] = Cov[2][0] / (scale2 * scale0);
        smeared_track.covMatrix[4] = Cov[2][1] / (scale2 * scale1);
        smeared_track.covMatrix[5] = Cov[2][2] / (scale2 * scale2);
        smeared_track.covMatrix[6] = Cov[3][0] / (scale3 * scale0);
        smeared_track.covMatrix[7] = Cov[3][1] / (scale3 * scale1);
        smeared_track.covMatrix[8] = Cov[3][2] / (scale3 * scale2);
        smeared_track.covMatrix[9] = Cov[3][3] / (scale3 * scale3);
        smeared_track.covMatrix[10] = Cov[4][0] / (scale4 * scale0);
        smeared_track.covMatrix[11] = Cov[4][1] / (scale4 * scale1);
        smeared_track.covMatrix[12] = Cov[4][2] / (scale4 * scale2);
        smeared_track.covMatrix[13] = Cov[4][3] / (scale4 * scale3);
        smeared_track.covMatrix[14] = Cov[4][4] / (scale4 * scale4);

        if (m_debug)
        {
          std::cout << std::endl
                    << "Original track " << track.D0 << " " << track.phi << " " << track.omega << " " << track.Z0 << " " << track.tanLambda << std::endl;
          std::cout << "Smeared track " << smeared_track.D0 << " " << smeared_track.phi << " " << smeared_track.omega << " " << smeared_track.Z0 << " " << smeared_track.tanLambda << std::endl;
          std::cout << "MC particle " << mcTrackParam[0] / scale0 << " " << mcTrackParam[1] / scale1 << " " << mcTrackParam[2] / scale2 << " " << mcTrackParam[3] / scale3 << " " << mcTrackParam[4] / scale4 << std::endl;
          for (int j = 0; j < 15; j++)
            std::cout << "smeared cov matrix(" << j << "): " << smeared_track.covMatrix[j] << ", scale factor: " << smeared_track.covMatrix[j] / track.covMatrix[j] << std::endl;
        }
        result[itrack] = smeared_track;

      } // end loop on tracks

      return result;
    }

    // -------------------------------------------------------------------------------------------

    //   to validate the SmearedTracks method.. : retrieve the TrackStates of the MC particles

    ROOT::VecOps::RVec<edm4hep::TrackState> mcTrackParameters(const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> &allRecoParticles,
                                                              const ROOT::VecOps::RVec<edm4hep::TrackState> &alltracks,
                                                              const ROOT::VecOps::RVec<int> &RP2MC_indices,
                                                              const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mcParticles)
    {

      int ntracks = alltracks.size();
      ROOT::VecOps::RVec<edm4hep::TrackState> result;

      edm4hep::TrackState dummy;

      for (int itrack = 0; itrack < ntracks; itrack++)
      {
        edm4hep::TrackState track = alltracks[itrack];

        // find the corresponding MC particle
        int MCindex = -1;
        for (int ireco = 0; ireco < allRecoParticles.size(); ireco++)
        {
          edm4hep::ReconstructedParticleData rp = allRecoParticles[ireco];
          int track_index = rp.tracks_begin;
          if (track_index == itrack)
          {
            MCindex = RP2MC_indices[ireco];
            break;
          }
        } // end loop on RPs

        if (MCindex < 0 || MCindex >= mcParticles.size())
        {
          result.push_back(dummy);
          continue;
        }

        edm4hep::MCParticleData MCpart = mcParticles[MCindex];

        // the MC-truth track parameters
        edm4hep::TrackState mcTrack;
        TVectorD mcTrackParam = TrackParamFromMC_DelphesConv(MCpart);
        // put the into an edm4hep TrackState :
        double scale0 = 1e-3;      // convert mm to m
        double scale2 = 0.5 * 1e3; // C = rho/2, convert from mm-1 to m-1
        double scale3 = 1e-3;      // convert mm to m
        scale2 = -scale2;          // sign of omega
        mcTrack.D0 = mcTrackParam[0] / scale0;
        mcTrack.phi = mcTrackParam[1];
        mcTrack.omega = mcTrackParam[2] / scale2;
        mcTrack.Z0 = mcTrackParam[3] / scale3;
        mcTrack.tanLambda = mcTrackParam[4];

        result.push_back(mcTrack);
      }
      return result;
    }

    // --------------------------------------------------------

    // code from FB

    TVectorD CovSmear(TVectorD x, TMatrixDSym C, TRandom *ran, bool debug = false)
    {

      //
      // Check arrays
      //
      // Consistency of dimensions
      Int_t Nvec = x.GetNrows();
      Int_t Nmat = C.GetNrows();
      if (Nvec != Nmat || Nvec == 0)
      {
        std::cout << "TrkUtil::CovSmear: vector/matrix mismatch. Aborting." << std::endl;
        exit(EXIT_FAILURE);
      }
      // Positive diagonal elements
      for (Int_t i = 0; i < Nvec; i++)
      {
        if (C(i, i) <= 0.0)
        {
          std::cout << "TrkUtil::CovSmear: covariance matrix has negative diagonal elements. Aborting." << std::endl;
          exit(EXIT_FAILURE);
        }
      }
      //
      // Do a Choleski decomposition and random number extraction, with appropriate stabilization
      //
      TMatrixDSym CvN = C;
      TMatrixDSym DCv(Nvec);
      DCv.Zero();
      TMatrixDSym DCvInv(Nvec);
      DCvInv.Zero();
      for (Int_t id = 0; id < Nvec; id++)
      {
        Double_t dVal = TMath::Sqrt(C(id, id));
        DCv(id, id) = dVal;
        DCvInv(id, id) = 1.0 / dVal;
      }
      CvN.Similarity(DCvInv); // Normalize diagonal to 1
      TDecompChol Chl(CvN);
      Bool_t OK = Chl.Decompose(); // Choleski decomposition of normalized matrix
      if (!OK)
      {
        std::cout << "SmearingObjects::CovSmear: covariance matrix is not positive definite. Will use the original track." << std::endl;
        // exit(EXIT_FAILURE);
        TVectorD zero(5);
        for (int k=0; k <5; k++) { zero(k) = 0. ; }
        return zero ;
      }
      TMatrixD U = Chl.GetU();               // Get Upper triangular matrix
      TMatrixD Ut(TMatrixD::kTransposed, U); // Transposed of U (lower triangular)
      TVectorD r(Nvec);
      for (Int_t i = 0; i < Nvec; i++)
        r(i) = ran->Gaus(0.0, 1.0); // Array of normal random numbers
      if (debug)
        std::cout << " random nb " << ran->Gaus(0.0, 1.0) << std::endl;
      TVectorD xOut = x + DCv * (Ut * r); // Observed parameter vector
      //
      return xOut;
    }

    // -------------------------------------------------------------------------------------------

    SmearedReconstructedParticle::SmearedReconstructedParticle(float scale, int type, int mode, bool debug = false)
    {

      // rescale resolution by this factor
      m_scale = scale;

      // apply rescaling only to particle of given type
      // supported: 11 (electrons), 13 (muons), 130 (neutral hadrons), 22 (photon), 0 (charged hadrons), -1 (all)
      m_type = type;

      // 0: energy, 1: momentum
      m_mode = mode;

      // debug flag
      m_debug = debug;
    }

    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> SmearedReconstructedParticle::operator()(
        const ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> &allRecoParticles,
        const ROOT::VecOps::RVec<int> &RP2MC_indices,
        const ROOT::VecOps::RVec<edm4hep::MCParticleData> &mcParticles)
    {

      // returns a vector of ReconstructedParticleData
      // The method retrieve the MC particle that is associated to the ReconstructedParticle,
      // and creates a new ReconstructedParticle with smeared parameters.

      int npart = allRecoParticles.size();

      ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
      result.resize(npart);

      TLorentzVector gen_p4, reco_p4, smeared_p4;

      for (int ipart = 0; ipart < npart; ipart++)
      {

        edm4hep::ReconstructedParticleData reco_part = allRecoParticles[ipart];
        edm4hep::ReconstructedParticleData smeared_part = reco_part;

        int reco_part_type = abs(reco_part.type);

        // have to manually infer pid of ele/mu from mass because type not stored in reco particles
        if (abs(reco_part.charge) > 0 and abs(reco_part.mass - 0.000510999) < 1.e-05)
        {
          reco_part_type = 11;
        }
        else if (abs(reco_part.charge) > 0 and abs(reco_part.mass - 0.105658) < 1.e-03)
        {
          reco_part_type = 13;
        }

        // find the corresponding MC particle
        int MCindex = -1;
        MCindex = RP2MC_indices[ipart];

        // smear particle only if MC particle found, else return original particle
        // and if type == requested
        if (MCindex >= 0 and MCindex < mcParticles.size() and reco_part_type == m_type)
        {
          edm4hep::MCParticleData mc_part = mcParticles[MCindex];

          gen_p4.SetXYZM(mc_part.momentum.x, mc_part.momentum.y, mc_part.momentum.z, mc_part.mass);
          reco_p4.SetXYZM(reco_part.momentum.x, reco_part.momentum.y, reco_part.momentum.z, reco_part.mass);

          float smeared_p = -1;

					if (m_mode == 0)
          {
            // rescale existing smearing of the energy
            smeared_part.energy = gen_p4.E() + m_scale * (reco_p4.E() - gen_p4.E());

            // recompute momentum magnitude
            smeared_p = (smeared_part.energy - reco_p4.M()) > 0 ? std::sqrt(smeared_part.energy * smeared_part.energy - reco_p4.M() * reco_p4.M()) : smeared_part.energy;

						// recompute mom x, y, z using original reco particle direction
						smeared_part.momentum.x = smeared_p * std::sin(reco_p4.Theta()) * std::cos(reco_p4.Phi());
						smeared_part.momentum.y = smeared_p * std::sin(reco_p4.Theta()) * std::sin(reco_p4.Phi());
						smeared_part.momentum.z = smeared_p * std::cos(reco_p4.Theta());

            smeared_p4.SetXYZM(smeared_part.momentum.x, smeared_part.momentum.y, smeared_part.momentum.z, smeared_part.mass);
          }

          // momentum resolution mode
          else if (m_mode == 1)
          {
            // rescale existing momentum smearing
            smeared_p = gen_p4.P() + m_scale * (reco_p4.P() - gen_p4.P());

            // recompute energy
            smeared_part.energy = std::sqrt(smeared_p * smeared_p + reco_p4.M() * reco_p4.M());
						// recompute mom x, y, z using original reco particle direction
						smeared_part.momentum.x = smeared_p * std::sin(reco_p4.Theta()) * std::cos(reco_p4.Phi());
						smeared_part.momentum.y = smeared_p * std::sin(reco_p4.Theta()) * std::sin(reco_p4.Phi());
						smeared_part.momentum.z = smeared_p * std::cos(reco_p4.Theta());

          }

					// return mc truth particle
					else if (m_mode == -1)
					{
						smeared_part.energy = gen_p4.E();
						smeared_p = gen_p4.P();
						smeared_p4 = gen_p4;

						// recompute mom x, y, z using original reco particle direction
						smeared_part.momentum.x = gen_p4.Px();
						smeared_part.momentum.y = gen_p4.Py();
						smeared_part.momentum.z = gen_p4.Pz();

						// set type
						smeared_part.type = mc_part.PDG;
					}

          if (m_debug)
          {
            std::cout << std::endl
                      << "requested smearing energy factor: " << m_scale << std::endl
                      << "gen     part (PID, p, theta, phi, m): " << mc_part.PDG << " " << gen_p4.P() << " " << gen_p4.Theta() << " " << gen_p4.Phi() << " " << gen_p4.M() << std::endl
                      << "reco    part (PID, p, theta, phi, m): " << reco_part_type << " " << reco_p4.P() << " " << reco_p4.Theta() << " " << reco_p4.Phi() << " " << reco_p4.M() << std::endl;
            std::cout << "smeared part (PID, p, theta, phi, m): " << smeared_part.type << " " << smeared_p4.P() << " " << smeared_p4.Theta() << " " << smeared_p4.Phi() << " " << smeared_p4.M() << std::endl;
          }
        }

        result[ipart] = smeared_part;

      } // end loop on particles

      return result;
    }

  } // end NS
} // end NS FCCAnalyses
